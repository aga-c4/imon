import logging
from pandas import Series
import datetime
from dateutil.parser import parse
import pytz
import os
import resource # Не работает в Windows

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

        tzdt = date_time_obj
        if tz_str!='':
            try:
                timezone = pytz.timezone(tz_str)
                tzdt = timezone.localize(date_time_obj)
            except:
                logging.error(f'SysBf:tzdt_fr_str: Timezone format error [{tz_str}] type:' + str(type(tz_str)))    

        return tzdt
    
    def tzdt(dt:datetime, tz_str:str='') -> datetime:
        tzdt = dt
        if tz_str!='':
            try:
                timezone = pytz.timezone(tz_str)
                tzdt = timezone.localize(tzdt)
            except:
                logging.error(f'SysBf:tzdt: Timezone format error [{tz_str}] type:' + str(type(tz_str)))    

        return tzdt
    
    def as_timezone(dt:datetime, tz_to_str:str='') -> datetime:
        tzdt = dt
        if tz_to_str!='':
            try:
                timezone = pytz.timezone(tz_to_str)
                tzdt = timezone.astimezone(tzdt)
            except:
                logging.error(f'SysBf:astimezone: Timezone format error [{tz_to_str}] type:' + str(type(tz_to_str)))    

        return tzdt
