import sys
from PyQt5.QtWidgets import QApplication,QWidget
from login import Ui_login
from home import Ui_stuhome
from mssqldb import *

# 角色字典
roles = {"学生":"student","教师":"teacher","管理员":"admin"}


class Student:
    def __init__(self):
        self.id = ""
        self.db = db()

    def setup(self):
        command=f"select * from users where id='{self.id}'"
        self.db.query(command)
        self.info = self.db.cursor.fetchall()
        self.name = self.info[0][1]
        home.home_ui.id.setText(self.id)
        home.home_ui.name.setText(self.name)


class Login(QWidget):
    def __init__(self):
        super(Login, self).__init__()
        self.login_ui = Ui_login()
        self.login_ui.setupUi(self)
        #创建按钮事件，当点击登陆时，会调用登录方法
        self.login_ui.login.clicked.connect(self.login)
        self.show()

    def login(self):
        #从输入框接受登录数据
        id=self.login_ui.username.text()
        password=self.login_ui.password.text()
        role=self.login_ui.post.currentText()
        #对输入的账号进行过滤,密码无需过滤
        id=id.replace("'",'').replace('"','').replace('#','').replace('-','')
        id.strip()
        #从数据库中查询输入的账号、密码
        command = f"select * from {roles[role]} where id='{id}' and password='{password}'"
        try:
            student.db.query(command)
            if student.db.cursor.fetchall():
                student.id=self.login_ui.username.text()
                login.close()
                student.setup()
                home.show()
            else:
                login.login_ui.label_5.setText("账号或密码错误")
                login.show()
        except:
            login.login_ui.label_5.setText("输入非法字符串")
            print(command)
            login.show()


class Home(QWidget):
    def __init__(self):
        super(Home, self).__init__()
        self.home_ui = Ui_stuhome()
        self.home_ui.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    student = Student()
    login = Login()
    home = Home()
    sys.exit(app.exec_())
