from models.mysqldb import Mysqldb
import json
import logging

from models.job import Job
from models.metric import Metric

class Task:

    table = 'tasks'
    info = None
    job = None
    id = None
    project_id = 0

    def __init__(self, *, db:Mysqldb, id:int):
        assert id > 0, 'Task.__init__: Tasks id is not set'
        self.db = db
        self.id = int(id)
        self.info = self.get_info()
        self.project_id = self.info["task_project_id"]

    @staticmethod
    def get_task(*, db:Mysqldb, id:int=0):
        if not id:
            return None
        task = Task(db=db, id=id)
        if not task.info:
            return None
        return task


    @staticmethod
    def get_list(*, db:Mysqldb, active:int=-1, project_id:int=0) -> list:
        active = int(active)
        sql = f"SELECT * from {Task.table}"
        sql_where = " WHERE 1=1"       
        if active>=0:
            sql_where += f" and task_active={active}"     
        if project_id>=0:
            sql_where += f" and task_project_id={project_id}"         
        if sql_where != " WHERE 1=1":    
            sql += sql_where  
        sql += ";"        
        result = db.query(sql)
        return result  
        
    def get_info(self) -> dict:
        sql = f"SELECT * from {self.table} where id={self.id};"     
        result = self.db.query(sql)
        info = None
        if result: 
            info = result[0]
        info['task_settings'] = json.loads(info['task_settings'])    
        return info 
    
    def get_jobs_list(self, *, limit:int=0, status:str='') -> list:
        return Job.get_list(db=self.db, task_id=self.id, limit=limit, status=status, 
                            project_id=self.project_id)
    
    def get_run(self) -> int:
        return  Job.get_run(db=self.db, task_id=self.id, max_execution_sec=self.info['task_max_execution_sec'], 
                            project_id=self.project_id)

    def create_job(self) -> Job:
        if not self.job and not self.get_run():
            self.job = Job.create_job(db=self.db, task_id=self.id, project_id=self.project_id)
            return self.job
        logging.warning(f"Task[{self.id}] already have the job!")
        return None

    def update_job(self, *, job_execution_sec:int=0, job_max_mem_kb:int=0,
                   job_dt_fin='', job_status='', job_comment='') -> int:
        if self.job:
            job = Job(db=self.db, id=self.job, project_id=self.project_id)
            return job.update_job(
                job_execution_sec = job_execution_sec,
                job_max_mem_kb = job_max_mem_kb, 
                job_dt_fin = job_dt_fin, 
                job_status = job_status, 
                job_comment = job_comment)
        return 0
    
    def delete_jobs(self, *, status:str='') -> int:
        self.job = None
        return Job.delete_jobs(db=self.db, status=status, task_id=self.id, project_id=self.project_id)

    @staticmethod
    def create_tasks_for_metrics(*, db:Mysqldb, group_id:int=0, project_id:int=0) -> int:
        'Добавляет задачи по метрикам без задач'
        
        counter = 0
        if project_id==0:
            return 0
        
        metric_list = Metric.get_list(db=db, group_id=group_id)
        print('len metric_list:', len(metric_list))
        tasks_list = Task.get_list(db=db, project_id=project_id)
        tasks_list2 = []
        if type(tasks_list) is list or len(tasks_list)>0:
            for task in tasks_list:
                task_settings = json.loads(task['task_settings'])    
                if task_settings.get('data', False) and task_settings['data'].get('metric_id', False):
                    tasks_list2.append(task_settings['data']['metric_id'])

        if type(metric_list) is list and len(metric_list)>0:
            for metric in metric_list:
                if not metric['id'] in tasks_list2:
                    message_lvl = 'all'
                    if metric['metric_group_id']==1:
                        message_lvl = 'critical'
                    elif metric['metric_group_id']==2:       
                        message_lvl = 'important'
                    accum_items = 1
                    if message_lvl == 4:
                        accum_items = 8
                    task_active = 0
                    if metric['metric_monitor']==1:
                        task_active = 1     
                    cur_metric_id = metric['id']    
                    task_settings_str = '{"data":{"region_alias": "", "device_alias": ""}, "anoms":{"direction": "both", "max_anoms": 0.2, "alpha": 0.01, "piecewise_median_period_weeks": 2}}'
                    sql = f"INSERT INTO {Task.table} (task_active, metric_id, granularity, message_lvl, task_comment, task_settings, task_robot, task_project_id) VALUES ({task_active}, {cur_metric_id}, 'h1', '{message_lvl}', 'anom_{metric['metric_alias']}_h1', '{task_settings_str}', 'twanom', {project_id});"    
                    db.insert(sql)
                    counter += 1

        return counter 
    
    @staticmethod
    def truncate_tasks(*, db:Mysqldb) -> int:
        return db.delete(f"TRUNCATE TABLE {Task.table};")