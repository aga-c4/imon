from models.mysqldb import Mysqldb
from datetime import datetime, timedelta

class Job:

    table = 'jobs'

    def __init__(self, *, db:Mysqldb, id:int, project_id:int=0):
        assert id > 0, 'Job.__init__: Job id is not set'
        self.db = db
        self.id = int(id)
        self.project_id = int(project_id)

    @staticmethod
    def get_list(*, db:Mysqldb, task_id:int=0, limit:int=0, status:str='', project_id:int=0) -> list:
        task_id = int(task_id)

        if not limit:
            limit = 10

        sql = f"SELECT * from {Job.table}"     
        sql_where = " WHERE 1=1"       
        if task_id>0:
            sql_where += f" and task_id={task_id}"
        if status:
            sql_where += f" and job_status='{status}'"         
        if project_id>=0:
            sql_where += f" and job_project_id={project_id}"         
        if sql_where != " WHERE 1=1":    
            sql += sql_where      
        sql += f" ORDER BY id DESC LIMIT 0,{limit};"     
        result = db.query(sql)
        return result  
    
    @staticmethod
    def get_run(*, db:Mysqldb, task_id:int=0, max_execution_sec:int=300, project_id:int=0) -> int:
        current_time = datetime.now()
        five_minutes_ago = current_time - timedelta(seconds=max_execution_sec)
        formatted_time = five_minutes_ago.strftime('%Y-%m-%d %H:%M:%S')
        sql = f"SELECT * from {Job.table} where job_project_id={project_id} and task_id={task_id} and job_status='run' and dt>'{formatted_time}';"    
        result = db.query(sql)
        if result: 
            return result[0]['id']
        else:
            return None 

    @staticmethod
    def create_job(*, db:Mysqldb, task_id:int, project_id:int=0) -> int:
        assert task_id > 0, 'Job.create_job: task_id id is not set'
        formatted_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql =  f"INSERT INTO {Job.table} (dt, task_id, job_dt_fin, job_status, job_comment, job_project_id) VALUES "    
        sql += f"('{formatted_time}', {task_id}, '{formatted_time}', 'run', '', {project_id});"    
        return db.insert(sql)
        
    @staticmethod
    def truncate_jobs(*, db:Mysqldb) -> int:
        return db.delete(f"TRUNCATE TABLE {Job.table};")

    @staticmethod
    def delete_jobs(*, db:Mysqldb, status:str='', task_id:int=0, project_id:int=0) -> int:
        sql = f"DELETE FROM {Job.table}"
        sql_where = " WHERE 1=1"       
        if task_id:
            sql_where += f" AND task_id={task_id}"         
        if status:
            sql_where += f" AND job_status='{status}'"         
        if project_id>=0:
            sql_where += f" and job_project_id={project_id}"         
        if sql_where != " WHERE 1=1":    
            sql += sql_where          
        sql += ";"    
        return db.delete(sql)

    def get_info(self) -> list:
        sql = f"SELECT * from {self.table} where id={self.id};"     
        result = self.db.query(sql)
        if result[0]: 
            result = result[0]
            return result
        else:
            return None 

    def update_job(self, *, job_execution_sec:int=0, job_max_mem_kb:int=0, job_dt_fin:str='', job_status:int='', job_comment:str='') -> int:
        assert job_status in ['', 'run', 'fin', 'error'], 'Job.update_job: granularity options:  | run | fin | error'
        formatted_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = f"UPDATE {Job.table} set job_execution_sec={job_execution_sec},  job_max_mem_kb={job_max_mem_kb}, job_dt_fin='{formatted_time}', job_status='{job_status}'"
        if job_comment:
            sql += f", job_comment='{job_comment}'"
        sql += f" WHERE id={self.id};"
        return self.db.update(sql)
    