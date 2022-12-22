import pyodbc

class db:
    def __init__(self):
        db=pyodbc.connect('DRIVER={sql server};SERVER=127.0.0.1,1433;DATABASE=StudentSystem;UID=sa;PWD=123456')
        db.autocommit=True
        self.cursor=db.cursor()

    def query(self,command):
        self.cursor.execute(command)


# if __name__ == '__main__':
#     db=db()
#     db.query("insert into cselection values('10', 1003);commit")
