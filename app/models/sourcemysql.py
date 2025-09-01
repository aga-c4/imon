from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
import logging
import json
import pandas as pd
import decimal

from models.mysqldb import Mysqldb
from models.sysbf import SysBf
from config import config

class Sourcemysql:

    tmp_path = 'tmp/mysql1get'
    proc_path = 'tmp/process'
    dtstr_tpl = {
            'm1': '%Y-%m-%d %H:%M',
            'h1': '%Y-%m-%d %H', 
            'd1': '%Y-%m-%d', 
            'w1': '%Y-%m-%d', 
            'mo1': '%Y-%m'
        }
    granularity_gr = {
            'm1': 'minute',
            'h1': "hour", 
            'd1': 'day', 
            'w1': 'week', 
            'mp1': 'month'
        }

    @staticmethod
    def get_weekday_fr_dtstr(*, dtstr:str, tz_str:str=''):
        return SysBf.tzdt_fr_str(dtstr, tz_str).weekday()

    @staticmethod
    def get_period_fr_dtstr(*, dtstr:str, granularity:str, tz_str:str=''):
        assert granularity in ['m1', 'h1', 'd1', 'w1', 'mo1'], 'Metric.get_data: granularity options: m1 | h1 | d1 | w1 | mo1'

        date1 = SysBf.tzdt_fr_str(dtstr, tz_str)
        if granularity=='m1':
            date2 = date1 + timedelta(minutes=1) - timedelta(seconds=1)
        if granularity=='h1':
            date2 = date1 + timedelta(hours=1) - timedelta(seconds=1)
        if granularity=='d1':
            date2 = date1 + timedelta(days=1) - timedelta(seconds=1)
        if granularity=='w1':
            date2 = date1 + timedelta(weeks=1) - timedelta(seconds=1)
        if granularity=='mo1':
            date2 = date1 + relativedelta(months = 1) - timedelta(seconds=1)
        
        return [datetime.strftime(date1, '%Y-%m-%d %H:%M:%S'), 
                datetime.strftime(date2, '%Y-%m-%d %H:%M:%S')]    

    @staticmethod
    def prepare_value(val):
        if type(val) is decimal.Decimal:
            return float(val)
        elif type(val) is int or type(val) is float or type(val) is str:
            return val
        else:
            return str(val)   

    @staticmethod
    def get_week_start_end(input_datetime:datetime):
        start_of_week = input_datetime - timedelta(days=input_datetime.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_week = end_of_week.replace(hour=23, minute=59, second=59, microsecond=999999)
        return start_of_week, end_of_week     
        
    @staticmethod
    def prepare_res(*, granularity:str, tz_str:str='',
                    dt_from_str:str='', dt_to_str:str='', metrics:list):    
        
        res = {
            "query": {
                "dimensions": [],
                "metrics": list(metrics)
            },
            "data": [
                {
                    "dimensions": [],
                    "metrics": []
                },
            ],
            "time_intervals": []
        }

        if dt_from_str!='':
            dt_from = SysBf.tzdt_fr_str(dt_from_str, tz_str)
        else:
            dt_from = SysBf.tzdt_fr_str('', tz_str)    
        if dt_to_str!='':
            dt_to = SysBf.tzdt_fr_str(dt_to_str, tz_str)
        else:    
            dt_to = SysBf.tzdt(datetime.now(), tz_str)

        if  granularity=='m1':
            dt_max = SysBf.tzdt_fr_str(datetime.strftime(dt_to, '%Y-%m'), tz_str)
            if dt_to>dt_max:
                dt_to = dt_max   
            
        dt_from_str = datetime.strftime(dt_from, '%Y-%m-%d 00:00:00')
        dt_to_str = datetime.strftime(dt_to, '%Y-%m-%d 23:59:59')

        res['query']["date1"] = dt_from_str
        res['query']["date2"] = dt_to_str
        res['query']["group"] = Sourcemysql.granularity_gr[granularity]

        for i in range(0,len(metrics)):
            res['data'][0]["metrics"].append([])

        return res
    
    @staticmethod
    def dt_validation(*, granularity:str, dt_obj:datetime, tz_str:str=''):  
        res = dt_obj
        if  granularity=='mo1':
            # текущий месяц начало
            dt_max = SysBf.tzdt_fr_str(datetime.strftime(datetime.now(), '%Y-%m'), tz_str)
        elif  granularity=='w1':
            # Текущий день начало
            dt_max = SysBf.tzdt_fr_str(datetime.strftime(datetime.now(), '%Y-%m-%d'), tz_str)
        elif  granularity=='d1':
            # Текущий день начало
            dt_max = SysBf.tzdt_fr_str(datetime.strftime(datetime.now(), '%Y-%m-%d'), tz_str)
        elif  granularity=='h1':
            # Текущий час начало
            dt_max = SysBf.tzdt_fr_str(datetime.strftime(datetime.now(), '%Y-%m-%d %H'), tz_str)
        elif  granularity=='m1':
            # Текущий час начало
            dt_max = SysBf.tzdt_fr_str(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M'), tz_str)    

        if dt_obj<dt_max:
            return True

        return False    
    
    @staticmethod
    def get_data(*, db:Mysqldb, granularity:str,
                                dt_from_str:str='', dt_to_str:str='', 
                                tz_str:str='', fileto:str='', metrics_list:list):
        
        if metrics_list[0]=='dbsrc_purchases_app':
            return Sourcemysql.get_dbsrc_purchases_app(db=db, granularity=granularity,
                                            dt_from_str=dt_from_str, dt_to_str=dt_to_str, 
                                            tz_str=tz_str, fileto=fileto)
        elif metrics_list[0]=='dbsrc_purchases_site':
            return Sourcemysql.get_dbsrc_purchases_site(db=db, granularity=granularity,
                                            dt_from_str=dt_from_str, dt_to_str=dt_to_str, 
                                            tz_str=tz_str, fileto=fileto)
       
        if metrics_list[0]=='dbsrc_articles_site_add':
            return Sourcemysql.get_dbsrc_articles_site_add(db=db, granularity=granularity,
                                            dt_from_str=dt_from_str, dt_to_str=dt_to_str, 
                                            tz_str=tz_str, fileto=fileto)

        if metrics_list[0]=='dbsrc_news_site_add':
            return Sourcemysql.get_dbsrc_news_site_add(db=db, granularity=granularity,
                                            dt_from_str=dt_from_str, dt_to_str=dt_to_str, 
                                            tz_str=tz_str, fileto=fileto)
   
        return False    

    @staticmethod
    def get_dbsrc_purchases_site(*, db:Mysqldb, granularity:str,
                                dt_from_str:str='', dt_to_str:str='', 
                                tz_str:str='', fileto:str=''):
        
        result_ok = True
        res = Sourcemysql.prepare_res(granularity=granularity, tz_str=tz_str, 
                                   dt_from_str=dt_from_str, dt_to_str=dt_to_str,
                                   metrics=["dbsrc_purchases_site"])

        sql = f"select ..."

        if dt_from_str!='':
            sql += f" and Date>='{res['query']['date1']}'"
        if dt_to_str!='':
            sql += f" and Date<='{res['query']['date2']}'"   

        sql += " GROUP BY dtstr;"    
        
        result = db.query(sql) 
        first_item = True
        cur_w_start_dt, cur_w_end_dt = Sourcemysql.get_week_start_end(SysBf.tzdt(datetime.now(), tz_str))
        val1 = 0
        if result:
            i = len(result) 
            if i>0:
                for row in result:
                    if granularity=='w1':
                        if first_item:
                            first_item = False
                            val1 = row["val1"]
                            date_start, date2 = Sourcemysql.get_period_fr_dtstr(dtstr=row["dtstr"], granularity='d1', tz_str=tz_str)
                            w_start_dt_old, w_end_dt_old = Sourcemysql.get_week_start_end(SysBf.tzdt_fr_str(row["dtstr"], tz_str))  
                            continue

                        curdt = SysBf.tzdt_fr_str(row["dtstr"], tz_str)
                        w_start_dt, w_end_dt = Sourcemysql.get_week_start_end(curdt)
                        if w_start_dt>w_start_dt_old or (i<=1 and curdt<cur_w_start_dt): # Следующая неделя
                            # Запишем сформированные данные
                            res['time_intervals'].append([date_start, date2])
                            res['data'][0]['metrics'][0].append(Sourcemysql.prepare_value(val1)) 
                            w_start_dt_old = w_start_dt  
                            w_end_dt_old = w_end_dt          

                            # Обновим счетчики
                            val1 = row["val1"]
                            date_start, date2 = Sourcemysql.get_period_fr_dtstr(dtstr=row["dtstr"], granularity='d1', tz_str=tz_str)

                            if i<=1:
                                res['time_intervals'].append([date_start, date2])
                                res['data'][0]['metrics'][0].append(Sourcemysql.prepare_value(val1))             
                        else:
                            date1, date2 = Sourcemysql.get_period_fr_dtstr(dtstr=row["dtstr"], granularity='d1', tz_str=tz_str)  
                            val = row["val1"]
                            if type(val) is decimal.Decimal or type(val) is int or type(val) is float:
                                val1 += val
                        
                    else:
                        if Sourcemysql.dt_validation(granularity=granularity, 
                                                  dt_obj=SysBf.tzdt_fr_str(row["dtstr"], tz_str=tz_str),
                                                  tz_str=tz_str):
                            # Если это не текущий временной интервал, то запишем
                            res['time_intervals'].append(Sourcemysql.get_period_fr_dtstr(dtstr=row["dtstr"], granularity=granularity, tz_str=tz_str))
                            res['data'][0]['metrics'][0].append(Sourcemysql.prepare_value(row["val1"]))      

                    i -= 1    
        if result_ok:
            if fileto!='':
                with open(fileto, "w") as f:
                    json.dump(res, f)
                    f.close() 
                return True    
            else:      
                return res
        else:
            return False
    

    @staticmethod
    def get_dbsrc_purchases_app(*, db:Mysqldb, granularity:str,
                                dt_from_str:str='', dt_to_str:str='', 
                                tz_str:str='', fileto:str=''):
        
        result_ok = True
        res = Sourcemysql.prepare_res(granularity=granularity, tz_str=tz_str, 
                                   dt_from_str=dt_from_str, dt_to_str=dt_to_str,
                                   metrics=["dbsrc_purchases_app"])

        sql = f"select ..."

        if dt_from_str!='':
            sql += f" and Date>='{res['query']['date1']}'"
        if dt_to_str!='':
            sql += f" and Date<='{res['query']['date2']}'"   

        sql += " GROUP BY dtstr;"    

        result = db.query(sql) 
        first_item = True
        cur_w_start_dt, cur_w_end_dt = Sourcemysql.get_week_start_end(SysBf.tzdt(datetime.now(), tz_str))
        val1 = 0
        if result:
            i = len(result) 
            if i>0:
                for row in result:
                    if granularity=='w1':
                        if first_item:
                            first_item = False
                            val1 = row["val1"]
                            date_start, date2 = Sourcemysql.get_period_fr_dtstr(dtstr=row["dtstr"], granularity='d1', tz_str=tz_str)
                            w_start_dt_old, w_end_dt_old = Sourcemysql.get_week_start_end(SysBf.tzdt_fr_str(row["dtstr"], tz_str))  
                            continue

                        curdt = SysBf.tzdt_fr_str(row["dtstr"], tz_str)
                        w_start_dt, w_end_dt = Sourcemysql.get_week_start_end(curdt)
                        if w_start_dt>w_start_dt_old or (i<=1 and curdt<cur_w_start_dt): # Следующая неделя
                            # Запишем сформированные данные
                            res['time_intervals'].append([date_start, date2])
                            res['data'][0]['metrics'][0].append(Sourcemysql.prepare_value(val1)) 
                            w_start_dt_old = w_start_dt  
                            w_end_dt_old = w_end_dt          

                            # Обновим счетчики
                            val1 = row["val1"]
                            date_start, date2 = Sourcemysql.get_period_fr_dtstr(dtstr=row["dtstr"], granularity='d1', tz_str=tz_str)

                            if i<=1:
                                res['time_intervals'].append([date_start, date2])
                                res['data'][0]['metrics'][0].append(Sourcemysql.prepare_value(val1))             
                        else:
                            date1, date2 = Sourcemysql.get_period_fr_dtstr(dtstr=row["dtstr"], granularity='d1', tz_str=tz_str)  
                            val = row["val1"]
                            if type(val) is decimal.Decimal or type(val) is int or type(val) is float:
                                val1 += val
                        
                    else:
                        if Sourcemysql.dt_validation(granularity=granularity, 
                                                  dt_obj=SysBf.tzdt_fr_str(row["dtstr"], tz_str=tz_str),
                                                  tz_str=tz_str):
                            # Если это не текущий временной интервал, то запишем
                            res['time_intervals'].append(Sourcemysql.get_period_fr_dtstr(dtstr=row["dtstr"], granularity=granularity, tz_str=tz_str))
                            res['data'][0]['metrics'][0].append(Sourcemysql.prepare_value(row["val1"]))      

                    i -= 1   
        if result_ok:
            if fileto!='':
                with open(fileto, "w") as f:
                    json.dump(res, f)
                    f.close() 
                return True    
            else:      
                return res
        else:
            return False
    

    @staticmethod
    def get_dbsrc_articles_site_add(*, db:Mysqldb, granularity:str,
                                dt_from_str:str='', dt_to_str:str='', 
                                tz_str:str='', fileto:str=''):
        
        result_ok = True
        res = Sourcemysql.prepare_res(granularity=granularity, tz_str=tz_str, 
                                   dt_from_str=dt_from_str, dt_to_str=dt_to_str,
                                   metrics=["dbsrc_articles_site_add"])
        
        sql = f"select ..."

        if dt_from_str!='':
            sql += f" and date>='{res['query']['date1']}'"
        if dt_to_str!='':
            sql += f" and date<='{res['query']['date2']}'"     

        sql += " GROUP BY dtstr;"    

        result = db.query(sql) 
        first_item = True
        cur_w_start_dt, cur_w_end_dt = Sourcemysql.get_week_start_end(SysBf.tzdt(datetime.now(), tz_str))
        val1 = 0
        if result:
            i = len(result) 
            if i>0:
                for row in result:
                    if granularity=='w1':
                        if first_item:
                            first_item = False
                            val1 = row["val1"]
                            date_start, date2 = Sourcemysql.get_period_fr_dtstr(dtstr=row["dtstr"], granularity='d1', tz_str=tz_str)
                            w_start_dt_old, w_end_dt_old = Sourcemysql.get_week_start_end(SysBf.tzdt_fr_str(row["dtstr"], tz_str))  
                            continue

                        curdt = SysBf.tzdt_fr_str(row["dtstr"], tz_str)
                        w_start_dt, w_end_dt = Sourcemysql.get_week_start_end(curdt)
                        if w_start_dt>w_start_dt_old or (i<=1 and curdt<cur_w_start_dt): # Следующая неделя
                            # Запишем сформированные данные
                            res['time_intervals'].append([date_start, date2])
                            res['data'][0]['metrics'][0].append(Sourcemysql.prepare_value(val1)) 
                            w_start_dt_old = w_start_dt  
                            w_end_dt_old = w_end_dt          

                            # Обновим счетчики
                            val1 = row["val1"]
                            date_start, date2 = Sourcemysql.get_period_fr_dtstr(dtstr=row["dtstr"], granularity='d1', tz_str=tz_str)

                            if i<=1:
                                res['time_intervals'].append([date_start, date2])
                                res['data'][0]['metrics'][0].append(Sourcemysql.prepare_value(val1))             
                        else:
                            date1, date2 = Sourcemysql.get_period_fr_dtstr(dtstr=row["dtstr"], granularity='d1', tz_str=tz_str)  
                            val = row["val1"]
                            if type(val) is decimal.Decimal or type(val) is int or type(val) is float:
                                val1 += val

                        
                    else:
                        if Sourcemysql.dt_validation(granularity=granularity, 
                                                  dt_obj=SysBf.tzdt_fr_str(row["dtstr"], tz_str=tz_str),
                                                  tz_str=tz_str):
                            # Если это не текущий временной интервал, то запишем
                            res['time_intervals'].append(Sourcemysql.get_period_fr_dtstr(dtstr=row["dtstr"], granularity=granularity, tz_str=tz_str))
                            res['data'][0]['metrics'][0].append(Sourcemysql.prepare_value(row["val1"]))      

                    i -= 1    
        if result_ok:
            if fileto!='':
                with open(fileto, "w") as f:
                    json.dump(res, f)
                    f.close() 
                return True    
            else:      
                return res
        else:
            return False
    
    @staticmethod
    def get_dbsrc_news_site_add(*, db:Mysqldb, granularity:str,
                                dt_from_str:str='', dt_to_str:str='', 
                                tz_str:str='', fileto:str=''):
        
        result_ok = True
        res = Sourcemysql.prepare_res(granularity=granularity, tz_str=tz_str, 
                                   dt_from_str=dt_from_str, dt_to_str=dt_to_str,
                                   metrics=["dbsrc_news_site_add"])
        
        sql = f"select ..."

        if dt_from_str!='':
            sql += f" and newsDatePub>='{res['query']['date1']}'"
        if dt_to_str!='':
            sql += f" and newsDatePub<='{res['query']['date2']}'"      

        sql += " GROUP BY dtstr;"    

        result = db.query(sql) 
        first_item = True
        cur_w_start_dt, cur_w_end_dt = Sourcemysql.get_week_start_end(SysBf.tzdt(datetime.now(), tz_str))
        val1 = 0
        if result:
            i = len(result) 
            if i>0:
                for row in result:
                    if granularity=='w1':
                        if first_item:
                            first_item = False
                            val1 = row["val1"]
                            date_start, date2 = Sourcemysql.get_period_fr_dtstr(dtstr=row["dtstr"], granularity='d1', tz_str=tz_str)
                            w_start_dt_old, w_end_dt_old = Sourcemysql.get_week_start_end(SysBf.tzdt_fr_str(row["dtstr"], tz_str))  
                            continue

                        curdt = SysBf.tzdt_fr_str(row["dtstr"], tz_str)
                        w_start_dt, w_end_dt = Sourcemysql.get_week_start_end(curdt)
                        if w_start_dt>w_start_dt_old or (i<=1 and curdt<cur_w_start_dt): # Следующая неделя
                            # Запишем сформированные данные
                            res['time_intervals'].append([date_start, date2])
                            res['data'][0]['metrics'][0].append(Sourcemysql.prepare_value(val1)) 
                            w_start_dt_old = w_start_dt  
                            w_end_dt_old = w_end_dt          

                            # Обновим счетчики
                            val1 = row["val1"]
                            date_start, date2 = Sourcemysql.get_period_fr_dtstr(dtstr=row["dtstr"], granularity='d1', tz_str=tz_str)

                            if i<=1:
                                res['time_intervals'].append([date_start, date2])
                                res['data'][0]['metrics'][0].append(Sourcemysql.prepare_value(val1))             
                        else:
                            date1, date2 = Sourcemysql.get_period_fr_dtstr(dtstr=row["dtstr"], granularity='d1', tz_str=tz_str)  
                            val = row["val1"]
                            if type(val) is decimal.Decimal or type(val) is int or type(val) is float:
                                val1 += val 
                        
                    else:
                        if Sourcemysql.dt_validation(granularity=granularity, 
                                                  dt_obj=SysBf.tzdt_fr_str(row["dtstr"], tz_str=tz_str),
                                                  tz_str=tz_str):
                            # Если это не текущий временной интервал, то запишем
                            res['time_intervals'].append(Sourcemysql.get_period_fr_dtstr(dtstr=row["dtstr"], granularity=granularity, tz_str=tz_str))
                            res['data'][0]['metrics'][0].append(Sourcemysql.prepare_value(row["val1"]))      

                    i -= 1    
        if result_ok:
            if fileto!='':
                with open(fileto, "w") as f:
                    json.dump(res, f)
                    f.close() 
                return True    
            else:      
                return res
        else:
            return False
    
