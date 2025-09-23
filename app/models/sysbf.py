import logging
from pandas import Series
import datetime
from dateutil.parser import parse
import pytz
import os
import resource # Не работает в Windows
from importlib import import_module

class SysBf:

    @staticmethod
    def get_max_memory_usage():
        max_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return max_memory

    @staticmethod
    def trim_series(series:Series, last_items:int=0):
        "Отдает последние last_items элементов pandas.Series, если last_items=0, то все"
        if last_items == 0:
            return series
        if len(series) <= last_items:
            return series
        else:
            return series[-last_items:]
        
    @staticmethod
    def filter_series_by_datetime(series:Series, datetime:datetime):
        filtered_series = series.loc[series.index > datetime]
        return filtered_series   

    @staticmethod    
    def tzdt_fr_str(dt_str:str='', tz_str:str='') -> datetime:
        "Сначала пробуем 3 топовых формата, потом более медленно распознаем все. Если не определилось, то отдаст начало эпохи Unix"
        
        # https://pythonist.ru/preobrazovanie-strok-v-datu-so-vremenem/?ysclid=m17h82ndn110307520
        date_time_obj = datetime.datetime.fromtimestamp(0)
        if dt_str!='':
            try:
                date_time_obj = datetime.datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S.%f')
            except:
                try:
                    date_time_obj = datetime.datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
                except:
                    try:
                        date_time_obj = datetime.datetime.strptime(dt_str, '%Y-%m-%d %H')
                    except:
                        try:
                            date_time_obj = datetime.datetime.strptime(dt_str, '%Y-%m-%d')
                        except:
                            try:
                                date_time_obj = datetime.datetime.strptime(dt_str, '%Y-%m')
                            except:
                                try:
                                    date_time_obj = parse(dt_str)
                                except:
                                    logging.error(f'SysBf:tzdt_fr_str: Date format error [{dt_str}] type:' + str(type(dt_str)))
        return SysBf.tzdt(dt=date_time_obj, tz_str=tz_str)
    
    @staticmethod
    def tzdt(dt:datetime, tz_str:str='') -> datetime:
        tzdt = dt
        if tz_str!='':
            try:
                timezone = pytz.timezone(tz_str)
                tzdt = timezone.localize(tzdt)
            except:
                logging.error(f'SysBf:tzdt: Timezone format error [{tz_str}] type:' + str(type(tz_str)) + ' time: ' + str(dt))    

        return tzdt

    @staticmethod
    def dt_to_tz(dt:datetime, tz_str:str='') -> datetime:
        if tz_str!='':
            timezone = pytz.timezone(tz_str)
            return  dt.astimezone(timezone)  
        return dt.astimezone(pytz.utc)    

    @staticmethod
    def get_dateframes_by_current_dt(date:datetime, granularity:str="", tpl:str=""):    
        result = {}
        resitem = None
        if granularity=="" or granularity=="m1":
            resitem = [date.replace(second=0, microsecond=0), date.replace(second=59, microsecond=1000) ]
            if tpl!="":
                result["m1"] = [resitem[0].strftime(tpl), resitem[1].strftime(tpl)]
            else:        
                result["m1"] = resitem
        if granularity=="" or granularity=="h1":    
            resitem = [date.replace(minute=0, second=0, microsecond=0), date.replace(minute=59, second=59, microsecond=1000)]
            if tpl!="":
                result["h1"] = [resitem[0].strftime(tpl), resitem[1].strftime(tpl)]
            else:        
                result["h1"] = resitem
        if granularity=="" or granularity=="d1":
            resitem = [date.replace(hour=0, minute=0, second=0, microsecond=0), date.replace(hour=23, minute=59, second=59, microsecond=1000)]
            if tpl!="":
                result["d1"] = [resitem[0].strftime(tpl), resitem[1].strftime(tpl)]
            else:        
                result["d1"] = resitem
        if granularity=="" or granularity=="w1":
            resitem = SysBf.get_days_of_week(date, tpl)
            result["w1"] = resitem
        if granularity=="" or granularity=="mo1":
            resitem = SysBf.get_days_of_month(date, tpl)
            result["mo1"] = resitem
        if granularity!="" and resitem!=None:
            return resitem        
        else:
            return result
        
    @staticmethod
    def get_days_of_month(date:datetime, tpl:str=""):
        firstd = date.replace(day=1) 
        if date.month == 12:
            lastd = date.replace(day=31)
        else:    
            lastd = date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)     
        firstd = firstd.replace(hour=0, minute=0, second=0, microsecond=0) 
        lastd = lastd.replace(hour=23, minute=59, second=59, microsecond=1000) 
        if tpl!="":
            return [firstd.strftime(tpl), lastd.strftime(tpl)] 
        else:    
            return [firstd, lastd] 

    @staticmethod
    def get_days_of_week(date:datetime, tpl:str=""):
        firstd = date - datetime.timedelta(days=date.weekday()) 
        lastd = firstd + datetime.timedelta(days=6)
        firstd = firstd.replace(hour=0, minute=0, second=0, microsecond=0) 
        lastd = lastd.replace(hour=23, minute=59, second=59, microsecond=1000) 
        if tpl!="":
            return [firstd.strftime(tpl), lastd.strftime(tpl)] 
        else:    
            return [firstd, lastd]  
    
    @staticmethod
    def as_timezone(dt:datetime, tz_to_str:str='') -> datetime:
        tzdt = dt
        if tz_to_str!='':
            try:
                timezone = pytz.timezone(tz_to_str)
                tzdt = timezone.astimezone(tzdt)
            except:
                logging.error(f'SysBf:astimezone: Timezone format error [{tz_to_str}] type:' + str(type(tz_to_str)))    

        return tzdt

    @staticmethod
    def get_substring(text:str, start_text:str="", end_text:str=""):
        if start_text == "":
            start_index = 0
        else:
            start_index = text.find(start_text)   
        
        if end_text == "":
            end_index = len(text)
        else:
            end_index = text.find(end_text)

        if start_index == -1 or end_index == -1:
            return ""        
        
        return text[start_index + len(start_text):end_index]
    
    @staticmethod
    def class_factory(module_name, class_name, *args, **kwargs):
        logging.info(f"SysBF:Factory:New: {class_name} from {module_name}") 
        try:
            module = import_module(module_name)
            try:
                class_obj = getattr(module, class_name)
                try:
                    instance = class_obj(*args, **kwargs)
                    return instance  # Вы создали экземпляр класса.
                except:
                    logging.warning(f"Error new [{class_name}] in {class_obj.__class__.__name__}")        
            except:
                logging.warning(f"Error getattr [{class_name}]")        
        except:
            logging.warning(f"Error import_module [{module_name}]") 
        
        return None
    
    @staticmethod
    def call_method_fr_obj(obj, method_name, *args, **kwargs):
        # Получаем метод из объекта по имени
        method = getattr(obj, method_name, None)
        if callable(method):
            # Вызываем метод с переданными аргументами
            return method(*args, **kwargs)
        else:
            logging.warning(f"Method not found: {method_name} in {obj.__class__.__name__}")
            return None
        
    @staticmethod
    def getitem(source, item, default=None):
        if type(source) is list:
            item_int = int(item)
            if len(source)>item_int:
                return source[item_int]
        elif type(source) is dict:
            return source.get(item, default)     
        return default    
        