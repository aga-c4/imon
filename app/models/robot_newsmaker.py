import time
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
import logging
import matplotlib.pyplot as plt
import io
import pandas as pd
from plotly import graph_objects as go
import plotly.express as px  
from models.project import Project
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
            "messages": [],
            "project_id": 0
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
        elif granularity=='h1':
            datetime_to = SysBf.tzdt_fr_str(datetime_now.strftime("%Y-%m-%d %H:00:00"), self.tz_str_system)  
        elif granularity=='d1':    
            datetime_to = SysBf.tzdt_fr_str(datetime_now.strftime("%Y-%m-%d 00:00:00"), self.tz_str_system)  
        elif granularity=='w1':      
            datetime_to_dict = SysBf.get_days_of_week(datetime_now, "%Y-%m-%d 00:00:00")  
            datetime_to = SysBf.tzdt_fr_str(datetime_to_dict[0], self.tz_str_system)  
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
        res = None
        self.comment_str = ''
        start_time = time.time() 
        logging.info(f"Robot {self.alias} run")   
        Message.send(self.settings['title'], lvl=self.message_lvl) 

        project_id = int(self.settings.get("project_id", 0))
        project = Project(db=self.db, id=project_id)
        self.comment(f"project: {project.info['metric_project_name']}, granularity: {self.settings['granularity']}")     

        if project.info["active"]>0:

            message_def = {
                "message_lvl": self.settings["message_lvl"],
                "granularity": self.settings["granularity"],
                "dt_to": self.settings["dt_to"],
                "dt_delta_fr": self.settings["dt_delta_fr"],   
                "project_id": project_id,
                "metric_tag_id": 0 
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
                elif message['type']=='pie':
                    res = self.get_pie(settings=settings)  
                elif message['type']=='tagspie':
                    res = self.get_tagspie(settings=settings)           

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
        
        dt_to = settings["dt_to_less"] - timedelta(seconds=1)
        dt1_str = settings["dt_from"].strftime("%Y-%m-%d")
        dt2_str= dt_to.strftime("%Y-%m-%d")
        if dt1_str==dt2_str:
            dt_diapazone_str = dt1_str
        else:
            dt_diapazone_str = dt1_str + ' - ' + dt2_str 

        mlabels = {}
        for metric_pos, metric_id in enumerate(settings["metric_ids"]): 
            mlabels[metric_id] = settings["metric_title"][metric_pos]    

        res = Metric.get_sum_by_metric_ids(db=self.db, tz_str_db=self.tz_str_db, 
                granularity=settings["granularity"], 
                dt_from=settings["dt_from"],
                dt_to_less=settings["dt_to_less"], 
                metric_ids=settings["metric_ids"],
                project_id=settings["project_id"],
                metric_tag_id=settings["metric_tag_id"])
        
        values = []
        labels = []
        for metric_res in res:
            metric_id = metric_res['metric_id'] 
            metric_value = metric_res['value'] 
            values.append(metric_value)    
            labels.append(mlabels[metric_id])  
        
        data_funnel = {}
        data_funnel["stage"] = labels
        data_funnel["number"] = values

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

        dt_to = settings["dt_to_less"] - timedelta(seconds=1)
        dt1_str = settings["dt_from"].strftime("%Y-%m-%d")
        dt2_str= dt_to.strftime("%Y-%m-%d")
        if dt1_str==dt2_str:
            dt_diapazone_str = dt1_str
        else:
            dt_diapazone_str = dt1_str + ' - ' + dt2_str 
 
        figure_data = []
        for metric_pos, metric_id in enumerate(settings["metric_ids"]):
            res = Metric.get_values(db=self.db, tz_str_db=self.tz_str_db, 
                granularity=settings["granularity"], 
                dt_from=settings["dt_from"], 
                dt_to_less=settings["dt_to_less"], 
                metric_id=metric_id,
                project_id=settings["project_id"],
                metric_tag_id=settings["metric_tag_id"])  
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

        dt_to = settings["dt_to_less"] - timedelta(seconds=1)
        dt1_str = settings["dt_from"].strftime("%Y-%m-%d")
        dt2_str= dt_to.strftime("%Y-%m-%d")
        if dt1_str==dt2_str:
            dt_diapazone_str = dt1_str
        else:
            dt_diapazone_str = dt1_str + ' - ' + dt2_str 
        
        fig = go.Figure()
        for metric_pos, metric_id in enumerate(settings["metric_ids"]):
            res = Metric.get_values(db=self.db, tz_str_db=self.tz_str_db, 
                granularity=settings["granularity"], 
                dt_from=settings["dt_from"], 
                dt_to_less=settings["dt_to_less"], 
                metric_id=metric_id,
                project_id=settings["project_id"],
                metric_tag_id=settings["metric_tag_id"])    
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


    def get_pie(self, *, settings:dict):

        """
        {
            "title": "Пользователи сайта",
            "type": "stack",
            "metric_ids": [201,200], 
            "metric_title": ["Вернувшиеся", "Новые"],
            "add_other": True,
            "total_metric_id": 1,
            "other_title": "Остальное",
            "other_val_dp": 0 
        }
        """

        if not "metric_ids" in settings \
            or not "metric_title" in settings \
            or not type(settings["metric_ids"]) is list \
            or not type(settings["metric_title"]) is list \
            or len(settings["metric_ids"])==0 \
            or len(settings["metric_ids"]) != len(settings["metric_title"]):
            return {}

        dt_to = settings["dt_to_less"] - timedelta(seconds=1)
        dt1_str = settings["dt_from"].strftime("%Y-%m-%d")
        dt2_str= dt_to.strftime("%Y-%m-%d")
        if dt1_str==dt2_str:
            dt_diapazone_str = dt1_str
        else:
            dt_diapazone_str = dt1_str + ' - ' + dt2_str 

        mlabels = {}
        for metric_pos, metric_id in enumerate(settings["metric_ids"]): 
            mlabels[metric_id] = settings["metric_title"][metric_pos]

        total_metric_id = 0
        if settings["add_other"] == True and int(settings.get("total_metric_id", 0)) > 0 and not settings["total_metric_id"] in settings["metric_ids"]:
            total_metric_id = settings["total_metric_id"]
            settings["metric_ids"].append(total_metric_id)
        res = Metric.get_sum_by_metric_ids(db=self.db, tz_str_db=self.tz_str_db, 
                granularity = settings["granularity"], 
                dt_from = settings["dt_from"],
                dt_to_less = settings["dt_to_less"], 
                metric_ids = settings["metric_ids"],
                project_id = settings["project_id"],
                metric_tag_id = settings["metric_tag_id"],
                order_by = 'value')
        sum_vals = 0
        total_val = 0
        values = []
        labels = []
        for metric_res in res:
            metric_id = metric_res['metric_id'] 
            metric_value = metric_res['value'] 
            if metric_id==total_metric_id:
                total_val = metric_value
            else:
                sum_vals += metric_value
                values.append(format(metric_value, "g"))    
                labels.append(mlabels[metric_id])  
        if total_metric_id>0 and total_val > sum_vals:
            values.append(format(round(total_val - sum_vals, settings.get("val_dp", 0)), "g"))    
            labels.append(settings.get("other_title", "Other"))  

        # Расчет процентов и подготовка списка
        total = sum(values)
        details = []
        for pos, value in enumerate(values):
            percent = (value / total) * 100
            details.append(f"{labels[pos]}: {value} ({percent:.1f}%)")    

        fig = px.pie(values=values, 
                     names=details, 
                     width=400, 
                     height=400)  
        fig.update_traces(textposition='outside', textinfo='percent')
        fig.update_layout(autosize=False, height=700, width=1800)
        fig.update_layout(plot_bgcolor='#ffffff')
        fig.update_layout(title_text=f'{settings["title"]} {dt_diapazone_str}')

        pie_object = io.BytesIO()
        fig.write_image(pie_object)
        pie_object.name = f'pie_{datetime.now().strftime("%Y%m%d%H%M%S")}.png'
        pie_object.seek(0)

        Message.send('', img_buf=pie_object, lvl=self.message_lvl)

        pie_object.close()

        return {}
                
    def get_tagspie(self, *, settings:dict):   
        if not "metric_id" in settings \
            or not type(settings["metric_id"]) is int \
            or settings["metric_id"] == 0:
            return {}

        dt_to = settings["dt_to_less"] - timedelta(seconds=1)
        dt1_str = settings["dt_from"].strftime("%Y-%m-%d")
        dt2_str= dt_to.strftime("%Y-%m-%d")
        if dt1_str==dt2_str:
            dt_diapazone_str = dt1_str
        else:
            dt_diapazone_str = dt1_str + ' - ' + dt2_str 

        limit = settings.get("limit", 0)    

        res = Metric.get_sum_by_metric_tags(db=self.db, tz_str_db=self.tz_str_db, 
                granularity = settings["granularity"], 
                dt_from = settings["dt_from"],
                dt_to_less = settings["dt_to_less"], 
                metric_id = settings["metric_id"],
                project_id = settings["project_id"], 
                limit=limit)
        
        
        sum_vals = 0
        total_val = 0
        values = []
        labels = []
        for metric_res in res: 
            tag_id = metric_res['tag_id']
            tag_name = metric_res['tag_name']
            tag_value = metric_res['value']
            if tag_id==0:
                total_val = tag_value
            else:
                sum_vals += tag_value
                values.append(format(tag_value, "g"))    
                labels.append(tag_name)  
        if total_val > sum_vals:
            values.append(format(round(total_val - sum_vals, settings.get("val_dp", 0)), "g"))    
            labels.append(settings.get("other_title", "Other"))  

        # Расчет процентов и подготовка списка
        total = sum(values)
        details = []
        for pos, value in enumerate(values):
            percent = (value / total) * 100
            details.append(f"{labels[pos]}: {value} ({percent:.1f}%)") 

        fig = px.pie(values=values, 
                     names=details, 
                     width=1024, 
                     height=768)
        fig.update_traces(textposition='outside', textinfo='percent')  
        fig.update_layout(autosize=False, height=768, width=1024)
        fig.update_layout(plot_bgcolor='#ffffff')
        fig.update_layout(title_text=f'{settings["title"]} {dt_diapazone_str}')

        tagspie_object = io.BytesIO()
        fig.write_image(tagspie_object)
        tagspie_object.name = f'stack_{datetime.now().strftime("%Y%m%d%H%M%S")}.png'
        tagspie_object.seek(0)

        Message.send('', img_buf=tagspie_object, lvl=self.message_lvl)

        tagspie_object.close()   
        
        return {}    
