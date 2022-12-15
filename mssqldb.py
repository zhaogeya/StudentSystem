import pymssql

class db:
    def __init__(self):
        db=pymssql.connect(server="127.0.0.1",user="sa",password="123456",database="StudentSystem")
        self.cursor=db.cursor()

    def query(self,command):
        self.cursor.execute(command)


# if __name__ == '__main__':
#     db=db()
#     command=f"select * from users where id='20200001'"
#     db.query(command)
#     print(db.cursor.fetchall())
