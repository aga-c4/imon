import datetime
import logging
import pandas as pd

from models.mysqldb import Mysqldb
from models.sysbf import SysBf


class Metric:

    table = 'metrics'    
    data_table = 'metrics_' 
    anoms_table = 'anoms_' 
    groups_table = 'metric_groups'   
    tags_table = 'tags'
    id = None
    granularity = None
    metric_tag_id = ""
    project_id = 0
    info = None
    dp = 0

    def __init__(self, *, db:Mysqldb, id:int, granularity:str='', project_id:int=0, metric_tag_id:int=0):
        """
        metric_id=1 # Идентификатор метрики
        granularity='h1' # Отслеживаемые диапазоны m1/h1/d1/w1/mo1
        project_id=0 # Идентификатор проекта
        metric_tag_id=0 # Идентификатор тега метрики
        dt_from = '' # Дата-время в формате 'ГГГГ-ММ-ДД чч-мм-сс'
        """
        assert id > 0, 'Metric.get_data: id is not set'
        assert granularity != '', 'Metric.get_data: granularity options: m1 | h1 | d1 | w1 | mo1 | ...'

        self.db = db
        self.id = id
        self.granularity = granularity
        self.metric_tag_id = metric_tag_id   
        self.project_id = project_id   
        self.info = self.get_info()
        self.dp = self.info.get('metric_dp', 0)
        self.parentid = self.info.get('parentid', 0)
        self.metric_group_id = self.info.get('metric_group_id', 0)

    @staticmethod
    def get_metric(*, db:Mysqldb, id:int, granularity:str='', project_id:int=0, metric_tag_id:int=0):
        """
        metric_id=1 # Идентификатор метрики
        granularity='h1' # Отслеживаемые диапазоны m1/h1/d1/w1/mo1
        project_id=0 # Идентификатор проекта
        metric_tag_id # Идентификатор тега
        dt_from = '' # Дата-время в формате 'ГГГГ-ММ-ДД чч-мм-сс'
        """
        if not id:
            return None
        metric = Metric(db=db, id=id, granularity=granularity, project_id=project_id, metric_tag_id=metric_tag_id)
        if not metric.info:
            return None
        return metric
    
    def get_info(self) -> dict:
        sql = f"SELECT * from {self.table} where id={self.id};"     
        result = self.db.query(sql)
        info = None
        if result: 
            info = result[0]  
        return info     

    @staticmethod
    def get_groups(*, db:Mysqldb) -> list:
        sql = f"SELECT * from {Metric.groups_table};"     
        result = db.query(sql)
        return result  
    
    @staticmethod
    def get_tags(*, db:Mysqldb, project_id:int=0) -> list:
        sql = f"SELECT id,tag from {Metric.tags_table} where project_id={project_id};"     
        result = db.query(sql)
        return result 
    
    @staticmethod
    def add_tag(*, db:Mysqldb, project_id:int=0, metric_tag:str="") -> list:
        sql = f"INSERT INTO {Metric.tags_table} (project_id, tag) VALUES ({project_id}, '{metric_tag}');"
        logging.info(f'Add tag {metric_tag} to project_id project_id')
        return db.insert(sql) 

    @staticmethod
    def get_list(*, db:Mysqldb, group_id:int=0, source_id:int=None, metric_type:str='', order:str='') -> list:
        sql = f"SELECT * from {Metric.table}  WHERE metric_active = 1"
        if group_id>0:
            sql += f" and metric_group_id={group_id}"    
        if not source_id is None:
            sql += f" and source_id={source_id}"   
        if metric_type!='':
            sql += f" and metric_type='{metric_type}'" 
        if order!='':
            sql += f" order by {order}"   
        sql += ';'        
        result = db.query(sql)
        return result  
    
    @staticmethod
    def clear_table(*, db:Mysqldb, granularity:str='', metric_id:int=0, date_to:datetime):
        "Очищает таблицу значений метрик, установите date_to в будущее, удалит все, если не задано metric_id, удалит по всем метрикам"
        sql = f"DELETE from {Metric.data_table}{granularity} where dt<'" + str(date_to)+"';"
        if metric_id>0:
            sql += f" and metric_id={metric_id}"                                                                                         
        sql += ";" 
        result = db.delete(sql)
        return result   

    @staticmethod
    def get_last_dt(*, db:Mysqldb, granularity:str='h1', id:int=0, tz_str:str='', project_id:int=0, source_id:int=None) -> datetime:
        if not source_id is None:
            # Выдадим время последней зарегистрированной метрики с заданным алиасом источника по заданному проекту
            sql = f"SELECT max(dt) as maxdt from {Metric.data_table}{granularity} where metric_id={id} and metric_project_id={project_id} and metric_source_id={source_id};"
        elif id==0:
            return SysBf.tzdt(datetime.datetime.fromtimestamp(0), tz_str)    
        else: 
            sql = f"SELECT max(dt) as maxdt from {Metric.data_table}{granularity} where metric_id={id} and metric_project_id={project_id};"
        result = db.query(sql) 
        if result:
            if not result[0]['maxdt'] is None:
                return SysBf.tzdt(result[0]['maxdt'], tz_str)
        return SysBf.tzdt(datetime.datetime.fromtimestamp(0), tz_str)
    
    @staticmethod
    def get_minmax_dt(*, db:Mysqldb, granularity:str='' , id:int, tz_str:str='', project_id:int=0) -> dict:
        if id==0:
            return {"mindt": None, "maxdt": None}

        sql = f"SELECT max(dt) as maxdt, min(dt) as mindt from {Metric.data_table}{granularity} where metric_id={id} and metric_project_id={project_id};"
        result = db.query(sql) 
        res = {"mindt": None, "maxdt": None}
        if result:
            if not result[0]['mindt'] is None:
                res['mindt'] = SysBf.tzdt(result[0]['mindt'], tz_str)
            if not result[0]['maxdt'] is None:
                res['maxdt'] = SysBf.tzdt(result[0]['maxdt'], tz_str)
        return res
    
    @staticmethod
    def stupdateval(*, db:Mysqldb, granularity:str='', metric_id:int=0, project_id:int=0, metric_tag_id:int=0, metric_dt:datetime, params:dict={}):
        sql = f"UPDATE `{Metric.data_table}{granularity}` SET "
        upd = False
        dt_str = str(metric_dt) # datetime.datetime.strftime(metric_dt, '%Y-%m-%d %H:%M:%S')
        for key, value in params.items():
            if key!='dt':
                if upd:   
                    sql += ', '
                sql += f"{key}='{value}'"
                upd = True
        
        if upd:   
            sql += f" WHERE metric_id={metric_id} and metric_project_id={project_id} and metric_tag_id={metric_tag_id} and dt='{dt_str}';"
            result = db.update(sql)
            return result 
        return 0

    def updateval(self, *, metric_dt:datetime, params:dict={}):
        return Metric.stupdateval(db=self.db, granularity=self.granularity, metric_id=self.id, 
                                  project_id=self.project_id, metric_tag_id=self.metric_tag_id,  
                                  metric_dt=metric_dt, params=params)

    @staticmethod
    def insert_list(*, db:Mysqldb, granularity:str='', params:list=[]):
        "Состав полей должен быть одинаковым, иначе будет все добавляться по первому элементу!"
        sql = f"INSERT INTO {Metric.data_table}{granularity}"
        key_str = ''
        val_str = ''
        upd = False
        for mitem in params:
            if key_str=='':
                for key, value in mitem.items():
                    if key_str=='':
                        key_str += ' ('
                    else:        
                        key_str += ', '     
                    key_str += f"{key}"
                sql += key_str + ') VALUES'

            if val_str=='':   
                val_str+=' ('
            else:
                val_str+=', ('

            vcnt = 0        
            for key, value in mitem.items():
                if vcnt>0:   
                    val_str += ', '
                val_str += f"'{value}'"
                upd = True
                vcnt +=1
            val_str += ')'    
        
        sql += val_str + ';'
        if upd:   
            result = db.insert(sql)
            return result 
        return 0
    
    @staticmethod
    def get_sum(*, db:Mysqldb, 
                   granularity:str, 
                   dt_from:str='', dt_to:str='', dt_from_more:str='', dt_to_less:str='', tz_str:str='',
                   metric_ids:list=None, metric_parentids:list=None, project_id:int=0, metric_tag_id:int=0) -> dict:

        metric_id_str_all = '' 
        gr_by_str = ""
        ids = []   
        if type(metric_ids) is list and len(metric_ids)>0:
            ids = metric_ids  
            gr_by_str = "metric_id"
            if len(metric_ids)==1:
                metric_id_str_all = f"metric_id={metric_ids[0]}"    
            else:  
                metric_ids_str = ','.join(map(str, ids))
                metric_id_str_all = f"metric_id in ({metric_ids_str})"    
        elif (metric_parentids) is list and len(metric_parentids)>0:
            ids = metric_parentids
            gr_by_str = "metric_parentid"
            if len(metric_ids)==1:
                metric_id_str_all = f"metric_parentid={metric_parentids[0]}"    
            else:
                metric_parent_ids_str = ','.join(map(str, ids))
                metric_id_str_all = f"metric_parentid in ({metric_parent_ids_str})"      
        
        res = [] 
        items = {}
        for item, id in enumerate(ids):
            items[str(id)] = int(item)
            res.append(0)    

        if metric_id_str_all!="":   
            sql = f"SELECT metric_id as metric_id, sum(value/POW( 10, dp )) as value from {Metric.data_table}{granularity} where {metric_id_str_all} and metric_project_id={project_id} and metric_tag_id={metric_tag_id}"
            if dt_from!='':
                sql += f" and dt>='{dt_from}'"
            if dt_to!='':
                sql += f" and dt<='{dt_to}'"   
            if dt_from_more!='':
                sql += f" and dt>'{dt_from_more}'"
            if dt_to_less!='':
                sql += f" and dt<'{dt_to_less}'"  
            if gr_by_str!='':    
                sql += f" GROUP BY {gr_by_str}" 
            sql += ";"      
            result = db.query(sql)  
            if type(result) is list:
                for row in result: 
                    res[items[str(row['metric_id'])]] = row['value'] 
                    
        return res

    @staticmethod
    def get_values(*, db:Mysqldb, 
                   granularity:str, 
                   dt_from:str='', dt_to:str='', dt_from_more:str='', dt_to_less:str='', tz_str:str='', orderby:str='',
                   metric_id:int=0, metric_parentid:int=0, project_id:int=0, metric_tag_id:int=0) -> dict: 
        if metric_id>0:
            metric_id_str = 'metric_id'   
            metric_id_val = metric_id   
        elif metric_parentid>0:
            metric_id_str = 'metric_parentid'   
            metric_id_val = metric_parentid       
        else:    
            metric_id_val = 0     
        res = {} 
        if metric_id_val>0:  
            sql = f"SELECT dt, value, dp from {Metric.data_table}{granularity} where {metric_id_str}={metric_id_val} and metric_project_id={project_id} and metric_tag_id={metric_tag_id}"
            if dt_from!='':
                sql += f" and dt>='{dt_from}'"
            if dt_to!='':
                sql += f" and dt<='{dt_to}'"   
            if dt_from_more!='':
                sql += f" and dt>'{dt_from_more}'"
            if dt_to_less!='':
                sql += f" and dt<'{dt_to_less}'"  
            if orderby!='':                     
                sql += f" ORDER BY {orderby};"
            else:
                sql += f" ORDER BY dt;"    
            result = db.query(sql)   
            found_data = 0
            if type(result) is list:
                for row in result:   
                    if (found_data == 0):
                        if row['value'] is None or not row['value']:
                            row['value'] = 0
                    value = 0
                    if not row['value'] is None and row['value']:
                        value = row['value']/(10**row['dp'])
                    res[SysBf.tzdt(row['dt'], tz_str)] = value
        return res

    def get_data(self, *, accum_items:int=1, dt_from:str='', last_items:int=0, tz_str:str='') -> pd.DataFrame:
        '''Вернет данные по метрике, ключ - datetime в timezone базы данных
        accum_items = '24' # Количество значений в аккумуляторе (1 - не используем, 7 - для дней по неделям, 24 - для суток по часам)
        last_items = 0 # Если больше нуля, то берется это количество элементов с конца после даты начала 
        '''

        sql = f"SELECT dt, value, dp from {self.data_table}{self.granularity} where metric_id={self.id} and metric_project_id={self.project_id} and metric_tag_id={self.metric_tag_id}"
        
        if dt_from!='':
            sql += f" and dt>='{dt_from}'"
            
        if last_items:
            if dt_from:
                sql += f" LIMIT 0,{last_items}"
            else:
                sql += f" ORDER BY id DESC LIMIT 0,{last_items}"

        sql += ';'
        
        result = self.db.query(sql)   
        if last_items and not dt_from:
            result.reverse()

        res = {"date_time":[], "count":[]}
        found_data = 0
        accum = []
        for row in result:   
            if (found_data == 0):
                if row['value'] is None or not row['value']:
                    continue
                else:
                    found_data = 1
            
            value = 0
            if not row['value'] is None and row['value']:
                value = row['value']/(10**self.dp)
            if accum_items>1:
                if len(accum) >= accum_items: # часы в сутках, если полный набор, то отрежем первое значение
                    accum.pop(0)
                accum.append(value)
                accum_len = len(accum)
                if accum_len>=accum_items:
                    res["count"].append(sum(accum)/accum_len)
                    res["date_time"].append(row['dt'])
            else:
                res["count"].append(value)
                res["date_time"].append(row['dt'])

        del(result)       

        reliance = pd.DataFrame(res["count"], index=res["date_time"], columns=['count'])  
        reliance.index.name = "date_time"

        return reliance

    def get_last_anom_dt(self, * , direction:int=0, tz_str:str='') -> dict:
        sql = f"SELECT dt, metric_value from {self.anoms_table}{self.granularity} where \
                metric_id={self.id} and metric_project_id={self.project_id} and metric_tag_id={self.metric_tag_id}"
        if direction != 0:
            sql += f" and direction=direction"    
        sql += " ORDER BY dt DESC LIMIT 0,1;"
        result = self.db.query(sql) 
        if result:
            return SysBf.tzdt(result[0]['dt'], tz_str)
        return None

    def add_anoms(self, *, 
                  anoms:pd.Series=pd.Series(), 
                  direction:str='',  
                  tz_str_to:str='') -> int:
        'Метки времени ожидаются в timezone базы данных без маркировки таймозны'

        if direction=='pos':
            direction_val = 1
        if direction=='neg':
            direction_val = -1
        else:       
            direction_val = 0
        sql = f"INSERT INTO {self.anoms_table}{self.granularity} (dt, metric_id, metric_parentid, metric_value, region_alias, device_alias, trafsrc_alias, direction, metric_project_id, metric_tag_id) VALUES "

        anoms = anoms.to_dict()
        counter_all = 0
        counter = 0
        last_anom_dt = self.get_last_anom_dt(direction=direction_val, tz_str=tz_str_to)
        for key, value in anoms.items():
            key_wtz = SysBf.tzdt(key, tz_str_to)
            if last_anom_dt is None or key_wtz > last_anom_dt:
                formatted_dt = str(key_wtz)
                value = int(value * (10**self.dp))
                if value>2140000000:
                    logging.warning(f"Anom Very big fin value: {value} dp: {self.dp}!")
                    value = 2140000000
                if counter>0:
                    sql += ','
                sql += f"('{formatted_dt}', {self.id}, {self.parentid}, {value}, '{self.region_alias}', '{self.device_alias}', '{self.trafsrc_alias}', {direction_val}, {self.project_id}, {self.metric_tag_id})"
                counter += 1
            counter_all += 1    
        sql += ';'
        
        logging.info(f'Add anoms in direction: {direction}; last_anom_dt: {last_anom_dt}; all anoms: {counter_all}; add anoms: {counter}')

        if counter>0:
            return self.db.insert(sql)
        else:
            return 0    

    def get_anoms(self, *, dt_from:str='', last_items:int=0, direction:str='', tz_str:str='') -> pd.Series:
        sql = f"SELECT dt, metric_value, posted from {self.anoms_table}{self.granularity} where \
                metric_id={self.id} and metric_project_id={self.project_id} and metric_tag_id={self.metric_tag_id}"
        if dt_from:
            sql += f" and dt>='{dt_from}'"
        if direction=='pos':
            direction_val = 1
        if direction=='neg':
            direction_val = -1
        else:       
            direction_val = 0    
        if direction!=0:
            sql += f" and direction='{direction}'"    
        if last_items:
            if dt_from:
                sql += f" LIMIT 0,{last_items}"
            else:
                sql += f" ORDER BY dt DESC LIMIT 0,{last_items}"
        sql += ';'
        result = self.db.query(sql)   
        if last_items and not dt_from:
            result.reverse()

        pd_index = []
        pd_val = []
        for row in result: 
            value = row['metric_value']/(10**self.dp)
            pd_index.append(SysBf.tzdt(row['dt'], tz_str))
            pd_val.append(value)
        return  pd.Series(pd_val, index=pd_index)  

    def get_actual_anom(self, *, message_dt_lag_sec:int=86400, tz_str:str='') -> dict:
        dt_start = SysBf.tzdt(datetime.datetime.now() - datetime.timedelta(seconds=message_dt_lag_sec), tz_str)

        direction = None
        formatted_dt_start = str(dt_start)
        sql = f"SELECT id, dt, metric_value, direction, posted from {self.anoms_table}{self.granularity} where \
                dt>'{formatted_dt_start}' \
                and metric_id={self.id}  and metric_project_id={self.project_id} and metric_tag_id={self.metric_tag_id} \
                and posted > 0 \
                ORDER BY dt LIMIT 0,1;"
        
        result = self.db.query(sql) 
        if result:
            direction = result[0]['direction']

        dt_start2 = SysBf.tzdt(datetime.datetime.now() - datetime.timedelta(seconds=10800), tz_str) # За последние 3 часа
        formatted_dt_start2 = str(dt_start2)
        sql = f"SELECT id, dt, metric_value, direction, posted from {self.anoms_table}{self.granularity} where \
                dt>'{formatted_dt_start2}' \
                and metric_id={self.id} and metric_project_id={self.project_id} and metric_tag_id={self.metric_tag_id} \
                and posted = 0 \
                ORDER BY dt DESC;"
        
        result = self.db.query(sql) 
        if result:
            for row in result:
                if direction is None or (row['direction']!=direction):
                    return {
                        "id": row["id"],
                        "dt": SysBf.tzdt(row["dt"], tz_str),
                        "direction": row["direction"]
                    }
        return None

    def set_anom_posted(self, anom_id:int)-> int:
        anom_id = int(anom_id)
        sql = f"UPDATE {self.anoms_table}{self.granularity} set posted=1 WHERE id={anom_id};"
        return self.db.update(sql)

    @staticmethod
    def truncate_anoms(*, db:Mysqldb, granularity:str='') -> int:
        if granularity=='':
            return False
        return db.delete(f"TRUNCATE TABLE {Metric.anoms_table}{granularity};")

    @staticmethod
    def truncate_values(*, db:Mysqldb, granularity:str='') -> int:
        if granularity=='':
            return False
        return db.delete(f"TRUNCATE TABLE {Metric.data_table}{granularity};")
    
        
    @staticmethod
    def add_fr_ym(*, db:Mysqldb,
                  metrics:dict, 
                  granularity:str, granularity_settings:dict, 
                  source_id:int,
                  upd_metric:str, 
                  project_id:int=0, 
                  metric_tag_id:int=0, 
                  upd_metric_vals:list, upd_metric_time_intervals:list,
                  tz_str_source:str='', tz_str_system:str='',
                  mode:str='prod',
                  datetime_to:str='',
                  onlyinsert:bool=False,
                  first_item_enable:bool=False):

        insert_counter_all = 0
        upd_counter_all = 0
        if datetime_to!='':
            datetime_add_to = SysBf.tzdt_fr_str(datetime_to, tz_str_system)
        else:  
            datetime_add_to = SysBf.tzdt(datetime.datetime.now(), tz_str_system)
        
        # Определим datetime до которого (не включая) будут записываться данные в базу
        if granularity=='m1':
            datetime_add_to = datetime_add_to.replace(second=0, microsecond=0)
        if granularity=='h1':
            datetime_add_to = datetime_add_to.replace(minute=0, second=0, microsecond=0)
        if granularity=='d1':
            datetime_add_to = datetime_add_to.replace(hour=0, minute=0, second=0, microsecond=0)
        if granularity=='w1':
            datetime_add_to = datetime_add_to - datetime.timedelta(days=datetime_add_to.weekday())
            datetime_add_to = datetime_add_to.replace(hour=0, minute=0, second=0, microsecond=0)
        if granularity=='mo1':
            datetime_add_to = datetime_add_to.replace(day=1, hour=0, minute=0, second=0, microsecond=0)            

        mcounter = 0
        upd_counter = 0
        ins_mt = []
        for itemKey, updValue in enumerate(upd_metric_vals):
            mcounter+=1
            if not first_item_enable and mcounter==1: 
                continue; # Первое значение обычно обрезанное, по умолчанию его не учитываем

            tsStr1 = upd_metric_time_intervals[itemKey][0] # Начальная дата интервала, иногда со временем "2024-09-15 00:00:00"
            real_value = round(updValue*(10**int(metrics[upd_metric]['metric_dp'])))
            cur_item_dt = SysBf.tzdt_fr_str(tsStr1, tz_str_source) # $curItemTs
            cur_item_dt_str = str(cur_item_dt) # datetime.strftime(cur_item_dt,'%Y-%m-%d %H:%M:%S') #$curItemDate

            # Проапдейтем несколько последних метрик
            upd_max_dt = SysBf.tzdt_fr_str('', tz_str_system)
            if metrics.get(upd_metric,False).get('max_dt',False):
                upd_max_dt = metrics[upd_metric]['max_dt']
            start_dt = SysBf.tzdt_fr_str('', tz_str_system)
            start_dt_exist = False

            if upd_max_dt.timestamp() > granularity_settings['update_ts_lag']:
                start_dt = upd_max_dt - datetime.timedelta(seconds=granularity_settings['update_ts_lag'])
                start_dt_exist = True
            if onlyinsert and start_dt_exist and cur_item_dt > start_dt and cur_item_dt<=upd_max_dt: # Есть что обновлять и это разрешено (onlyinsert=True)
                if mode=="prod": 
                    Metric.stupdateval(db=db, 
                                    granularity=granularity, 
                                    metric_id=metrics[upd_metric]['id'], 
                                    metric_dt = cur_item_dt,
                                    project_id=project_id, metric_tag_id=metric_tag_id, 
                                    params={"value": real_value, "dp": metrics[upd_metric]['metric_dp']})
                logging.info(f"Update {granularity}.[{metrics[upd_metric]['id']}.{metrics[upd_metric]['metric_alias']}.{project_id}.{metric_tag_id}: [{cur_item_dt_str}] = {real_value}")
                upd_counter += 1
                continue

            # Если не апдейт, то соберем пачку на добавление - дата до (не включая начала текущего часа) 
            if cur_item_dt > start_dt and cur_item_dt<datetime_add_to:
                ins_mt.append({
                    "dt": cur_item_dt_str, 
                    "source_id": source_id, 
                    "metric_id": metrics[upd_metric]['id'],  
                    "metric_parentid": metrics[upd_metric]['parentid'], 
                    "metric_project_id": project_id,
                    "metric_tag_id": metric_tag_id,
                    "value": real_value, 
                    "dp": metrics[upd_metric]['metric_dp']
                })
                logging.info(f"Insert {granularity}.{metrics[upd_metric]['id']}.{metrics[upd_metric]['metric_alias']}.{project_id}.{metric_tag_id}: [{cur_item_dt_str}] = {real_value}")

        # Если есть, что добавлять, добавляем
        if len(ins_mt):
            if mode=="prod":
                Metric.insert_list(db=db, granularity=granularity, params=ins_mt)
            logging.info(f"Insert {granularity}.{metrics[upd_metric]['id']}.{metrics[upd_metric]['metric_alias']}.{project_id}.{metric_tag_id}: Complete "+str(len(ins_mt))+" items!")
            insert_counter_all += len(ins_mt)
        if upd_counter>0:
            logging.info(f"Update {granularity}.{metrics[upd_metric]['id']}.{metrics[upd_metric]['metric_alias']}.{project_id}.{metric_tag_id}: Complete "+str(upd_counter)+" items!")
            upd_counter_all += upd_counter    

        return {'insert_counter_all': insert_counter_all, 'upd_counter_all': upd_counter_all}    