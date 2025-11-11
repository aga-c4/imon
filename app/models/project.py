from models.mysqldb import Mysqldb

class Project:

    table = 'metric_projects'
    info = None
    id = None

    def __init__(self, *, db:Mysqldb, id:int):
        assert id > 0, 'Task.__init__: Tasks id is not set'
        self.db = db
        self.id = int(id)
        self.info = self.get_info()

    @staticmethod
    def get_project(*, db:Mysqldb, id:int=0):
        if not id:
            return None
        project = Project(db=db, id=id)
        if not project.info:
            return None
        return project

    @staticmethod
    def get_list(*, db:Mysqldb) -> list:
        active = int(active)
        sql = f"SELECT * from {Project.table};"       
        result = db.query(sql)
        return result  
    
    def get_info(self) -> dict:
        sql = f"SELECT * from {self.table} where id={self.id};"     
        result = self.db.query(sql)
        info = None
        if result: 
            info = result[0] 
        return info 
    