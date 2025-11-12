import time
from datetime import timedelta, datetime
import logging
import matplotlib.pyplot as plt
import io
import pandas as pd

from models.anomaly_detect import anomaly_detect 
from models.mysqldb import Mysqldb
from models.metric import Metric
from models.message import Message
from models.project import Project
from models.sysbf import SysBf

class Robot_twanom:
    "Поиск инцидентов по временным рядам"

    """
    Robot settings example: 
    {
        "data":{"region_alias": "", "device_alias": ""}, 
        "anoms":{"direction": "neg", "max_anoms": 0.2, "alpha": 0.01, "piecewise_median_period_weeks": 2}
    }
    """

    alias = 'twanom'
    settings = {}
    config = {}
    comment_str = ''
    db = None
    metric = None
    message_dt_lag_sec = 24 * 60 * 60 
    granularity = ''
    tz_str_system = ''
    tz_str_db = ''

    def __init__(self, *, settings:None, config:dict={}):
        data_settings = {"metric_id":0, "project_id":0, "metric_tag_id":0, "granularity":"", "region_alias": "", 
                         "device_alias":"", "accum_items":1, "dt_from":"", "last_items":0}
        anom_settings = {"max_anoms":0.1, "direction":"both", "direction_reverce":False, "alpha":0.05, "only_last":None,
                      "threshold":None, "e_value":False, "longterm":False, "piecewise_median_period_weeks":2,
                      "y_log":False, "verbose":False, "resampling":False, "period_override":None}
        
        self.config = config
        self.db = Mysqldb(config['db'])
        if settings and type(settings) is dict:
            self.settings = settings 
        if not self.settings['data']:
            self.settings['data'] = {}        
        if not self.settings['anoms']:
            self.settings['anoms'] = {}       
        self.settings['data'] = {key: self.settings['data'].get(key, data_settings[key]) for key in data_settings}
        self.settings['anoms'] = {key: self.settings['anoms'].get(key, anom_settings[key]) for key in anom_settings} 
        self.settings['message_lvl'] = self.settings.get('message_lvl', '')
        self.message_dt_lag_sec = int(config['system'].get('message_dt_lag_sec', self.message_dt_lag_sec))
        self.message_dt_lag_sec = int(config['granularity_list'][self.settings['data']['granularity']].get('message_dt_lag_sec', self.message_dt_lag_sec))
        self.metric = Metric.get_metric(db=self.db, id=self.settings['data']['metric_id'], 
                              project_id=self.settings['data']['project_id'], 
                              metric_tag_id=self.settings['data']['metric_tag_id'],          
                              granularity=self.settings['data']['granularity'],
                              )
        self.granularity = self.settings['data']['granularity']
        self.tz_str_db = config['db'].get('timezone', self.tz_str_db)

        if 'system' in config:
            self.tz_str_system = config['system'].get('timezone', self.tz_str_system)


    def comment(self, cstr):
        if self.comment_str != '':
            fin_str = " \n" + cstr
        else:
            fin_str = cstr    
        self.comment_str += fin_str
        return cstr
    

    def run(self, *, output:bool=False) -> dict:
        ######################[ Monitor ]######################### 
        config = self.config
        logging.info(f"Robot {self.alias} run with metric [{self.settings['data']['metric_id']}] {self.metric.info['metric_name']} dp: [{self.metric.info['metric_dp']}]")   
        res = None
        anoms = None
        self.comment_str = ''
        start_time = time.time() 
        datetime_now = SysBf.tzdt(datetime.now(), self.tz_str_system)
        dt_from_str = self.settings['data'].get('dt_from', '')
        dt_from = None
        if dt_from_str!='':
            dt_from = SysBf.tzdt_fr_str(dt_from_str, self.tz_str_system)
        # print('metric_monitor=', self.metric.info['metric_monitor'])
        if self.metric and self.metric.info['metric_monitor']>0: 
            # Если granularity>"h1", то берем данные за последние пол года
            if self.settings['data']['granularity']!="h1" and self.settings['data']['granularity']!="m1":
                dt_from = datetime_now - timedelta(days=6*30+4)
            reliance = self.metric.get_data(accum_items=self.metric.info['accum_items'], 
                                            dt_from=dt_from, 
                                            last_items=self.settings['data']['last_items'], 
                                            tz_str=self.tz_str_system, tz_str_db=self.tz_str_db, drop_tz=True)
            res = reliance.squeeze()
            
            if len(res)>0:
                # direction: 'pos', 'neg', 'both', 'bothsplit'

                anom_dict = {'anoms': pd.Series(), 'anoms_pos': pd.Series(), 'anoms_neg': pd.Series(), 'expected': None}
                try:
                # if True:
                    anoms_settings = dict(self.settings['anoms'])
                    direction = anoms_settings['direction']
                    if self.settings['anoms']['direction'] == 'bothsplit':
                        anoms_settings['direction'] = 'both'
                    if self.metric.info['neg_reverce']>0:
                        anoms_settings['direction_reverce'] = True   
                    # anoms_settings['direction_reverce'] = True # TODO - для теста         
                    anom_dict = anomaly_detect(res, **anoms_settings) # Всегда отдает {"anoms":pd.Series, ...} Не проверяем
                    if direction == 'bothsplit':
                        self.metric.add_anoms(anoms=anom_dict['anoms'], 
                                            tz_str=self.tz_str_system, tz_str_db=self.tz_str_db)
                    else:
                        if direction in ['neg','both']:
                            self.metric.add_anoms(anoms=anom_dict['anoms_neg'], direction='neg', 
                                            tz_str=self.tz_str_system, tz_str_db=self.tz_str_db)
                            
                        if direction in ['pos','both']:
                            self.metric.add_anoms(anoms=anom_dict['anoms_pos'], direction='pos', 
                                            tz_str=self.tz_str_system, tz_str_db=self.tz_str_db)    

                except:
                # else:
                    logging.warning(self.comment(f"metric [{self.settings['data']['metric_id']}] {self.metric.info['metric_name']}: Anomaly Detect ERROR!"))   

                # Отошлем сообщения о последней неповторяющейся аномалии в течении message_dt_lag_sec
                actual_anom = self.metric.get_actual_anom(message_dt_lag_sec=self.message_dt_lag_sec, tz_str=self.tz_str_db)
                if not actual_anom is None:
                    message_lvl = self.settings['message_lvl']
                    # metric_anom_dt = actual_anom['dt'].strftime('%Y-%m-%d %H:%M')

                    # Сформируем график по последней неделе
                    anoms = anom_dict['anoms']
                    anoms_pos = anom_dict['anoms_pos']
                    anoms_neg = anom_dict['anoms_neg']

                    datetime_from = datetime.now() - timedelta(days=15)
                    res2 = SysBf.filter_series_by_datetime(res, datetime_from)
                    fig, ax = plt.subplots(1, figsize=(15,5))
                    res2.plot(ax=ax)
                    if len(anoms_pos)>0:
                        anoms_pos2 = SysBf.filter_series_by_datetime(anoms_pos, datetime_from)
                        ax.scatter(anoms_pos2.index.values, anoms_pos2, color='green')
                    if len(anoms_neg)>0:
                        anoms_neg2 = SysBf.filter_series_by_datetime(anoms_neg, datetime_from)
                        ax.scatter(anoms_neg2.index.values, anoms_neg2, color='red')
                    if self.settings['anoms']['direction']=='bothsplit' and len(anoms)>0:
                        anoms2 = SysBf.filter_series_by_datetime(anoms, datetime_from)
                        ax.scatter(anoms2.index.values, anoms2, color='yellow')    
                    ax.set_xlabel('Date time')
                    ax.set_ylabel('Count')
                    ax.set_title(self.metric.info['metric_name'] + ' [accum_items=' + str(self.metric.info['accum_items']) + ']')
                    img_buf = io.BytesIO()
                    fig.savefig(img_buf, format='png')
                    img_buf.seek(0)

                    metric_name = self.metric.info.get('metric_name', self.metric.info['metric_alias'])
                    msg_metric_id = self.metric.info['id']
                    msg_granularity = self.granularity 

                    project_id = self.settings['data']['project_id']
                    project_name = f"[{project_id}]"
                    project = Project(db=self.db, id=project_id)
                    if not project is None:
                        project_name = project.info["metric_project_name"]
                    
                    msg_anom_pos = config['message_str'].get('msg_anom_pos', "{project_name} - {metric_name}: Превышение нормы!").format(metric_name=metric_name, project_name=project_name)
                    msg_anom_neg = config['message_str'].get('msg_anom_neg', "{project_name} - {metric_name}: Ниже нормы!").format(metric_name=metric_name, project_name=project_name)
                    msg_anom_all = config['message_str'].get('msg_anom_all', "{project_name} - {metric_name}: Аномальное значение!").format(metric_name=metric_name, project_name=project_name)
                    msg_link = config['message_str']['msg_link'].get(f"{self.metric.info['metric_project_id']}", "")
                    if msg_link!="":
                        msg_link = config['message_str']['msg_link'].get("default", "")    
                    msg_link_str = msg_link.format(msg_metric_id=msg_metric_id, msg_granularity=msg_granularity, project_id=project_id)
                    if actual_anom['direction']==1:
                        if self.metric.info['neg_reverce']==0:
                            message_str = "\U0001F7E2 " + msg_anom_pos + msg_link_str
                            if message_lvl == 'critical':
                                message_lvl = 'important'
                        else:
                            message_str = "\U0001F7E2 " + msg_anom_neg + msg_link_str    
                    elif actual_anom['direction']==-1:
                        if self.metric.info['neg_reverce']==0:
                            message_str = "\U0001F534 " + msg_anom_neg + msg_link_str
                        else:
                            message_str = "\U0001F534 " + msg_anom_pos + msg_link_str  
                            if message_lvl == 'critical':
                                message_lvl = 'important'  
                    else:    
                        message_str = "\U0001F7E1 " + msg_anom_all + msg_link_str
                    tg_status = Message.send(message_str, lvl=message_lvl, img_buf=img_buf, project_id=project_id) 
                    if tg_status>0:
                        self.metric.set_anom_posted(actual_anom['id'])   
                    else:    
                        pass
                    plt.clf()
            else:
                metric_name = self.metric.info.get('metric_name', self.metric.info['metric_alias'])
                logging.warning(self.comment(f"No Data for metric [{self.settings['data']['metric_id']}] {metric_name}!"))    
            
        anoms = None
        anoms_neg = None
        anoms_pos = None
        if output:
            anoms = self.metric.get_anoms(tz_str=self.tz_str_db, dt_from=dt_from, drop_tz=True)   
            anoms_neg = self.metric.get_anoms(direction='neg', tz_str=self.tz_str_db, dt_from=dt_from, drop_tz=True)   
            anoms_pos = self.metric.get_anoms(direction='pos', tz_str=self.tz_str_db, dt_from=dt_from, drop_tz=True)   
            res.sort_index(inplace=True)
            anoms.sort_index(inplace=True)
            anoms_neg.sort_index(inplace=True)
            anoms_pos.sort_index(inplace=True)
        return {"success": True, 
                      "telemetry": {
                          "job_execution_sec": round(time.time() - start_time, 4), 
                          "job_max_mem_kb": SysBf.get_max_memory_usage()},
                      "data": res,
                      "anoms": anoms,
                      "anoms_neg": anoms_neg,
                      "anoms_pos": anoms_pos,
                      "comment": self.comment_str} 
        #######################[ /Monitor ]########################