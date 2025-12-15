from models.mysqldb import Mysqldb

class Project:

    table = 'metric_projects'
    info = None
    id = None

    def __init__(self, *, db:Mysqldb, id:int=0):
        self.db = db
        self.id = int(id)
        self.info = self.get_info()
        if self.info is None:
            self.id = 0
            self.info = {
                "id": 0,
                "active": 0,
                "metric_project_alias": "Def",
                "metric_project_name": "Def"
            }

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
    