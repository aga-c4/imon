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
