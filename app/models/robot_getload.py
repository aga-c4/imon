import time
from datetime import timedelta, datetime
import logging
import os.path
import csv  

from models.mysqldb import Mysqldb
from models.metric import Metric
from models.systimer import SysTimer
from models.getloadapi import GetLoadAPI
from models.sysbf import SysBf

class Robot_getload:
    "Сбор данных с Я.Метрики управление с параметров и из конфига"

    metrics_pkg_qty = 1 # Количество метрик в пачке
    source_id = 0
    source_alias = ''
    alias = 'getload'
    settings = {}
    config = {}
    comment_str = ''
    db = None
    tmp_path = 'tmp/srcget'
    proc_path = 'tmp/process'
    proc_ttl = 2 * 60 * 60 
    debug = False
    pid = ''
    source_get_api_lag_sec = 1 # Задержка между запросами к API
    api = None
    fr_api = False
    tz_str_source = ''
    tz_str_system = ''
    tz_str_db = ''

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
        def_settings = {"pid": "nopid", "fr_api": False, "source": "", "granularity":"", "group_id": 0, "metric_id":0, "mode": "prod", "datetime_to": ""}  
        
        self.db = Mysqldb(config['db'])
        
        self.config = config
        self.settings = {key: settings.get(key, def_settings[key]) for key in def_settings}
        self.debug = self.settings.get('debug',False)
        self.settings['group_id'] = int(self.settings['group_id'])
        self.settings['metric_id'] = int(self.settings['metric_id'])
        self.pid = str(settings.get('pid','nopid'))
        self.source_alias = self.settings['source']

        self.granularity_list = config['granularity_list']
        self.tz_str_db = config['db'].get('timezone', self.tz_str_db)
        
        if 'system' in config:
            self.proc_path = config['system'].get('proc_path', self.proc_path)
            self.proc_ttl = int(config['system'].get('proc_ttl', self.proc_ttl))
            self.tz_str_system = config['system'].get('timezone', self.tz_str_system)

        if 'sources' in config:
            self.tmp_path = config['sources'][self.source_alias].get('tmp_path', self.tmp_path)
            self.source_id = config['sources'][self.source_alias]['id']
            self.metrics_pkg_qty = int(config['sources'][self.source_alias].get('metrics_pkg_qty', self.metrics_pkg_qty))
            self.source_get_api_lag_sec = int(config['sources'][self.source_alias].get('source_get_api_lag_sec', self.source_get_api_lag_sec))
            self.tz_str_source = config['sources'][self.source_alias].get('timezone', self.tz_str_source)
            self.api = GetLoadAPI(token=config['sources'][self.source_alias]['token'], 
                            api_url=config['sources'][self.source_alias]['api_url'], 
                            source=self.settings['source'], tmp_path=self.tmp_path)
            
        
    def run(self, *, output:bool=False) -> dict:
        run_timer = SysTimer() 
        self.comment_str = ''
        insert_counter_all = 0
        upd_counter_all = 0

        db = self.db
        source_id = self.source_id
        source_alias = self.source_alias
        datetime_now = SysBf.tzdt(datetime.now(), self.tz_str_system)
        if self.settings['datetime_to']!='':
            datetime_to = SysBf.tzdt_fr_str(self.settings['datetime_to'], self.tz_str_system)
        else:
            datetime_to = datetime_now
        
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

        granularity = "m1"
        granularity_settings = self.granularity_list.get(granularity, {})
        logging.info(f"granularity: {granularity}")

        # Почистим базу от лишних записей по данному варианту таймфрейма
        Metric.clear_table(db=self.db, granularity=granularity, date_to=datetime_now - timedelta(days=granularity_settings['dblimit']))

        metrics_dict = {}
        metrics = Metric.get_list(db=db, source_alias=source_alias, metric_type="src")
        # Дадим метрикам ключи - API алиасы метрик    
        for mt in metrics:
            # if not mt['id'] in [10, 11]: # TODO - Отрубить после теста. Для теста пачки или там, где нужны ограничения по метрикам
            #    continue

            if self.settings['metric_id']>0 and self.settings['metric_id']!=mt['id']:
                continue

            metrics_dict[mt['metric_api_alias']] = mt
        metrics = metrics_dict
        del metrics_dict

        # Получить дату последних данных в базе
        max_dt = Metric.get_last_dt(db=db, granularity=granularity, tz_str=self.tz_str_db, source_alias=self.source_alias)
        max_dt_str = max_dt.strftime("%Y-%m-%dT%H")
        
        # Сформируем дату до которой будем искать данные
        end_dt_str = datetime_to.strftime("%Y-%m-%d")+'T00'

        # Получить список доступных архивов
        file_list = self.api.get_list()
        
        if file_list!=False and len(file_list)>0:
            for dt_file in file_list:
                if dt_file>max_dt_str and dt_file<end_dt_str:
                    logging.info(f'API start get {dt_file}')
                    # Забрать архивы по одному, при этом делая что ниже
                    api_timer_sec = 0
                    api_timer = SysTimer()
                    minute_file_list = self.api.get_files(file=dt_file, fr_api=self.fr_api)

                    # Пройтись по минутам, открыть файлы, записать данные в базу данных с тегами, записать суммарные данные без тега  
                    if minute_file_list!=False and type(minute_file_list) is list:    
                        for minute_file in minute_file_list:
                            with open(minute_file, 'r') as file:  
                                reader = csv.reader(file)  
                                for row in reader:  
                                    
                                    print(type(row), row)
                                    continue  
                                    upd_metric="" # API алиас изменяемой метрики
                                    upd_metric_vals_list = []
                                    upd_metric_ts_list = []

                                    res = Metric.add_fr_ym(db=db,
                                                metrics=metrics, # Словарь метрик с их параметрами
                                                granularity=granularity, granularity_settings=granularity_settings, 
                                                source_id=source_id, source_alias=source_alias,
                                                tz_str_source=self.tz_str_source, tz_str_system=self.tz_str_system,
                                                upd_metric=upd_metric, # API алиас изменяемой метрики
                                                upd_metric_vals=upd_metric_vals_list, # Список добавляемых значений метрики
                                                upd_metric_time_intervals=upd_metric_ts_list, # Список интервалов добавляемых элементов
                                                mode='dev', # prod
                                                datetime_to=self.settings['datetime_to'],
                                                onlyinsert=True)  
                                    insert_counter_all += res['insert_counter_all']
                                    upd_counter_all += res['upd_counter_all']   
                                break       
                    
                    api_timer_sec = api_timer.get_time()
                    if api_timer_sec<self.source_get_api_lag_sec: 
                        # Обеспечение минимального перерыва между запросами TODO - далее брать лаг из базы.
                        time.sleep(self.source_get_api_lag_sec - api_timer_sec)
                    logging.info(f'API complite get {dt_file}')

                    break

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
        