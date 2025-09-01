import time
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
import logging
import matplotlib.pyplot as plt
import io
import pandas as pd
from plotly import graph_objects as go
from time import sleep

from models.mysqldb import Mysqldb
from models.metric import Metric
from models.message import Message
from models.sysbf import SysBf

class Robot_newsmaker:
    "Вещает новости в телеграм"

    """
    Robot settings example: 
    {
        "title": "📣⏰ Good morning DIGEST",
        "message_lvl": "all",
        "granularity": "h1",
        "dt": "2024-10-09 23:59:59",
        "dt_delta_sec": -24*60*60 + 1,
        "messages": [
            {
                "title": "Воронка сайта",
                "type": "funnel",
                "granularity": "h1",
                "dt_to": "2024-10-09 23:59:59",
                "dt_delta_sec": -24*60*60 + 1,
                "metric_ids": [2, 7, 41, 21, 23],
                "metric_title": ["Сессии", "Просмотр товара", "Добавили в корзину", "Начало оформления заказа", "Успешный заказ"]
            },
            {
                "title": "Сессии сайта",
                "type": "trend",
                "metric_ids": [2], 
                "metric_title=["Сессии"]
            },
            {
                "title": "Сессии сайта",
                "type": "stack",
                "metric_ids": [2,], 
                "metric_title=["Сессии"]
            }
        ]
    }
    """

    alias = 'newsmaker'
    settings = {}
    config = {}
    comment_str = ''
    db = None
    metric = None
    tz_str_system = ''
    tz_str_db = ''
    message_lvl = 'news'

    def __init__(self, *, settings:None, config:dict={}):
        def_settings = {
            "title":"", 
            "message_lvl": "news", 
            "messages": []
        }

        self.config = config
        self.db = Mysqldb(config['db'])
        self.tz_str_db = config['db'].get('timezone', self.tz_str_db)
        if 'system' in config:
            self.tz_str_system = config['system'].get('timezone', self.tz_str_system)
        if settings and type(settings) is dict:
            self.settings = {**def_settings, **settings}
        else:
            self.settings = def_settings
        self.message_lvl = self.settings["message_lvl"]       

    def comment(self, cstr):
        if self.comment_str != '':
            fin_str = " \n" + cstr
        else:
            fin_str = cstr    
        self.comment_str += fin_str
        return cstr

    def get_date_diapazone(self, *, granularity:str, dt_to:datetime, dt_delta_fr:dict) -> dict:
        "Возвращает словарь с датой начала и датой после конца"

        """
            dt_delta_fr = { # На сколько единиц времени назад начнется отчет, учитывается только одно наибольшее отклонение, значение 0 - не учитывается. Отсчет ведется от первой секунды начала текущего периода
                "month": 0,
                "days": 15,
                "hours": 0
            }  
        """

        result = {}

        if dt_to=="current":
            datetime_now = SysBf.tzdt(datetime.now(), self.tz_str_system)
        else:
            datetime_now = SysBf.tzdt_fr_str(dt_to, self.tz_str_system)  

        if granularity not in ['m1', 'h1', 'd1', 'w1', 'mo1']:
            granularity = 'd1'    

        # Определение даты-времени первой секунды текущего granularity
        if granularity=='m1':
            datetime_to = SysBf.tzdt_fr_str(datetime_now.strftime("%Y-%m-%d %H:%M:00"), self.tz_str_system)  
        if granularity=='h1':
            datetime_to = SysBf.tzdt_fr_str(datetime_now.strftime("%Y-%m-%d %H:00:00"), self.tz_str_system)  
        elif granularity=='d1':    
            datetime_to = SysBf.tzdt_fr_str(datetime_now.strftime("%Y-%m-%d 00:00:00"), self.tz_str_system)  
        elif granularity=='w1':        
            datetime_to = SysBf.tzdt_fr_str(datetime_now.strftime("%Y-%m-%d 00:00:00"), self.tz_str_system)  
            datetime_to = datetime_to - timedelta(days=datetime_to.weekday() % 7)
        elif granularity=='mo1':            
            datetime_to = SysBf.tzdt_fr_str(datetime_now.strftime("%Y-%m-01 00:00:00"), self.tz_str_system)  
        result["dt_to_less"] = datetime_to

        if "month" in dt_delta_fr and dt_delta_fr["month"]>0:
            datetime_from = datetime_to - relativedelta(months=dt_delta_fr["month"])
        elif "days" in dt_delta_fr and dt_delta_fr["days"]>0:
            datetime_from = datetime_to - timedelta(days=dt_delta_fr["days"])    
        else:    
            if "hours" in dt_delta_fr and dt_delta_fr["hours"]>0:
                hours = dt_delta_fr["hours"]      
            else:
                hours = 14*24
            datetime_from = datetime_to - timedelta(hours=hours)    

        return {
            "dt_from": datetime_from,
            "dt_to_less": datetime_to 
        }      


    def run(self, *, output:bool=False) -> dict:
        ######################[ Monitor ]######################### 
        config = self.config
        logging.info(f"Robot {self.alias} run")   

        res = None
        self.comment_str = ''
        start_time = time.time() 

        Message.send(self.settings['title'], lvl=self.message_lvl) 

        message_def = {
            "message_lvl": self.settings["message_lvl"],
            "granularity": self.settings["granularity"],
            "dt_to": self.settings["dt_to"],
            "dt_delta_fr": self.settings["dt_delta_fr"],    
        }
        for message in self.settings['messages']:
            settings={**message_def, **message}
            dt_diapazone = self.get_date_diapazone(granularity=settings["granularity"], 
                                                   dt_to=settings["dt_to"], 
                                                   dt_delta_fr=settings["dt_delta_fr"])
            settings["dt_from"] = dt_diapazone["dt_from"]
            settings["dt_to_less"] = dt_diapazone["dt_to_less"]
            if message['type']=='funnel':
                res = self.get_funnel(settings=settings)
            elif message['type']=='trace':
                res = self.get_trace(settings=settings)
            elif message['type']=='stack':
                res = self.get_stack(settings=settings)    

        Message.send(self.settings['bottom'], lvl=self.message_lvl)         

        return {"success": True, 
                      "telemetry": {
                          "job_execution_sec": round(time.time() - start_time, 4), 
                          "job_max_mem_kb": SysBf.get_max_memory_usage()},
                      "comment": self.comment_str} 
        #######################[ /Monitor ]########################


    def get_funnel(self, *, settings:dict):

        if not "metric_ids" in settings \
            or not "metric_title" in settings \
            or not type(settings["metric_ids"]) is list \
            or not type(settings["metric_title"]) is list \
            or len(settings["metric_ids"])==0 \
            or len(settings["metric_ids"]) != len(settings["metric_title"]):
            return {}
        
        device_alias = settings.get("metric_device_alias", "") 
        trafsrc_alias = settings.get("metric_trafsrc_alias", "")
        
        dt_to = settings["dt_to_less"] -timedelta(seconds=1)
        dt1_str = settings["dt_from"].strftime("%Y-%m-%d")
        dt2_str= dt_to.strftime("%Y-%m-%d")
        if dt1_str==dt2_str:
            dt_diapazone_str = dt1_str
        else:
            dt_diapazone_str = dt1_str + ' - ' + dt2_str 

        data_funnel = {}
        data_funnel["stage"] = settings["metric_title"]
        data_funnel["number"] = Metric.get_sum(db=self.db, 
                granularity=settings["granularity"], 
                dt_from=settings["dt_from"].strftime("%Y-%m-%d %H:%M:%S"), 
                dt_to_less=settings["dt_to_less"].strftime("%Y-%m-%d %H:%M:%S"), 
                device_alias=device_alias, 
                trafsrc_alias=trafsrc_alias,
                metric_ids=settings["metric_ids"])

        df_funnel = pd.DataFrame(data_funnel)

        fig = go.Figure(go.Funnel(y=df_funnel.number,
                                    x=df_funnel.stage,
                                    textposition="auto",
                                    textinfo="value+percent initial",
                                    texttemplate='Всего: %{value:,d} <br> Доля от пред. шага: %{percentPrevious:.1%} <br> Доля от всех: %{percentInitial:.2%}',
                                    orientation='v',
                                    marker={"color": ['#dc143c','#ff0000','#ff4500','#FF6347','#ff7F50'],
                                                "colorscale": 'Hot',
                                            "colorbar": {"bgcolor": None}}
                                    ))
            
        fig.update_layout(autosize=False, height=700, width=1800)
        fig.update_layout(plot_bgcolor='#ffffff')
        fig.update_layout(title_text=f'{settings["title"]} {dt_diapazone_str}')

        # fig.update_traces(textfont_color='black', selector=dict(type='funnel'))
        fig.update_traces(textfont_size=16, selector=dict(type='funnel'))

        fig.update_layout(font_size=13)

        # --------------------- end funnel

        funnel_object = io.BytesIO()
        fig.write_image(funnel_object)
        funnel_object.name = f'funnel_{datetime.now().strftime("%Y%m%d%H%M%S")}.png'
        funnel_object.seek(0)

        Message.send('', img_buf=funnel_object, lvl=self.message_lvl)

        funnel_object.close()

        return {}

    def get_stack(self, *, settings:dict):

        """
        {
            "title": "Пользователи сайта",
            "type": "stack",
            "metric_ids": [201,200], 
            "metric_title": ["Вернувшиеся", "Новые"]
        }
        """

        if not "metric_ids" in settings \
            or not "metric_title" in settings \
            or not type(settings["metric_ids"]) is list \
            or not type(settings["metric_title"]) is list \
            or len(settings["metric_ids"])==0 \
            or len(settings["metric_ids"]) != len(settings["metric_title"]):
            return {}
        
        device_alias = settings.get("metric_device_alias", "") 
        trafsrc_alias = settings.get("metric_trafsrc_alias", "")

        dt_to = settings["dt_to_less"] -timedelta(seconds=1)
        dt1_str = settings["dt_from"].strftime("%Y-%m-%d")
        dt2_str= dt_to.strftime("%Y-%m-%d")
        if dt1_str==dt2_str:
            dt_diapazone_str = dt1_str
        else:
            dt_diapazone_str = dt1_str + ' - ' + dt2_str 
 
        figure_data = []
        for metric_pos, metric_id in enumerate(settings["metric_ids"]):
            res = Metric.get_values(db=self.db, 
                granularity=settings["granularity"], 
                dt_from=settings["dt_from"].strftime("%Y-%m-%d %H:%M:%S"), 
                dt_to_less=settings["dt_to_less"].strftime("%Y-%m-%d %H:%M:%S"), 
                device_alias=device_alias, 
                trafsrc_alias=trafsrc_alias,
                metric_id=metric_id)
            
            x = []
            y = []
            for dt,value in res.items():
                x.append(dt)
                y.append(value)
            
            figure_data.append(go.Bar(
                name = settings["metric_title"][metric_pos],
                x = x,
                y = y
            ))
        
        fig = go.Figure(figure_data)
        
        fig.update_layout(barmode='stack')
        fig.update_layout(autosize=False, height=700, width=1800)
        fig.update_layout(plot_bgcolor='#ffffff')
        fig.update_layout(title_text=f'{settings["title"]} {dt_diapazone_str}')

        stack_object = io.BytesIO()
        fig.write_image(stack_object)
        stack_object.name = f'stack_{datetime.now().strftime("%Y%m%d%H%M%S")}.png'
        stack_object.seek(0)

        Message.send('', img_buf=stack_object, lvl=self.message_lvl)

        stack_object.close()

        return {}

    def get_trace(self, *, settings:dict):

        """
        {
            "title": "Сессии, пользователи сайта",
            "type": "trend",
            "metric_ids": [2,1], 
            "metric_title": ["Сессии","Пользователи"]
        }
        """

        if not "metric_ids" in settings \
            or not "metric_title" in settings \
            or not type(settings["metric_ids"]) is list \
            or not type(settings["metric_title"]) is list \
            or len(settings["metric_ids"])==0 \
            or len(settings["metric_ids"]) != len(settings["metric_title"]):
            return {}
        
        device_alias = settings.get("metric_device_alias", "") 
        trafsrc_alias = settings.get("metric_trafsrc_alias", "")

        dt_to = settings["dt_to_less"] -timedelta(seconds=1)
        dt1_str = settings["dt_from"].strftime("%Y-%m-%d")
        dt2_str= dt_to.strftime("%Y-%m-%d")
        if dt1_str==dt2_str:
            dt_diapazone_str = dt1_str
        else:
            dt_diapazone_str = dt1_str + ' - ' + dt2_str 
        
        fig = go.Figure()
        for metric_pos, metric_id in enumerate(settings["metric_ids"]):
            res = Metric.get_values(db=self.db, 
                granularity=settings["granularity"], 
                dt_from=settings["dt_from"].strftime("%Y-%m-%d %H:%M:%S"), 
                dt_to_less=settings["dt_to_less"].strftime("%Y-%m-%d %H:%M:%S"), 
                device_alias=device_alias, 
                trafsrc_alias=trafsrc_alias,
                metric_id=metric_id)    
            x = []
            y = []
            for dt,value in res.items():
                x.append(dt)
                y.append(value)
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name=settings["metric_title"][metric_pos]))

        # fig.update_traces(marker=dict(size=10, line=dict(width=3, color='blue'))) 
        # fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
        #           font=dict(family='Arial', size=14, color='white'))
        
        fig.update_layout(xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
               yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'))
        
        fig.update_layout(autosize=False, height=700, width=1800)
        fig.update_layout(plot_bgcolor='#e4ebf5')
        fig.update_layout(title_text=f'{settings["title"]} {dt_diapazone_str}')

        stack_object = io.BytesIO()
        fig.write_image(stack_object)
        stack_object.name = f'trace_{datetime.now().strftime("%Y%m%d%H%M%S")}.png'
        stack_object.seek(0)

        Message.send('', img_buf=stack_object, lvl=self.message_lvl)

        stack_object.close()

        return {}
    










        """
        if self.metric and self.metric.info['metric_monitor']>0: 
            # Данные заберем с коррекцией с учетом таймзоны, но не будем это фиксировать.
            # значения дат будут в timezone БД, но не будет метки  
            # на этапе добавления инцидентов мы зафиксируем таймзону без изменения времени.
            reliance = self.metric.get_data(accum_items=self.settings['data']['accum_items'], 
                                            dt_from=self.settings['data']['dt_from'], 
                                            last_items=self.settings['data']['last_items'], tz_str=self.tz_str_db)
            res = reliance.squeeze()
            
            if len(res)>0:
                # direction: 'pos', 'neg', 'both', 'bothsplit'

                anom_dict = {'anoms': pd.Series(), 'plot': None}
                anom_dict_neg = {'anoms': pd.Series(), 'plot': None}
                anom_dict_pos = {'anoms': pd.Series(), 'plot': None}
                try:
                    if self.settings['anoms']['direction'] == 'bothsplit':
                        anoms_settings = dict(self.settings['anoms'])
                        anoms_settings['direction'] = 'both'
                        anom_dict = tad(res, **anoms_settings) # Всегда отдает {"anoms":pd.Series, ...} Не проверяем
                        anoms = anom_dict['anoms']
                        self.metric.add_anoms(anoms=anom_dict['anoms'], 
                                            metric_group_id=self.metric.info['metric_group_id'], 
                                            metric_project_id=self.metric.info['metric_project_id'],
                                            tz_str_to=self.tz_str_db)
                    
                    if self.settings['anoms']['direction'] in ['neg','both']:
                        anoms_settings = dict(self.settings['anoms'])
                        # Учет реверса значений метрик - например негативное состояние ошибки - превышение нормы
                        if self.metric.info['neg_reverce']==0:
                            anoms_settings['direction'] = 'neg'
                        else:
                            anoms_settings['direction'] = 'pos'    
                        anom_dict_neg = tad(res, **anoms_settings) 
                        self.metric.add_anoms(anoms=anom_dict_neg['anoms'], direction="neg", 
                                            metric_group_id=self.metric.info['metric_group_id'], 
                                            metric_project_id=self.metric.info['metric_project_id'],
                                            tz_str_to=self.tz_str_db)

                    if self.settings['anoms']['direction'] in ['pos','both']:
                        anoms_settings = dict(self.settings['anoms'])
                        # Учет реверса значений метрик - например негативное состояние ошибки - превышение нормы
                        if self.metric.info['neg_reverce']==0:
                            anoms_settings['direction'] = 'pos'
                        else:
                            anoms_settings['direction'] = 'neg'  
                        anom_dict_pos = tad(res, **anoms_settings) 
                        self.metric.add_anoms(anoms=anom_dict_pos['anoms'], direction="pos", 
                                            metric_group_id=self.metric.info['metric_group_id'], 
                                            metric_project_id=self.metric.info['metric_project_id'],
                                            tz_str_to=self.tz_str_db)
                except:
                    logging.warning(self.comment(f"metric [{self.settings['data']['metric_id']}] {self.metric.info['metric_name']}: TAD ERROR!"))   

                # Отошлем сообщения о последней неповторяющейся аномалии в течении message_dt_lag_sec
                actual_anom = self.metric.get_actual_anom(message_dt_lag_sec=self.message_dt_lag_sec, tz_str=self.tz_str_db)
                if not actual_anom is None:
                    message_lvl = self.settings['message_lvl']
                    # metric_anom_dt = actual_anom['dt'].strftime('%Y-%m-%d %H:%M')

                    # Сформируем график по последней неделе
                    anoms = anom_dict['anoms']
                    anoms_pos = anom_dict_pos['anoms']
                    anoms_neg = anom_dict_neg['anoms']

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
                    if len(anoms)>0:
                        anoms2 = SysBf.filter_series_by_datetime(anoms, datetime_from)
                        ax.scatter(anoms2.index.values, anoms2, color='yellow')    
                    ax.set_xlabel('Date time')
                    ax.set_ylabel('Count')
                    ax.set_title(self.metric.info['metric_name'])
                    img_buf = io.BytesIO()
                    fig.savefig(img_buf, format='png')
                    img_buf.seek(0)

                    metric_name = self.metric.info.get('metric_name', self.metric.info['metric_alias'])
                    msg_metric_id = self.metric.info['id']
                    msg_granularity = self.granularity

                    msg_anom_pos = config['message_str'].get('msg_anom_pos', "{metric_name}: Превышение нормы!").format(metric_name=metric_name)
                    msg_anom_neg = config['message_str'].get('msg_anom_neg', "{metric_name}: Ниже нормы!").format(metric_name=metric_name)
                    msg_anom_all = config['message_str'].get('msg_anom_all', "{metric_name}: Аномальное значение!").format(metric_name=metric_name)
                    if self.metric.info['metric_project_id']==1:
                        msg_link_str = config['message_str'].get('msg_link1', "").format(msg_metric_id=msg_metric_id, msg_granularity=msg_granularity)
                    if self.metric.info['metric_project_id']==2:
                        msg_link_str = config['message_str'].get('msg_link2', "").format(msg_metric_id=msg_metric_id, msg_granularity=msg_granularity)
                    else:
                        msg_link_str = config['message_str'].get('msg_link', "").format(msg_metric_id=msg_metric_id, msg_granularity=msg_granularity)
                    if actual_anom['direction']=='pos':
                        if self.metric.info['neg_reverce']==0:
                            message_str = '\U0001F7E2 ' + msg_anom_pos + msg_link_str
                            if message_lvl == 'critical':
                                message_lvl = 'important'
                        else:
                            message_str = '\U0001F7E2 ' + msg_anom_neg + msg_link_str    
                    elif actual_anom['direction']=='neg':
                        if self.metric.info['neg_reverce']==0:
                            message_str = '\U0001F534 ' + msg_anom_neg + msg_link_str
                        else:
                            message_str = '\U0001F534 ' + msg_anom_pos + msg_link_str  
                            if message_lvl == 'critical':
                                message_lvl = 'important'  
                    else:    
                        message_str = '\U0001F7E1 ' + msg_anom_all + msg_link_str
                    tg_status = Message.send(message_str, lvl=message_lvl, img_buf=img_buf) 
                    if tg_status>0:
                        self.metric.set_anom_posted(actual_anom['id'])   
                    else:    
                        pass
                    plt.clf()
            else:
                metric_name = self.metric.info.get('metric_name', self.metric.info['metric_alias'])
                logging.warning(self.comment(f'No Data for metric {metric_name}!'))    
        """
        return {}    