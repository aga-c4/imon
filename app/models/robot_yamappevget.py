import time
from datetime import date, timedelta, datetime
import logging
import os.path
import json

from models.mysqldb import Mysqldb
from models.metric import Metric
from models.systimer import SysTimer
from models.yamapi import YaMAPI
from models.sysbf import SysBf

class Robot_yamappevget:
    "Сбор данных с Я.Метрики управление с параметров и из конфига"

    metric_alias:str ="ym:ce2:allEvents"
    dimension:str = "ym:ce2:eventLabel"
    filter_env:str = "eventLabel"
    metrics_pkg_qty = 1 # Количество метрик в пачке
    source_id = 0
    source_alias = ''
    alias = 'yamappevget'
    settings = {}
    config = {}
    comment_str = ''
    db = None
    tmp_path = 'tmp/yamappget'
    proc_path = 'tmp/process'
    proc_ttl = 2 * 60 * 60 
    debug = False
    sample_metric_ids = [] # Идентификаторы метрик, которые семплируем
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
            self.sample_metric_ids = config['sources'][self.source_alias].get('sample_metric_ids', self.sample_metric_ids)
            self.tz_str_source = config['sources'][self.source_alias].get('timezone', self.tz_str_source)
            self.api = YaMAPI(token=config['sources'][self.source_alias]['token'], 
                            counter_ids=config['sources'][self.source_alias]['counter_ids'], 
                            type=self.settings['source'])
            
        
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

        for granularity, granularity_settings in self.granularity_list.items():
            if self.settings['granularity']!='' and self.settings['granularity']!=granularity:
                continue
            logging.info(f"granularity: {granularity}")

            # Почистим базу от лишних записей по данному варианту таймфрейма
            Metric.clear_table(db=self.db, granularity=granularity, date_to=SysBf.tzdt(datetime_now - timedelta(days=granularity_settings['dblimit']), self.tz_str_system), tz_str_db=self.tz_str_db)

            # Получим группы метрик из базы
            metric_groups = Metric.get_groups(db=db)
            for metric_group in metric_groups:
                if self.settings['group_id']>0 and int(self.settings['group_id'])!=metric_group['id']:
                    continue

                logging.info(f"Group: {metric_group['metric_group_name']}")    

                metrics_dict = {}
                metrics = Metric.get_list(db=db, source_alias=source_alias, group_id=metric_group['id'], metric_type="src", order='accuracy')
                last_metric = ''
                # Дадим метрикам ключи - API алиасы метрик    
                for mt in metrics:
                    # if not mt['id'] in [10, 11]: # TODO - Отрубить после теста. Для теста пачки или там, где нужны ограничения по метрикам
                    #    continue

                    if self.settings['metric_id']>0 and self.settings['metric_id']!=mt['id']:
                        continue
                    metrics_dict[mt['metric_api_alias']] = mt
                    last_metric = mt['metric_api_alias']
                metrics = metrics_dict
                del metrics_dict

                counter = 0
                metrics_str = ''
                metrics_fstr = ''
                min_max_dt = None

                for metric_api_alias, metric in metrics.items():
                    metrics_str += (',' if metrics_str!='' else '') + "'" + metric['metric_api_alias'] + "'"
                    metrics_fstr += '_m' + str(metric['id'])

                    # Дата-время последнего значения метики в БД
                    max_dt = Metric.get_last_dt(db=db, granularity=granularity, id=int(metric['id']), tz_str_db=self.tz_str_db)
                    metrics[metric_api_alias]['max_dt'] = max_dt

                    if max_dt > datetime_to:
                        continue

                    # Минимальная последняя дата метрик из пачки, надо для формирования начальной даты забора через API
                    if min_max_dt is None:
                        min_max_dt = max_dt
                    elif min_max_dt > max_dt: 
                        min_max_dt = max_dt

                    counter += 1
                    if metric['accuracy']<1 or counter >= self.metrics_pkg_qty or metric_api_alias == last_metric: # Пачку собрали, обрабатываем
                        counter = 0
                        start_dt = min_max_dt - timedelta(seconds=granularity_settings['update_ts_lag'])
                        min_start_dt = datetime_now - timedelta(seconds=granularity_settings['days_before_max'] * 24 * 60 * 60)
                        real_start_dt = start_dt if start_dt > min_start_dt else min_start_dt 
                        start_dt_str = real_start_dt.strftime("%Y-%m-%d")

                        if granularity=='h1':
                            end_date = datetime_to.strftime("%Y-%m-%d")
                            end_date_f = datetime_to.strftime("%Y-%m-%d-%H")
                        else:
                            end_date = (datetime_to - timedelta(days=1)).strftime("%Y-%m-%d")
                            end_date_f = (datetime_to - timedelta(days=1)).strftime("%Y-%m-%d")

                        params = {
                            'metrics': self.metric_alias,
                            'dimensions': self.dimension,
                            'filters': f"{self.filter_env}=.({metrics_str})",
                            'date1': start_dt_str,
                            'group': granularity_settings['api_group']
                        }

                        # Если необходимо, то будем семплировать данные
                        if (granularity=='h1' or granularity=='m1') and metric['accuracy']<1:
                            params['accuracy'] = metric['accuracy']
                        else: 
                            params['accuracy'] = 'full'

                        # Все кроме часов собираем до вчерашнего дня
                        if granularity!='h1' and granularity!='m1':
                            params['date2'] = end_date

                        filename = self.tmp_path + '/ym_' + source_alias + '_' + granularity + metrics_fstr + '_' + start_dt_str + '_' + end_date_f + '.json'
                
                        api_timer_sec = 0
                        if not self.fr_api and not os.path.exists(filename): # Принудительный забор или еще не забирали и нет файла, то и кладем в файл
                            logging.info(f'API start get to: {filename}')
                            api_timer = SysTimer()
                            response = self.api.get_report(method='/bytime', params=params, fileto=filename)
                            api_timer_sec = api_timer.get_time()
                            if api_timer_sec<self.source_get_api_lag_sec: 
                                # Обеспечение минимального перерыва между запросами TODO - далее брать лаг из базы.
                                time.sleep(self.source_get_api_lag_sec - api_timer_sec)
                            logging.info(f'API complite get to: {filename}')

                        if not os.path.exists(filename):
                            logging.error(self.comment(f"Load file Error: {filename} not found!"))
                        else:    
                            logging.info(f'Load metrics from: {filename}')
                            with open(filename, "r") as read_it:
                                result = json.load(read_it)    
                                if not type(result) is dict or not 'data' in result:
                                    logging.error(self.comment(f"{granularity}.m_ids({metrics_str}): API code [{result['code']}] Message: {result['message']}"))
                                    if result.get('errors', False):
                                        logging.error(self.comment(f'{granularity}.m_ids({metrics_str}): API Errors:'))
                                        for error in result['errors']:
                                            logging.error(self.comment(f"{granularity}.m_ids({metrics_str}):error_type: {error['error_type']}; error_message: {error['message']}"))
                                else:
                                    # Обработка файла, формирование записей по метрикам в БД
                                    
                                    # Предупреждение о семплировании в лог, возможно будем вообще останавливать процесс.
                                    if result.get('sampled', False):  
                                        logging.info(self.comment(f"{granularity}.m_ids({metrics_str}): API SAMPLED result. sample_share: {result['sample_share']}"))

                                    for curdims_dict in result['data']:
                                        res = Metric.add_fr_ym(db=db,
                                                        metrics=metrics, 
                                                        granularity=granularity, granularity_settings=granularity_settings, 
                                                        source_id=source_id, source_alias=source_alias,
                                                        tz_str_source=self.tz_str_source, tz_str_system=self.tz_str_system,
                                                        upd_metric=curdims_dict['dimensions'][0]['name'], 
                                                        upd_metric_vals=curdims_dict['metrics'][0], 
                                                        upd_metric_time_intervals=result['time_intervals'],
                                                        mode='prod',
                                                        datetime_to=self.settings['datetime_to'])
                                        insert_counter_all += res['insert_counter_all']
                                        upd_counter_all += res['upd_counter_all']                  

                        logging.info(f"Finish {granularity}::{metric_group['metric_group_alias']}::{metric['metric_alias']}")                            

                        # Чистим счетчики
                        metrics_str = ''
                        metrics_fstr = ''
                        min_max_dt = None 

                    # /Цикл прохода по метрикам     
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
        