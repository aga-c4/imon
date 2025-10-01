import time
from datetime import date, timedelta, datetime
import logging
import os.path
import json
import re

from models.mysqldb import Mysqldb
from models.metric import Metric
from models.systimer import SysTimer
from models.yamapi import YaMAPI
from models.sysbf import SysBf

class Robot_mgen:
    "Сбор данных с Я.Метрики управление с параметров и из конфига"

    alias = 'mgen'
    settings = {}
    config = {}
    db = None
    tmp_path = 'tmp/yamget'
    proc_path = 'tmp/process'
    proc_ttl = 2 * 60 * 60 
    debug = False
    pid = ''
    tz_str_system = ''
    tz_str_db = ''
    comment_str = ''
    db_mode = 'prod' # prod - для реальной записи
    all_gran_list = ["m1","h1", "d1", "w1", "mo1"]
    add_gran_list = ["h1", "d1", "w1", "mo1"]
    project_id = 0

    """
    Используемые параметры:
    sec - секунд в таймфрейме
    dblimit - количество дней данных, хранимых в базе.
    days_before_max - максимальное количество дней сбора данной метрики с API
    update_ts_lag - время в секундах до текущего момента для метрик, которые мы будем апдейтить перед добавлением новых. При заборе первый результат не учитываем, т.к. он не полный. Делаем запас
    get_item_lag_sec - лаг в секундах после которого необходимо забрать очередной элемент метрики. Раскидал, чтоб не сильно мешали друг другу.
    message_dt_lag_sec - отошлем сообщения о последней неповторяющейся аномалии в течении message_dt_lag_sec
    """
    granularity_list = { # Допустимые таймфреймы и их временные периоды в секундах 
        "m1": {"sec": 60, "dblimit": 30, "days_before_max": 15, "update_ts_lag": 30 * 60, "get_item_lag_sec": 10 * 60, "api_group": "hour"},
        "h1": {"sec": 60 * 60, "dblimit": 3*30, "days_before_max": 83, "update_ts_lag": 6 * 60 * 60, "get_item_lag_sec": 60 * 60, "api_group": "hour"},
        "d1": {"sec": 24 * 60 * 60, "dblimit": 3*12*30, "days_before_max": 1000, "update_ts_lag": 4 * 24 * 60 * 60, "get_item_lag_sec": 4 * 60 * 60, "api_group": "day"},
        "w1": {"sec": 7 * 24 * 60 * 60, "dblimit": 3*12*30, "days_before_max": 1000, "update_ts_lag": 15 * 24 * 60 * 60, "get_item_lag_sec": 5 * 60 * 60, "api_group": "week"},
        "mo1": {"sec": 30 * 24 * 60 * 60, "dblimit": 3*12*30, "days_before_max": 1000, "update_ts_lag": 65 * 24 * 60 * 60, "get_item_lag_sec": 6 * 60 * 60, "api_group": "month"}
    }

    def comment(self, cstr):
        if self.comment_str != '':
            fin_str = " \n" + cstr
        else:
            fin_str = cstr    
        self.comment_str += fin_str
        return cstr

    def __init__(self, *, settings:None, config:dict={}):
        def_settings = {"pid": "nopid", "granularity":"", "group_id": 0, "project_id":0, "metric_id":0, "mode": "prod"}  
        
        self.db = Mysqldb(config['db'])
        
        self.config = config
        self.settings = {key: settings.get(key, def_settings[key]) for key in def_settings}
        self.debug = self.settings.get('debug',False)
        self.settings['group_id'] = int(self.settings['group_id'])
        self.settings['project_id'] = int(self.settings['project_id'])
        self.settings['metric_id'] = int(self.settings['metric_id'])
        self.pid = str(settings.get('pid','nopid'))

        self.granularity_list = config['granularity_list']
        self.tz_str_db = config['db'].get('timezone', self.tz_str_db)
        
        if 'system' in config:
            self.tmp_path = config['system'].get('tmp_path', self.tmp_path)
            self.proc_path = config['system'].get('proc_path', self.proc_path)
            self.proc_ttl = int(config['system'].get('proc_ttl', self.proc_ttl))
            self.tz_str_system = config['system'].get('timezone', self.tz_str_system)

    @staticmethod
    def extract_m_values(formula) -> set:
        return set(re.findall(r'm(\d+)', formula))
    
    @staticmethod
    def extract_ma_values(formula) -> set:
        return set(re.findall(r'ma(\d+)', formula))

    @staticmethod
    def calculate_formula(mlist, formula) -> str:
        for i, element in mlist.items():
            formula = re.sub(fr'\b{i}\b', str(element), formula)
        try:
            res = eval(formula)
        except:
            res = None   
            logging.info(f'calculate_formula [{formula}] error!')     
        return res
    
    def run(self, *, output:bool=False) -> dict:
        run_timer = SysTimer() 
        self.comment_str = ''
        insert_counter_all = 0
        upd_counter_all = 0

        logging.info('### Generate metrics ###')

        db = self.db
        datetime_now = SysBf.tzdt(datetime.now(), self.tz_str_system)
        
        # Запрет дублирования запуска, если зависнет удалите файл!
        proc_file = f"{self.proc_path}/{self.alias}_{self.settings['pid']}.pid"
        if os.path.exists(proc_file):
            last_proc_dt_str = ''
            try:
                file = open(proc_file, 'r')
                last_proc_dt_str = file.readline()
            except:
                logging.error(f"Error openning file: {proc_file}")

            if last_proc_dt_str=='' or SysBf.tzdt_fr_str(last_proc_dt_str, self.tz_str_system) > datetime_now - timedelta(seconds=self.proc_ttl):
                logging.warning("Error: Already running or process file error!")
                return {"success": False, 
                        "telemetry": {
                            "job_execution_sec": run_timer.get_time(), 
                            "job_max_mem_kb": 0},
                        "count": 0,
                        "comment": "Error: Already running or process file error!"} 
        
        # Файл устарел или отсутствует, перезапишем
        f = open(proc_file, 'w')
        f.write(datetime_now.strftime("%Y-%m-%d %H:%M:%S"))
        f.close()

        ########################[ Робот ]##########################
        # 1. Получим список ВСЕХ метрик и для res метрик сформируем список метрик от которых они зависят
        metrics_dict = {}
        metrics = Metric.get_list(db=db)
        # Дадим метрикам ключи - Id метрик    
        for mt in metrics:
            metrics_dict[mt['id']] = mt  
        metrics = metrics_dict
        del metrics_dict

        metric_projects = Metric.get_projects(db=db)
        metric_groups = Metric.get_groups(db=db)

        # res метрики имеют формулу типа 10*m1/(m2+m3)+10 , где m - префикс метрики с идентификатором с совпадающим тегом, ma - без тега, остальное - операторы и константы
        for granularity, granularity_settings in self.granularity_list.items():
            if self.settings['granularity']!='' and self.settings['granularity']!=granularity:
                continue
            logging.info(f"granularity: {granularity}")

            # Почистим базу от лишних записей по данному варианту таймфрейма
            Metric.clear_table(db=self.db, granularity=granularity, date_to=datetime_now - timedelta(days=granularity_settings['dblimit']))
            
            for metric_project in metric_projects:
                project_id = metric_project["id"]
                if self.settings['project_id']>0 and int(self.settings['project_id'])!=project_id:
                    continue
                logging.info(f"Project: {metric_project['metric_project_name']}") 

                # Почистим данные по метрикам для нового проекта
                m_src_vals = {} # Массив значений метрик источников
                m_src_dt = {} # Массив значений метрик дат начала и конца данных
                for key, mt in metrics.items():
                    metrics[key]["tags"] = {}  

                for metric_group in metric_groups:
                    if self.settings['group_id']>0 and int(self.settings['group_id'])!=metric_group['id']:
                        continue

                    logging.info(f"Group: {metric_group['metric_group_name']}") 
                    group_id = metric_group['id']

                    # 1. Получим список метрик res и сформируем список метрик от которых они зависят
                    metric_tags = Metric.get_tags(db=db, granularity=granularity, project_id=project_id)
                    cur_res_metrics = Metric.get_list(db=db, group_id=metric_group['id'], metric_type="res")
                    for cur_tag in metric_tags:
                        if cur_tag["tag_id"] is None:
                            continue
                        # if cur_tag["tag_id"] != 110: continue
                        tag_id = cur_tag["tag_id"]
                        tag_name = cur_tag["tag"]
                        for mt in cur_res_metrics:
                            if metrics[mt['id']].get('notags', 0)==1 and tag_id!=0:
                                # По данной метрике допустим только тег All c id=0
                                continue

                            if self.settings['metric_id']>0 and self.settings['metric_id']!=mt['id']:
                                # Схема не оптимальная, но оставим пока так
                                continue
   
                            metrics[mt['id']]["tags"][tag_id] = Metric.get_minmax_dt(db=self.db, 
                                                                            granularity=granularity, 
                                                                            metric_id=int(mt['id']), 
                                                                            project_id=project_id, metric_tag_id=tag_id,
                                                                            tz_str=self.tz_str_db)

                            # Получим исходные метрики для расчета
                            if mt['metric_modification']=='':
                                metrics[mt['id']]['metric_modification'] = 0
                                metrics[mt['id']]['metric_modification_set'] = set()
                                metrics[mt['id']]['metric_modification_set_ma'] = set()
                                continue
                            else:    
                                metrics[mt['id']]['metric_modification_set'] = Robot_mgen.extract_m_values(mt['metric_modification'])
                                metrics[mt['id']]['metric_modification_set_ma'] = Robot_mgen.extract_ma_values(mt['metric_modification'])

                            # Для исходных метрик при необходимости заберем даты начала и конца
                            cur_mindt = None # Начальная начальная возможная дата генерации
                            cur_maxdt = None # Начальная конечная возможная дата генерации
                            for smt in metrics[mt['id']]['metric_modification_set']:
                                smt = int(smt) 
                                if smt in metrics and (not tag_id in metrics[smt]["tags"] or not 'mindt' in metrics[smt]["tags"][tag_id]): 
                                    metrics[smt]["tags"][tag_id] = Metric.get_minmax_dt(db=self.db, 
                                                                            granularity=granularity, 
                                                                            metric_id=int(smt), 
                                                                            project_id=project_id, metric_tag_id=tag_id,
                                                                            tz_str=self.tz_str_db)
                                if not metrics[smt]["tags"][tag_id]['mindt'] is None:
                                    if cur_mindt is None or metrics[mt['id']]["tags"][tag_id]['mindt'] is None:
                                        cur_mindt = metrics[smt]["tags"][tag_id]['mindt']
                                    elif metrics[smt]["tags"][tag_id]['mindt'] > cur_mindt:
                                        cur_mindt = metrics[smt]["tags"][tag_id]['mindt']  
                                if not metrics[smt]["tags"][tag_id]['maxdt'] is None:           
                                    if cur_maxdt is None or metrics[mt['id']]["tags"][tag_id]['maxdt'] is None:
                                        cur_maxdt = metrics[smt]["tags"][tag_id]['maxdt']
                                    elif metrics[smt]["tags"][tag_id]['maxdt'] < cur_maxdt:
                                        cur_maxdt = metrics[smt]["tags"][tag_id]['maxdt']             

                            for smt in metrics[mt['id']]['metric_modification_set_ma']:
                                smt = int(smt)
                                if smt in metrics and (not tag_id in metrics[smt]["tags"] or not 'mindt' in metrics[smt]["tags"][0]):
                                    metrics[smt]["tags"][0] = Metric.get_minmax_dt(db=self.db, 
                                                                            granularity=granularity, 
                                                                            metric_id=int(smt), 
                                                                            project_id=project_id, metric_tag_id=0,
                                                                            tz_str=self.tz_str_db)                    
                                if not metrics[smt]["tags"][0]['mindt'] is None:
                                    if cur_mindt is None or metrics[mt['id']]["tags"][0]['mindt'] is None:
                                        cur_mindt = metrics[smt]["tags"][0]['mindt']
                                    elif metrics[smt]["tags"][0]['mindt'] > cur_mindt:
                                        cur_mindt = metrics[smt]["tags"][0]['mindt']  
                                if not metrics[smt]["tags"][0]['maxdt'] is None:           
                                    if cur_maxdt is None or metrics[mt['id']]["tags"][0]['maxdt'] is None:
                                        cur_maxdt = metrics[smt]["tags"][0]['maxdt']
                                    elif metrics[smt]["tags"][0]['maxdt'] < cur_maxdt:
                                        cur_maxdt = metrics[smt]["tags"][0]['maxdt']              

                            if cur_mindt is None or cur_maxdt is None:
                                logging.info(f"Calculate {granularity}.{project_id}.{group_id}.{mt['id']}.{mt['metric_alias']}.{tag_name}: There is not enough data!")
                                continue 

                            if tag_id in metrics[mt['id']]["tags"] \
                                and not metrics[mt['id']]["tags"][tag_id]['mindt'] is None and cur_maxdt <= metrics[mt['id']]["tags"][tag_id]['mindt']:
                                logging.info(f"Calculate {granularity}.{project_id}.{group_id}.{mt['id']}.{mt['metric_alias']}.{tag_name}: Already calculated!")
                                continue  

                            if 0 in metrics[mt['id']]["tags"] \
                                and not metrics[mt['id']]["tags"][0]['mindt'] is None and cur_maxdt <= metrics[mt['id']]["tags"][0]['mindt']:
                                logging.info(f"Calculate {granularity}.{project_id}.{group_id}.{mt['id']}.{mt['metric_alias']}.{tag_name}: Already calculated!")
                                continue 

                            dt_start_gen = cur_mindt # Начальная реальная дата, после которой начнется генерация
                            dt_start_ins = cur_mindt # Начальная реальная дата, после которой начнется генерация (инсерт) НЕ включая ее!!!
                            dt_fin_gen = cur_maxdt # Конечная реальная дата, после которой закончится генерация

                            all_insert = True
                            if tag_id in metrics[mt['id']]["tags"] and 'maxdt' in metrics[mt['id']]["tags"][tag_id]: 
                                if metrics[mt['id']]["tags"][tag_id].get('maxdt', False):  
                                    all_insert = False
                                    dt_start_gen = metrics[mt['id']]["tags"][tag_id]['maxdt'] - timedelta(seconds=granularity_settings['update_ts_lag'])
                                    if dt_start_gen < cur_mindt:
                                        dt_start_gen = cur_mindt
                                    if dt_start_ins <= metrics[mt['id']]["tags"][tag_id]['maxdt']:
                                        dt_start_ins = metrics[mt['id']]["tags"][tag_id]['maxdt']

                            # print("dt_start_gen:", dt_start_gen, " dt_start_ins:", dt_start_ins, " dt_fin_gen:", dt_fin_gen)       
                            
                            # Пройдем по метрикам src, в реалтайме заберем данные по нужным источникам, 
                            for smt in metrics[mt['id']]['metric_modification_set']:
                                smt = int(smt)
                                if not m_src_dt.get(smt, False) or not m_src_dt[smt].get(tag_id, False) \
                                    or m_src_dt[smt][tag_id]["mindt"]>dt_start_gen or m_src_dt[smt][tag_id]["maxdt"]<cur_maxdt:
                                    
                                    # Требуется перегенерации ряда источника
                                    if not smt in m_src_dt:
                                        m_src_dt[smt] = {}    
                                        m_src_vals[smt] = {}    
                                        m_src_vals[smt][tag_id] = {} 
                                    if not tag_id in m_src_dt[smt]:
                                        m_src_dt[smt][tag_id] = {"mindt": None, "maxdt": None}       
                                    m_src_dt[smt][tag_id]["mindt"] = dt_start_gen
                                    m_src_dt[smt][tag_id]["maxdt"] = cur_maxdt                                  
                                    m_src_vals[smt][tag_id] = Metric.get_values(db=db, 
                                                                granularity=granularity, 
                                                                dt_from=dt_start_gen.strftime("%Y-%m-%d %H:%M:%S"), 
                                                                dt_to=dt_fin_gen.strftime("%Y-%m-%d %H:%M:%S"), 
                                                                project_id=project_id, metric_tag_id=tag_id,
                                                                metric_id=smt)
                                    
                            for smt in metrics[mt['id']]['metric_modification_set_ma']:
                                smt = int(smt)
                                if not m_src_dt.get(smt, False) or not m_src_dt[smt].get(tag_id, False) \
                                    or m_src_dt[smt][0]["mindt"]>dt_start_gen or m_src_dt[smt][0]["maxdt"]<cur_maxdt:
                                    # Требуется перегенерации ряда источника
                                    if not smt in m_src_dt:
                                        m_src_dt[smt] = {}    
                                        m_src_vals[smt] = {}
                                        m_src_vals[smt][0] = {} 
                                    if not tag_id in m_src_dt[smt]:
                                        m_src_dt[smt][tag_id] = {"mindt": None, "maxdt": None}               
                                    m_src_dt[smt][0]["mindt"] = dt_start_gen
                                    m_src_dt[smt][0]["maxdt"] = cur_maxdt                                  
                                    m_src_vals[smt][0] = Metric.get_values(db=db, 
                                                                granularity=granularity, 
                                                                dt_from=dt_start_gen.strftime("%Y-%m-%d %H:%M:%S"), 
                                                                dt_to=dt_fin_gen.strftime("%Y-%m-%d %H:%M:%S"), 
                                                                project_id=project_id, metric_tag_id=0,
                                                                metric_id=smt)        
                                    
                            # Рассчитаем значение res метрики, запишем.
                            mlist_src_vals={}
                            for smt in metrics[mt['id']]['metric_modification_set']:
                                smt = int(smt)
                                for smt_dt, smt_val in m_src_vals[smt][tag_id].items():
                                    # Тут smt_dt без зоны
                                    if not smt_dt in mlist_src_vals:
                                        mlist_src_vals[smt_dt] = {}    
                                    mlist_src_vals[smt_dt][f"m{smt}"] = smt_val
                            for smt in metrics[mt['id']]['metric_modification_set_ma']:
                                smt = int(smt)
                                for smt_dt, smt_val in m_src_vals[smt][0].items():
                                    # Тут smt_dt без зоны
                                    if not smt_dt in mlist_src_vals:
                                        mlist_src_vals[smt_dt] = {}    
                                    mlist_src_vals[smt_dt][f"ma{smt}"] = smt_val        
                            
                            ins_mt = []
                            insert_counter = 0
                            upd_counter = 0
                            for mlist_dt, mlist in mlist_src_vals.items():
                                mlist_dt = SysBf.tzdt(mlist_dt, self.tz_str_db)
                                # mlist_dt = SysBf.tzdt_fr_str(mlist_dt_str, tz_str) # Нужно, если ключи не объекты detetime
                                mlist_dt_str = str(mlist_dt) # mlist_dt.strftime("%Y-%m-%d %H:%M:%S")
                                if mlist_dt >= dt_start_gen and mlist_dt <= dt_fin_gen: 
                                    value = Robot_mgen.calculate_formula(mlist, metrics[mt['id']]['metric_modification'])
                                    if value is None:
                                        continue
                                    real_value = round(value*(10**int(mt['metric_dp'])))
                                    round_value = round(value, mt['metric_dp'])

                                    
                                    if granularity_settings['update_ts_lag']>0 and mlist_dt >= dt_start_gen and mlist_dt <= dt_start_ins: 
                                        # Есть что обновлять 
                                        if self.settings["mode"]=="prod": 
                                            Metric.stupdateval(db=self.db, 
                                                            granularity=granularity, 
                                                            metric_id=mt['id'], 
                                                            metric_dt = mlist_dt,
                                                            project_id=self.project_id,
                                                            metric_tag_id=tag_id,
                                                            params={"value": real_value, "dp": mt['metric_dp']})
                                        logging.info(f"Update {granularity}.{project_id}.{group_id}.{mt['id']}.{mt['metric_alias']}: [{mlist_dt_str}] = {round_value}")
                                        upd_counter += 1
                                        continue

                                    if all_insert or mlist_dt > dt_start_ins:
                                        ins_mt.append({
                                            "dt": mlist_dt_str, 
                                            "source_id": 0, 
                                            "metric_id": mt['id'], 
                                            "metric_parentid": mt['parentid'], 
                                            "metric_tag_id": tag_id,
                                            "value": real_value, 
                                            "dp": mt['metric_dp'], 
                                            "metric_project_id": project_id
                                        })
                                        logging.info(f"Insert {granularity}.{project_id}.{group_id}.{mt['id']}.{mt['metric_alias']}.{tag_name}: [{mlist_dt_str}] = {round_value}")
                                        insert_counter += len(ins_mt)
                            # Если есть, что добавлять, добавляем
                            if len(ins_mt):
                                if self.settings["mode"]=="prod":
                                    Metric.insert_list(db=self.db, granularity=granularity, params=ins_mt)
                                logging.info(f"Insert {granularity}.{project_id}.{group_id}.{mt['id']}.{mt['metric_alias']}.{tag_name}: Complete "+str(len(ins_mt))+" items!")
                                insert_counter_all += insert_counter
                            if upd_counter:
                                logging.info(f"Update {granularity}.{project_id}.{group_id}.{mt['id']}.{mt['metric_alias']}.{tag_name}: Complete "+str(upd_counter)+" items!")
                                upd_counter_all += upd_counter 

                            # Актуализируем данные по измененной метрике       
                            metrics[mt['id']]["tags"][tag_id] = Metric.get_minmax_dt(db=self.db, 
                                                                            granularity=granularity, 
                                                                            metric_id=int(mt['id']), 
                                                                            project_id=project_id, metric_tag_id=tag_id,
                                                                            tz_str=self.tz_str_db)    

                logging.info(f"Finish {granularity}::{metric_group['metric_group_alias']}::{mt['metric_alias']}")


        ########################[ /Робот ]##########################

        # Удалим блокирующий запуск файл
        os.remove(proc_file)

        self.comment(f"Update: {upd_counter_all}; Insert:{insert_counter_all}")
        return {"success": True, 
                      "telemetry": {
                          "job_execution_sec": run_timer.get_time(), 
                          "job_max_mem_kb": SysBf.get_max_memory_usage()},
                      "count": insert_counter_all + upd_counter_all,
                      "comment": self.comment_str} 
        