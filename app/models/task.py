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

    def __init__(self, *, db:Mysqldb, id:int):
        assert id > 0, 'Task.__init__: Tasks id is not set'
        self.db = db
        self.id = int(id)
        self.info = self.get_info()

    @staticmethod
    def get_task(*, db:Mysqldb, id:int=0):
        if not id:
            return None
        task = Task(db=db, id=id)
        if not task.info:
            return None
        return task

    @staticmethod
    def get_list(*, db:Mysqldb, active:int=-1) -> list:
        active = int(active)
        sql = f"SELECT * from {Task.table}"
        if active>=0:
            sql += f" WHERE task_active={active}"     
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
        return Job.get_list(db=self.db, task_id=self.id, limit=limit, status=status)
    
    def get_run(self) -> int:
        return  Job.get_run(db=self.db, task_id=self.id, max_execution_sec=self.info['task_max_execution_sec'])

    def create_job(self) -> Job:
        if not self.job and not self.get_run():
            self.job = Job.create_job(db=self.db, task_id=self.id)
            return self.job
        logging.warning(f"Task[{self.id}] already have the job!")
        return None

    def update_job(self, *, job_execution_sec=0, job_max_mem_kb=0, job_dt_fin='', job_status='', job_comment='') -> int:
        if self.job:
            job = Job(db=self.db, id=self.job)
            return job.update_job(
                job_execution_sec=job_execution_sec,
                job_max_mem_kb=job_max_mem_kb, 
                job_dt_fin=job_dt_fin, 
                job_status=job_status, 
                job_comment=job_comment)
        return 0
    
    def delete_jobs(self, *, status:str='') -> int:
        self.job = None
        return Job.delete_jobs(db=self.db, status=status, task_id=self.id)

    @staticmethod
    def create_tasks_for_metrics(*, db:Mysqldb, group_id:int=0) -> int:
        'Добавляет задачи по метрикам без задач'
        
        counter = 0
        metric_list = Metric.get_list(db=db, group_id=group_id)
        print('len metric_list:', len(metric_list))
        tasks_list = Task.get_list(db=db)
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
                    task_settings_str = '{"data":{"metric_id":'+str(metric['id'])+', "granularity":"h1", "region_alias": "", "device_alias": "","accum_items": '+str(accum_items)+'}, "anoms":{"direction": "both", "max_anoms": 0.2, "alpha": 0.01, "piecewise_median_period_weeks": 2},"message_lvl":"'+str(message_lvl)+'"}'
                    sql = f"INSERT INTO {Task.table} (task_active, task_comment, task_settings, task_robot) VALUES (1, 'anom_{metric['metric_alias']}_h1', '{task_settings_str}', 'twanom');"    
                    db.insert(sql)
                    counter += 1

        return counter 
    
    @staticmethod
    def truncate_tasks(*, db:Mysqldb) -> int:
        return db.delete(f"TRUNCATE TABLE {Task.table};")