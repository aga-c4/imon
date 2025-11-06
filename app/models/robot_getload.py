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
    "Сбор данных по нагрузке через API"

    """
    Тест на дубли
    SELECT mt.dt, mt.metric_tag_id, mt.metric_id, count(*) as cnt FROM `metrics_m1` mt LEFT JOIN metrics mm on mt.metric_id=mm.id WHERE mt.metric_project_id=3 and mm.metric_type='src' group by mt.metric_tag_id, mt.metric_id, mt.dt ORDER BY `cnt` DESC
    """ 

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
    db_mode = 'prod' # prod - для реальной записи
    all_gran_list = ["m1","h1", "d1", "w1", "mo1"] # От младших к старшим, Важно!
    add_gran_list = ["h1", "d1", "w1", "mo1"] # От младших к старшим, Важно!
    prev_gran_list = {"h1":"m1", "d1":"h1", "w1":"d1", "mo1":"d1"}
    project_id = 1

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
        "m1": {"sec": 60, "dblimit": 7, "days_before_max": 15, "update_ts_lag": 30 * 60, "get_item_lag_sec": 10 * 60, "api_group": "hour"},
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
        def_settings = {"pid": "nopid", "fr_api": False, "source": "", "granularity":"", "group_id": 0, "metric_id":0, "project_id":1,"mode": "prod", "datetime_to": ""}  
        self.db = Mysqldb(config['db'])
        
        self.config = config
        self.settings = {key: settings.get(key, def_settings[key]) for key in def_settings}
        self.debug = self.settings.get('debug',False)
        self.settings['group_id'] = int(self.settings['group_id'])
        self.settings['metric_id'] = int(self.settings['metric_id'])
        self.settings['project_id'] = int(self.settings['project_id'])
        self.pid = str(settings.get('pid','nopid'))
        self.source_alias = self.settings['source']
        self.project_id = self.settings['project_id']
        
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
                            source=self.settings['source'], tmp_path=self.tmp_path,
                            insecure=config['sources'][self.source_alias].get("insecure", False))
        print("Robot_getload.__init__: Ok!")
        
    def run(self, *, output:bool=False) -> dict:
        run_timer = SysTimer() 
        self.comment_str = ''
        insert_counter_all = 0
        insert_counter = {
                "m1": 0,
                "h1": 0,
                "d1": 0,
                "w1": 0,
                "mo1": 0}
        upd_counter_all = 0
        upd_counter = {
                "m1": 0,
                "h1": 0,
                "d1": 0,
                "w1": 0,
                "mo1": 0}

        db = self.db
        source_id = self.source_id
        datetime_now = SysBf.tzdt(datetime.now(), self.tz_str_system)
        if self.settings['datetime_to']!='':
            datetime_to = SysBf.tzdt_fr_str(self.settings['datetime_to'], self.tz_str_system)
        else:
            datetime_to = datetime_now   
        print("datetime_to:", str(datetime_to))

        if self.settings['project_id']>0:
            settings_project_id = int(self.settings['project_id'])
        else:
            settings_project_id = 0  
        
        # Запрет дублирования запуска, если зависнет удалите файл!
        proc_file0 = f"{self.proc_path}/{self.alias}_{self.settings['pid']}_0.pid"
        proc_file = f"{self.proc_path}/{self.alias}_{self.settings['pid']}_{settings_project_id}.pid"
        if os.path.exists(proc_file0) or os.path.exists(proc_file):
            last_proc_dt_str = ''
            last_proc_dt_str0 = ''
            if os.path.exists(proc_file0):
                try:
                    file = open(proc_file0, 'r')
                    last_proc_dt_str0 = file.readline()
                except:
                    logging.error(f"Error openning file: {proc_file0}")
            if os.path.exists(proc_file):    
                try:
                    file = open(proc_file, 'r')
                    last_proc_dt_str = file.readline()
                except:
                    logging.error(f"Error openning file: {proc_file}")
            if last_proc_dt_str0>last_proc_dt_str:
                last_proc_dt_str = last_proc_dt_str0

            if last_proc_dt_str=='' or SysBf.tzdt_fr_str(last_proc_dt_str, self.tz_str_system) > (datetime_now - timedelta(seconds=self.proc_ttl)):
                logging.warning("Error: Already running or process file error!")
                return {"success": False, 
                        "telemetry": {
                            "job_execution_sec": run_timer.get_time(), 
                            "job_max_mem_kb": 0},
                        "count": 0,
                        "comment": f"Project {settings_project_id} Error: Already running or process file error!"} 
        
        # Файл устарел или отсутствует, перезапишем
        f = open(proc_file, 'w')
        f.write(datetime_now.strftime("%Y-%m-%d %H:%M:%S"))
        f.close()

        ########################[ Робот ]##########################
        try:
            metrics_dict = {}
            metrics = Metric.get_list(db=db, metric_type="src")
            # Дадим метрикам ключи - API алиасы метрик    
            for mt in metrics:
                # if not mt['id'] in [10, 11]: # TODO - Отрубить после теста. Для теста пачки или там, где нужны ограничения по метрикам
                #    continue
                if self.settings['metric_id']>0 and self.settings['metric_id']!=mt['id']:
                    continue
                metrics_dict[mt['metric_alias']] = mt
            metrics = metrics_dict
            del metrics_dict

            # Сформируем дату до которой будем искать данные
            end_dt_source = SysBf.dt_to_tz(datetime_to, self.tz_str_source)
            end_dt_source_str = end_dt_source.strftime("%Y-%m-%dT%H")   
            cur_metric_accum = {}
            dt_insert_from = {}
            db_exist_dt = {}
            db_exist_dt_str = {}
            max_dt = SysBf.tzdt_fr_str(dt_str='1980-01-01', tz_str=self.tz_str_system)
            for gran in self.all_gran_list:
                granularity_settings = self.granularity_list.get(gran, {})
                # есть фильтр по source, т.к. помимо метрик сислоуда в системе могут быть и другие метрики, тогда важны будут их идентификаторы
                db_exist_dt[gran] = SysBf.dt_to_tz(Metric.get_last_dt(db=db, granularity=gran, tz_str_db=self.tz_str_db, project_id=self.project_id, source_id=source_id), tz_str=self.tz_str_system)
                if gran in self.prev_gran_list:
                    prev_gran = self.prev_gran_list[gran]  
                    db_first_dt_prev  = SysBf.dt_to_tz(Metric.get_first_dt(db=db, granularity=prev_gran, tz_str_db=self.tz_str_db, project_id=self.project_id, source_id=source_id), tz_str=self.tz_str_system)
                    if not db_first_dt_prev is None and db_exist_dt[gran]<db_first_dt_prev:
                        db_exist_dt[gran]=db_first_dt_prev
                        # print(f"no data, db_exist_dt[{gran}]=", db_first_dt_prev)
                db_exist_dt_str[gran] = db_exist_dt[gran].strftime("%Y-%m-%dT%H:%M:%S")  
                if db_exist_dt[gran]>max_dt:
                    max_dt = db_exist_dt[gran] 
                    # print(f"new max_dt = db_exist_dt[{gran}]=", db_exist_dt[gran] )
                Metric.clear_table(db=self.db, granularity=gran, date_to=datetime_now - timedelta(days=granularity_settings['dblimit']), tz_str_db=self.tz_str_db)
                # Ограничение по записи в базу
                dt_insert_from[gran] = (datetime_now - timedelta(days=granularity_settings["dblimit"])).strftime("%Y-%m-%d")+"T00:00:00"   
                # Очистка аккумулятора генерации вышестоящих рядов   
                cur_metric_accum[gran] = {} 
            # Получим дату последних данных в базе
            max_dt_source = SysBf.dt_to_tz(max_dt, self.tz_str_source)
            max_dt_source_str = max_dt_source.strftime("%Y-%m-%dT%H")    
            max_dt_str = max_dt.strftime("%Y-%m-%dT%H")    
            print("max_dt:", str(max_dt), " --> max_dt_str:", max_dt_str)
            cur_ts_period = SysBf.get_dateframes_by_current_dt(date=max_dt, tpl="%Y-%m-%dT%H:%M:%S")
            cur_ts_period_dt = SysBf.get_dateframes_by_current_dt(date=max_dt)
            print("cur_ts_period:", cur_ts_period)

            # Добавление старших таймфреймов в списки их сохранения
            for gran in self.add_gran_list:
                if db_exist_dt[gran]<cur_ts_period_dt[gran][0]:
                    # print(f"db_exist_dt[{gran}]:", db_exist_dt[gran])
                    # Сформируем из нижестоящих рядов недостающие значения до текущего периода
                    max_dt_bk = max_dt
                    granularity_settings = self.granularity_list.get(gran, {})  
                    res = Metric.add_items_fr_jun_tf(mode=self.db_mode, # prod
                                                    db=db, metrics=metrics, source_id=source_id, project_id=self.project_id,
                                                    tz_str_db=self.tz_str_db, tz_str_system=self.tz_str_system,
                                                    granularity=gran, prev_granularity=self.prev_gran_list[gran], granularity_settings=granularity_settings, 
                                                    dt_from=db_exist_dt[gran], dt_to=cur_ts_period_dt[gran][0], 
                                                    datetime_to=self.settings['datetime_to'], first_item_enable=True)

                    insert_counter_all += res['insert_counter_all']
                    insert_counter[gran] += res['insert_counter_all']
                    upd_counter_all += res['upd_counter_all']
                    upd_counter[gran] += res['upd_counter_all']
                    # if res['insert_counter_all']>0:
                    #     print(gran, "Add ", res['insert_counter_all'], "items")
                    db_exist_dt_gran = SysBf.dt_to_tz(Metric.get_last_dt(db=db, granularity=gran, tz_str_db=self.tz_str_db, project_id=self.project_id, source_id=source_id), tz_str=self.tz_str_system)
                    if db_exist_dt[gran]<db_exist_dt_gran:
                        db_exist_dt[gran] = db_exist_dt_gran
                        # print(f"New db_exist_dt[{gran}]=", db_exist_dt[gran])
                        if db_exist_dt[gran]>max_dt:
                            max_dt = db_exist_dt[gran] 
                            # print(f"New max_dt=", db_exist_dt[gran])

                    if max_dt_bk != max_dt:
                        cur_ts_period = SysBf.get_dateframes_by_current_dt(date=max_dt, tpl="%Y-%m-%dT%H:%M:%S")
                        cur_ts_period_dt = SysBf.get_dateframes_by_current_dt(date=max_dt)
                        # print("New cur_ts_period:", cur_ts_period)

                # Запросим список метрики и их сумм по заданной гранулярности, метрикам и тегам
                tags_sum_list = Metric.get_tags_sum_list(db=db, granularity=gran, tz_str_db=self.tz_str_db, project_id=self.project_id, 
                                                            dt_from=cur_ts_period_dt[gran][0], dt_to=cur_ts_period_dt[gran][1])
                for mtres in tags_sum_list:      
                    upd_metric = mtres["metric_alias"]   
                    upd_tag = mtres["tag"] 
                    if not upd_metric in cur_metric_accum[gran]:
                        cur_metric_accum[gran][upd_metric] = {}    
                    if not upd_tag in cur_metric_accum[gran][upd_metric]:
                        cur_metric_accum[gran][upd_metric][upd_tag] = {'sum':0, 'cnt': 0}      
                    if not "all" in cur_metric_accum[gran][upd_metric]:
                        cur_metric_accum[gran][upd_metric]["all"] = {'sum':0, 'cnt': 0}      
                    cur_metric_accum[gran][upd_metric][upd_tag]["sum"] = mtres["value"] 
                    cur_metric_accum[gran][upd_metric]["all"]["sum"] = mtres["value"]   
                    cur_metric_accum[gran][upd_metric][upd_tag]["cnt"] = mtres["val_count"]  
                    cur_metric_accum[gran][upd_metric]["all"]["cnt"] = mtres["val_count"]   

            # Получить список доступных архивов
            file_list = self.api.get_list()
            
            if file_list!=False and len(file_list)>0:
                upd_metric_list = {
                    "m1": {},
                    "h1": {},
                    "d1": {},
                    "w1": {},
                    "mo1": {},
                }
                last_ts_period = {
                    "m1": ["",""],
                    "h1": ["",""],
                    "d1": ["",""],
                    "w1": ["",""],
                    "mo1": ["",""],
                }
                project_tags = Metric.get_tags(db=db, project_id=self.project_id)
                project_tags_ids = {}
                for tag in project_tags:
                    project_tags_ids[tag["tag"]] = tag["tag_id"]
                for dt_file in file_list:
                    if dt_file>=max_dt_source_str and dt_file<end_dt_source_str:
                        logging.info(f'API start get {dt_file}')

                        # end_dt_source = SysBf.dt_to_tz(datetime_to, self.tz_str_source)
                        # end_dt_source_str = end_dt_source.strftime("%Y-%m-%dT%H")   

                        # Забрать архивы по одному, при этом делая что ниже
                        api_timer_sec = 0
                        api_timer = SysTimer()
                        minute_file_list = self.api.get_files(file=dt_file, fr_api=self.fr_api)
                        dt_cur_hour = SysBf.dt_to_tz(SysBf.tzdt(datetime.strptime(dt_file, '%Y-%m-%dT%H'), self.tz_str_source), self.tz_str_system)
                        dt_cur_hour_day_str = dt_cur_hour.strftime("%Y-%m-%d")+"T00:00:00"

                        # Пройтись по минутам, открыть файлы, записать данные в базу данных с тегами, записать суммарные данные без тега  
                        if minute_file_list!=False and type(minute_file_list["flist"]) is list:    
                            for gran in self.add_gran_list:
                                # рассчитаем края периода по текущим данным
                                item_ts_period = ["",""]
                                if gran=="h1":
                                    dt_cur_hour_str = dt_cur_hour.strftime("%Y-%m-%dT%H")
                                    item_ts_period = [dt_cur_hour_str+":00:00", dt_cur_hour_str+":59:59"] 
                                elif gran=="d1":
                                    base_dt_str = dt_cur_hour.strftime("%Y-%m-%d")
                                    item_ts_period = [base_dt_str+"T00:00:00", base_dt_str+"T23:59:59"] 
                                elif gran=="w1":
                                    days_of_week = SysBf.get_days_of_week(dt_cur_hour)
                                    item_ts_period = [days_of_week[0].strftime("%Y-%m-%d")+"T00:00:00", days_of_week[1].strftime("%Y-%m-%d")+"T23:59:59"]     
                                elif gran=="mo1":
                                    days_of_month = SysBf.get_days_of_month(dt_cur_hour)
                                    item_ts_period = [days_of_month[0].strftime("%Y-%m-%d")+"T00:00:00", days_of_month[1].strftime("%Y-%m-%d")+"T23:59:59"]         

                                if item_ts_period[0]!=cur_ts_period[gran][0]:
                                    # Запишем данные по прошлому периоду
                                    granularity_settings = self.granularity_list.get(gran, {})    
                                    for upd_metric,metric_data in cur_metric_accum[gran].items():
                                        for metric_tag, metric_tag_vals in metric_data.items():
                                            if cur_ts_period[gran][0]>=dt_insert_from[gran] and cur_ts_period[gran][0]>db_exist_dt_str[gran]:
                                                if not upd_metric in upd_metric_list[gran]:
                                                    upd_metric_list[gran][upd_metric] = {}   
                                                if not metric_tag in upd_metric_list[gran][upd_metric]:
                                                    upd_metric_list[gran][upd_metric][metric_tag] = {"ts":[],"vals":[]}
                                                upd_metric_list[gran][upd_metric][metric_tag]["ts"].append(cur_ts_period[gran])
                                                if metric_tag_vals["cnt"]==0:
                                                    upd_metric_list[gran][upd_metric][metric_tag]["vals"].append(0)           
                                                else:        
                                                    if metrics[upd_metric]["up_dt_funct"]=="avg": # Средняя
                                                        upd_metric_list[gran][upd_metric][metric_tag]["vals"].append(metric_tag_vals["sum"] / metric_tag_vals["cnt"])           
                                                    else: # Сумма
                                                        upd_metric_list[gran][upd_metric][metric_tag]["vals"].append(metric_tag_vals["sum"])      

                                    # Сменился период в заданном таймфрейме
                                    last_ts_period[gran] = cur_ts_period[gran]
                                    cur_ts_period[gran] = item_ts_period 
                                    # Почистим накопители текущего периода
                                    cur_metric_accum[gran] = {} 


                            # При изменении таймфреймов проведем необохдимые действия по сохранению и т.п.
                            upd_metric_list["m1"] = {}
                            for minute_file in minute_file_list["flist"]:
                                # try:
                                    cur_minute = minute_file[-2:]   
                                    cur_ts_period["m1"] = [dt_file+f":{cur_minute}:00", dt_file+f":{cur_minute}:59"]
                                    minute_file_full = minute_file_list.get("foldername","")+"/"+minute_file
                                    with open(minute_file_full, 'r') as file:  
                                        reader = csv.reader(file)  
                                        upd_metric_minte_all_vals = {}
                                        exist_tg_mt = {}
                                        for row in reader:  
                                            if not type(row) is list or len(row)<3:
                                                continue
                                            upd_metric = row[0].strip().lower()
                                            # print(type(row), row)
                                            if not upd_metric in metrics:
                                                # Обрабатываются только зарегистрированные метрики
                                                continue
                                            upd_tag =  row[1].strip()
                                            if upd_tag=="UNKNOWN" or upd_tag=="":
                                                upd_tag="unknown"
                                            upd_value = float(row[2])

                                            if not upd_tag in exist_tg_mt:
                                                exist_tg_mt[upd_tag] = []
                                            if not upd_metric in exist_tg_mt[upd_tag]:
                                                exist_tg_mt[upd_tag].append(upd_metric) 
                                            else:
                                                logging.info(f"{minute_file} Dublicate metrics {upd_metric}:{upd_tag}")
                                                continue   

                                            # Добавление старших таймфреймов в списки их сохранения
                                            for gran in self.add_gran_list:
                                                if not upd_metric in cur_metric_accum[gran]:
                                                    cur_metric_accum[gran][upd_metric] = {}           
                                                if not upd_tag in cur_metric_accum[gran][upd_metric]:
                                                    cur_metric_accum[gran][upd_metric][upd_tag] = {'sum':0, 'cnt': 0}     
                                                if not "all" in cur_metric_accum[gran][upd_metric]:
                                                    cur_metric_accum[gran][upd_metric]["all"] = {'sum':0, 'cnt': 0}
                                                cur_metric_accum[gran][upd_metric][upd_tag]["sum"] += upd_value 
                                                cur_metric_accum[gran][upd_metric]["all"]["sum"] += upd_value   
                                                cur_metric_accum[gran][upd_metric][upd_tag]["cnt"] += 1 
                                                cur_metric_accum[gran][upd_metric]["all"]["cnt"] += 1  
                                            
                                            # Если надо сохранять m1, до добавим в список сохранения
                                            if dt_cur_hour_day_str<dt_insert_from["m1"]:
                                                continue

                                            # Сформируем текущие значения
                                            if cur_ts_period["m1"][0]>db_exist_dt_str["m1"]:
                                                print("cur_ts_period_m1:", cur_ts_period["m1"][0], " > db_exist_dt_str_m1:", db_exist_dt_str["m1"])
                                                if not upd_metric in upd_metric_list["m1"]:
                                                    upd_metric_list["m1"][upd_metric] = {}   
                                                if not upd_tag in upd_metric_list["m1"][upd_metric]:
                                                    upd_metric_list["m1"][upd_metric][upd_tag] = {"ts":[],"vals":[]}
                                                upd_metric_list["m1"][upd_metric][upd_tag]["ts"].append(cur_ts_period["m1"])
                                                upd_metric_list["m1"][upd_metric][upd_tag]["vals"].append(upd_value)

                                            # Добавим в накопитель по текущей минуте
                                            if not upd_metric in upd_metric_minte_all_vals:
                                                upd_metric_minte_all_vals[upd_metric] = 0      
                                            upd_metric_minte_all_vals[upd_metric] += upd_value

                                        # По всем минутным метрикам сформируем "all" из накопителя по текущей минуте
                                        if cur_ts_period["m1"][0]>db_exist_dt_str["m1"]:
                                            for upd_metric,upd_metric_val in  upd_metric_minte_all_vals.items():
                                                if not upd_metric in upd_metric_list["m1"]:
                                                    upd_metric_list["m1"][upd_metric] = {}
                                                if not "all" in upd_metric_list["m1"][upd_metric]:
                                                    upd_metric_list["m1"][upd_metric]["all"] = {"ts":[],"vals":[]}
                                                upd_metric_list["m1"][upd_metric]["all"]["ts"].append(cur_ts_period["m1"])
                                                upd_metric_list["m1"][upd_metric]["all"]["vals"].append(upd_metric_val)        
        
                                # except Exception as err:  
                                #     logging.info(f'Robot_getload:run: Error open {minute_file_full} Unexpected {err=}, {type(err)=}')


                            granularity_settings = self.granularity_list.get("m1", {})  
                            for upd_metric,metric_data in upd_metric_list["m1"].items():
                                for metric_tag, metric_tag_data in metric_data.items():
                                    if metric_tag=="all" or metric_tag=="UNKNOWN":
                                        metric_tag = ""   
                                    if metric_tag == "":
                                        metric_tag_id = 0
                                    elif metric_tag in project_tags_ids:
                                        metric_tag_id = project_tags_ids[metric_tag]
                                    else:
                                        # Тег не зарегистрирован, добавим в массив и базу
                                        metric_tag_id = Metric.add_tag(db=db, project_id=self.project_id, metric_tag=metric_tag)
                                        project_tags_ids[metric_tag] = metric_tag_id  
                                        logging.info(f'Add tag {metric_tag_id} to project_id={self.project_id}')   

                                    res = Metric.add_fr_ym(db=db,
                                                metrics=metrics, # Словарь метрик с их параметрами
                                                granularity="m1", granularity_settings=granularity_settings, 
                                                source_id=source_id,
                                                tz_str_source=self.tz_str_source, tz_str_system=self.tz_str_system, tz_str_db=self.tz_str_db,
                                                upd_metric=upd_metric, # API алиас изменяемой метрики
                                                project_id=self.project_id,
                                                metric_tag_id=metric_tag_id,
                                                upd_metric_vals=metric_tag_data["vals"], # Список добавляемых значений метрики
                                                upd_metric_time_intervals=metric_tag_data["ts"], # Список интервалов добавляемых элементов
                                                mode=self.db_mode, # prod
                                                datetime_to=self.settings['datetime_to'], first_item_enable=True)  
                                    insert_counter_all += res['insert_counter_all'] 
                                    insert_counter["m1"] += res['insert_counter_all'] 

                        api_timer_sec = api_timer.get_time()
                        if api_timer_sec<self.source_get_api_lag_sec: 
                            # Обеспечение минимального перерыва между запросами TODO - далее брать лаг из базы.
                            time.sleep(self.source_get_api_lag_sec - api_timer_sec)
                        logging.info(f'API complite get {dt_file}')
                

                for gran in self.add_gran_list:
                    granularity_settings = self.granularity_list.get(gran, {})  
                    for upd_metric,metric_data in upd_metric_list[gran].items():
                        for metric_tag, metric_tag_data in metric_data.items():
                            if metric_tag=="all" or metric_tag=="UNKNOWN":
                                metric_tag = ""   
                            if metric_tag == "":
                                metric_tag_id = 0
                            elif metric_tag in project_tags_ids:
                                metric_tag_id = project_tags_ids[metric_tag]
                            else:
                                # Тег не зарегистрирован, добавим в массив и базу
                                metric_tag_id = Metric.add_tag(db=db, project_id=self.project_id, metric_tag=metric_tag)
                                project_tags_ids[metric_tag] = metric_tag_id       
                            res = Metric.add_fr_ym(db=db,
                                        metrics=metrics, # Словарь метрик с их параметрами
                                        granularity=gran, granularity_settings=granularity_settings, 
                                        source_id=source_id,
                                        tz_str_source=self.tz_str_source, tz_str_system=self.tz_str_system, tz_str_db=self.tz_str_db,
                                        upd_metric=upd_metric, # API алиас изменяемой метрики
                                        project_id=self.project_id,
                                        metric_tag_id=metric_tag_id,
                                        upd_metric_vals=metric_tag_data["vals"], # Список добавляемых значений метрики
                                        upd_metric_time_intervals=metric_tag_data["ts"], # Список интервалов добавляемых элементов
                                        mode=self.db_mode, # prod
                                        datetime_to=self.settings['datetime_to'], first_item_enable=True)  
                            insert_counter_all += res['insert_counter_all'] 
                            insert_counter[gran] += res['insert_counter_all'] 
        except Exception as err:
            errmess = f'Robot:getload:run: {type(err)=} Unexpected {err=}'
            logging.error(errmess)                                  
            self.comment(errmess)
        ########################[ /Робот ]##########################

        # Удалим блокирующий запуск файл
        os.remove(proc_file)

        self.comment(f"Update: {upd_counter_all}; Insert all:{insert_counter_all}")
        for gran in ["m1", "h1", "d1", "w1", "mo1"]:
            self.comment(f"Insert {gran}:{insert_counter[gran]}")
        return {"success": True, 
                      "telemetry": {
                          "job_execution_sec": run_timer.get_time(), 
                          "job_max_mem_kb": SysBf.get_max_memory_usage()},
                      "count": insert_counter_all + upd_counter_all,
                      "comment": self.comment_str} 
        