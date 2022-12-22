import sys
from PyQt5.QtWidgets import QApplication,QWidget,QAbstractItemView,QHeaderView,QTableView
from login import Ui_login
from home import Ui_stuhome
from forget import Ui_forget
from mssqldb import *
from DataDispose import *
from PyQt5.QtGui import QStandardItemModel,QStandardItem

# 角色字典
roles = {"学生":"student","教师":"teacher","管理员":"admin"}
Page = {"学生":0,"教师":1,"管理员":2}


class User:
    def __init__(self):
        self.id = ""
        self.db = db()

    def setup(self):
        command=f"select * from users_info where id='{self.id}'"
        self.db.query(command)
        self.info = self.db.cursor.fetchall()
        # 为每个控件设置显示信息
        self.name = self.info[0][1]
        self.age = str(self.info[0][2])
        self.sex = self.info[0][3]
        self._class = self.info[0][4]
        self.phone = self.info[0][5]
        home.home_ui.id.setText(self.id)
        home.home_ui.name.setText(self.name)
        home.home_ui.age.setText(self.age)
        home.home_ui.sex.setText(self.sex)
        home.home_ui.class_.setText(self._class)
        home.home_ui.phone.setText(self.phone)


class Login(QWidget):
    def __init__(self):
        super(Login, self).__init__()
        self.login_ui = Ui_login()
        self.role=""
        self.login_ui.setupUi(self)
        # 创建按钮事件，当点击登陆时，会调用登录方法
        self.login_ui.login.clicked.connect(self.login)
        self.login_ui.modify.clicked.connect(self.MPassword)
        self.login_ui.forget.clicked.connect(self.forget)
        self.show()

    def login(self):
        # 从输入框接受登录数据
        id = self.login_ui.username.text()
        password = self.login_ui.password.text()
        self.role = self.login_ui.post.currentText()
        # 对输入的账号和密码进行过滤
        id = Login_dis(id)
        password = Login_dis(password)
        # 从数据库中查询输入的账号、密码
        if id and password:
            command = f"select * from users where id='{id}' and password='{password}' and role='{roles[self.role]}'"
            try:
                user.db.query(command)
                if user.db.cursor.fetchall():
                    user.id=Login_dis(self.login_ui.username.text())
                    login.close()
                    user.setup()
                    home.home_ui.stackedWidget_2.setCurrentIndex(Page[self.role])
                    home.connect(roles[self.role])
                    home.show()
                else:
                    login.login_ui.label_5.setText("账号或密码错误")
                    login.show()
            except:
                login.login_ui.label_5.setText("存在非法字符串")
                #print(command)
                login.show()
        else:
            login.login_ui.label_5.setText("请输入账号或密码")
            login.show()

    def MPassword(self):
        mpass.show()

    def forget(self):
        self.login_ui.label_5.setText("请联系管理员")

class Password(QWidget):
    def __init__(self):
        super(Password, self).__init__()
        self.passowrd=Ui_forget()
        self.passowrd.setupUi(self)
        self.passowrd.pushButton.clicked.connect(self.Modify)

    def Modify(self):
        id=self.passowrd.lineEdit.text()
        now_pass=Login_dis(self.passowrd.lineEdit_2.text())
        new_pass=Login_dis(self.passowrd.lineEdit_3.text())
        if id=='' or now_pass=='' or new_pass=='':
            pass
        else:
            command=f"select * from users where id={int(id)} and password='{now_pass}'"
            user.db.query(command)
            result=user.db.cursor.fetchall()
            if result:
                command=f"update users set password='{new_pass}' where id={int(id)}"
                user.db.query(command)
                self.passowrd.label_4.setText("修改成功")
            else:
                self.passowrd.label_4.setText("密码错误")

class Home(QWidget):
    def __init__(self):
        super(Home, self).__init__()
        self.home_ui = Ui_stuhome()
        self.home_ui.setupUi(self)
        self.home_ui.pushButton.clicked.connect(self.SelectCourse)
        self.home_ui.pushButton_2.clicked.connect(self.ExitCoure)
        self.home_ui.pushButton_3.clicked.connect(self.Commit)
        self.home_ui.pushButton_4.clicked.connect(self.Pass)
        self.home_ui.pushButton_5.clicked.connect(self.NoPass)
        self.home_ui.pushButton_11.clicked.connect(self.Delect)
        self.home_ui.pushButton_17.clicked.connect(self.Score_Add)
        self.home_ui.pushButton_6.clicked.connect(self.Score_Query)
        self.home_ui.pushButton_7.clicked.connect(self.Score_Modify)
        self.home_ui.pushButton_20.clicked.connect(self.Info_Query)
        self.home_ui.pushButton_18.clicked.connect(self.Info_Modify)
        self.home_ui.pushButton_19.clicked.connect(self.Info_Add)
        self.home_ui.pushButton_8.clicked.connect(self.Score_Del)

    def connect(self,role):
        # 连接信号槽，当选中一个项时，调用action函数
        if role == "student":
            self.home_ui.SystemSet.activated.connect(self.action_System_0)
            self.home_ui.CourseSelection.activated.connect(self.action_Course_0)
            self.home_ui.ScoreManager.activated.connect(self.action_Score_0)
        elif role == "teacher":
            self.home_ui.SystemSet_2.activated.connect(self.action_System_1)
            self.home_ui.CourseSelection_2.activated.connect(self.action_Course_1)
            self.home_ui.ScoreManager_2.activated.connect(self.action_Score_1)
        elif role == "admin":
            self.home_ui.SystemSet_3.activated.connect(self.action_System_2)
            self.home_ui.CourseSelection_3.activated.connect(self.action_Course_2)
            self.home_ui.ScoreManager_3.activated.connect(self.action_Score_2)
            self.home_ui.Info_System.activated.connect(self.info_System)

    def SelectCourse(self):
        row=self.home_ui.tableView_2.currentIndex().row()
        cid=self.home_ui.tableView_2.model().itemData(self.home_ui.tableView_2.model().index(row,0))[0]
        id=int(user.id)
        command=f"begin transaction;insert into cselection values('{cid}', {id});commit transaction;"
        user.db.query(command)


    def ExitCoure(self):
        row = self.home_ui.tableView_4.currentIndex().row()
        cid = self.home_ui.tableView_4.model().itemData(self.home_ui.tableView_4.model().index(row, 0))[0]
        id = int(user.id)
        command = f"begin transaction;delete from cselection where Cid='{cid}' and sid={id};commit transaction;"
        user.db.query(command)

    def Commit(self):
        cid=self.home_ui.lineEdit.text()
        ctime=self.home_ui.lineEdit_2.text()
        cname=self.home_ui.lineEdit_3.text()
        cplace=self.home_ui.lineEdit_4.text()
        command = "begin transaction;insert into courses values(%d,'%s','%s','%s','%s','0',%d);" \
                  "commit transaction;" %(int(cid),cname,user.name,ctime,cplace,int(user.id))
        user.db.query(command)

    def Pass(self):
        row = self.home_ui.tableView_7.currentIndex().row()
        cid = self.home_ui.tableView_7.model().itemData(self.home_ui.tableView_7.model().index(row, 0))[0]
        command = f"begin transaction;update courses set status=1 where Cid={int(cid)};commit transaction;"
        user.db.query(command)

    def NoPass(self):
        row = self.home_ui.tableView_7.currentIndex().row()
        cid = self.home_ui.tableView_7.model().itemData(self.home_ui.tableView_7.model().index(row, 0))[0]
        command = f"begin transaction;delete from courses where Cid={int(cid)};commit transaction;"
        user.db.query(command)

    def Delect(self):
        row = self.home_ui.tableView_15.currentIndex().row()
        cid = self.home_ui.tableView_15.model().itemData(self.home_ui.tableView_15.model().index(row, 0))[0]
        command = f"begin transaction;delete from courses where Cid={int(cid)};commit transaction;"
        user.db.query(command)

    def Score_Add(self):
        cid=self.home_ui.lineEdit_16.text()
        sid=self.home_ui.lineEdit_17.text()
        score=self.home_ui.lineEdit_15.text()
        if cid=='' or sid=='' or score=='':
            self.home_ui.label_39.setText("请输入信息")
        else:
            self.home_ui.label_39.clear()
            command=f"select Cname from courses where Cid={cid}"
            user.db.query(command)
            result=user.db.cursor.fetchall()
            cname=result[0][0]
            command = f"begin transaction;insert into scores values({int(cid)},{int(sid)},'{cname}',{score});commit transaction;"
            user.db.query(command)


    def Score_Query(self):
        cid=self.home_ui.lineEdit_5.text()
        sid=self.home_ui.lineEdit_6.text()
        if cid=='' and sid=='':
            pass
        else:
            if cid=='':
                user.db.query(f"select Cid,Sid,Cname,score from scores where Sid={int(sid)}")
            elif sid=='':
                user.db.query(f"select Cid,Sid,Cname,score from scores where Cid={int(cid)}")
            else:
                user.db.query(f"select Cid,Sid,Cname,score from scores where Cid={int(cid)} and Sid={int(sid)}")
            courses = user.db.cursor.fetchall()
            model = QStandardItemModel(0, 4)
            model.setHorizontalHeaderLabels(['课程编号', '学号', '课程名', '分数'])
            self.home_ui.tableView_18.setModel(model)
            self.home_ui.tableView_18.horizontalHeader().setStretchLastSection(True)
            self.home_ui.tableView_18.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只能选中一行
            self.home_ui.tableView_18.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.home_ui.tableView_18.setEditTriggers(QTableView.NoEditTriggers)  # 不可编辑
            for course in courses:
                model.appendRow([QStandardItem(str(tcourse)) for tcourse in course])

    def Score_Modify(self):
        try:
            self.home_ui.label_38.clear()
            row = self.home_ui.tableView_18.currentIndex().row()
            cid = self.home_ui.tableView_18.model().itemData(self.home_ui.tableView_18.model().index(row, 0))[0]
            sid = self.home_ui.tableView_18.model().itemData(self.home_ui.tableView_18.model().index(row, 2))[0]
            score=self.home_ui.lineEdit_7.text()
            command = f"begin transaction;update scores set score={int(score)} where Cid={int(cid)} and Sid={int(sid)};commit transaction;"
            user.db.query(command)
        except:
            self.home_ui.label_38.setText("请选择一个课程或输入一个分数")

    def Score_Del(self):
        try:
            self.home_ui.label_38.clear()
            row = self.home_ui.tableView_18.currentIndex().row()
            cid = self.home_ui.tableView_18.model().itemData(self.home_ui.tableView_18.model().index(row, 0))[0]
            sid = self.home_ui.tableView_18.model().itemData(self.home_ui.tableView_18.model().index(row, 2))[0]
            score=self.home_ui.lineEdit_7.text()
            command = f"begin transaction;delete from scores where Cid={int(cid)} and Sid={int(sid)};commit transaction;"
            user.db.query(command)
        except:
            self.home_ui.label_38.setText("请选择一个课程")

    def Info_Query(self):
        sid = self.home_ui.lineEdit_19.text()
        if sid == '':
            pass
        else:
            user.db.query(f"select id,name,sex,age,class,phone from users_info where id={int(sid)}")
            infos = user.db.cursor.fetchall()
            model = QStandardItemModel(0, 6)
            model.setHorizontalHeaderLabels(['学号', '姓名', '性别', '年龄','班级','联系方式'])
            self.home_ui.tableView_22.setModel(model)
            self.home_ui.tableView_22.horizontalHeader().setStretchLastSection(True)
            self.home_ui.tableView_22.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只能选中一行
            self.home_ui.tableView_22.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.home_ui.tableView_22.setEditTriggers(QTableView.NoEditTriggers)  # 不可编辑
            for info in infos:
                model.appendRow([QStandardItem(str(tinfo)) for tinfo in info])

    def Info_Modify(self):
        try:
            self.home_ui.label_37.clear()
            row = self.home_ui.tableView_22.currentIndex().row()
            sid = self.home_ui.tableView_22.model().itemData(self.home_ui.tableView_22.model().index(row, 0))[0]
            name=self.home_ui.lineEdit_20.text()
            sex=self.home_ui.lineEdit_21.text()
            age=self.home_ui.lineEdit_18.text()
            class_=self.home_ui.lineEdit_23.text()
            phone=self.home_ui.lineEdit_22.text()
            if name!='':
                command = f"begin transaction;update users_info set name={name} where id={int(sid)};commit transaction;"
                user.db.query(command)
            if sex!='':
                command = f"begin transaction;update users_info set sex={sex} where id={int(sid)};commit transaction;"
                user.db.query(command)
            if age!='':
                command = f"begin transaction;update users_info set age={age} where id={int(sid)};commit transaction;"
                user.db.query(command)
            if class_!='':
                command = f"begin transaction;update users_info set class={class_} where id={int(sid)};commit transaction;"
                user.db.query(command)
            if phone!='':
                command = f"begin transaction;update users_info set phone={phone} where id={int(sid)};commit transaction;"
                user.db.query(command)
        except:
            self.home_ui.label_37.setText("请选择一个学生")

    def Info_Add(self):
        name = self.home_ui.lineEdit_27.text()
        sid = self.home_ui.lineEdit_25.text()
        sex = self.home_ui.lineEdit_26.text()
        age = self.home_ui.lineEdit_24.text()
        class_ = self.home_ui.lineEdit_28.text()
        phone = self.home_ui.lineEdit_29.text()
        role=roles[self.home_ui.post.currentText()]
        if sid == '' or name == '' or sex == '' or age=='' or class_=='' or phone=='' or role=='':
            self.home_ui.label_40.setText("请输入完整信息")
        else:
            self.home_ui.label_40.clear()
            command = f"begin transaction;insert into users_info values" \
                      f"({int(sid)},'{name}','{age}','{sex}','{class_}','{phone}');commit transaction;"
            user.db.query(command)
            command = f"insert into users values('{sid}','123456','{role}')"
            user.db.query(command)

    def action_System_0(self):
        # 获取选中项的索引
        result = self.home_ui.SystemSet.currentIndex().row()
        if result == 1:                                     # 如果选中第二个，则退出
            self.close()
        elif result == 0:                                   # 如果选中第一个，则返回首页
            self.home_ui.stackedWidget.setCurrentIndex(0)

    def action_Course_0(self):
        #获取选中项的索引
        result = self.home_ui.CourseSelection.currentIndex().row()
        if result == 0:
            user.db.query("select Cid,Cname,Cteacher,Ctime,Cplace from courses where status=1")
            lists=user.db.cursor.fetchall()
            model = QStandardItemModel(0, 5)
            model.setHorizontalHeaderLabels(['课程编号', '课程名', '教师','上课时间','上课地点'])
            self.home_ui.tableView_2.setModel(model)
            self.home_ui.tableView_2.horizontalHeader().setStretchLastSection(True)
            self.home_ui.tableView_2.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只能选中一行
            self.home_ui.tableView_2.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置只能选中整行
            self.home_ui.tableView_2.setEditTriggers(QTableView.NoEditTriggers)  # 不可编辑
            for list in lists:
                model.appendRow([QStandardItem(str(course)) for course in list])
            self.home_ui.stackedWidget.setCurrentIndex(3)   # 如果选中第一个，则跳转到选课界面
        elif result == 2:
            user.db.query(f"select Cid,Cname,Cteacher,Ctime,Cplace from courses where Cid in ("
                          f"select Cid from cselection where sid='{user.id}')")
            courses = user.db.cursor.fetchall()
            model = QStandardItemModel(0, 5)
            model.setHorizontalHeaderLabels(['课程编号', '课程名', '教师', '上课时间', '上课地点'])
            self.home_ui.tableView_3.setModel(model)
            self.home_ui.tableView_3.horizontalHeader().setStretchLastSection(True)
            self.home_ui.tableView_3.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只能选中一行
            self.home_ui.tableView_3.setEditTriggers(QTableView.NoEditTriggers)  # 不可编辑
            for course in courses:
                model.appendRow([QStandardItem(str(tcourse)) for tcourse in course])
            self.home_ui.stackedWidget.setCurrentIndex(2)  # 如果选中第一个，则跳转到选课界面
        elif result == 1:
            user.db.query(f"select Cid,Cname,Cteacher,Ctime,Cplace from courses where Cid in ("
                          f"select Cid from cselection where sid='{user.id}')")
            courses = user.db.cursor.fetchall()
            model = QStandardItemModel(0, 5)
            model.setHorizontalHeaderLabels(['课程编号', '课程名', '教师', '上课时间', '上课地点'])
            self.home_ui.tableView_4.setModel(model)
            self.home_ui.tableView_4.horizontalHeader().setStretchLastSection(True)
            self.home_ui.tableView_4.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只能选中一行
            self.home_ui.tableView_4.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.home_ui.tableView_4.setEditTriggers(QTableView.NoEditTriggers)  # 不可编辑
            for course in courses:
                model.appendRow([QStandardItem(str(tcourse)) for tcourse in course])
            self.home_ui.stackedWidget.setCurrentIndex(4)  # 如果选中第一个，则跳转到选课界面
    def action_Score_0(self):
        # 获取选中项的索引
        result=self.home_ui.ScoreManager.currentIndex().row()
        if result==0:
            user.db.query(f"select Cid,Cname,score from scores where Sid={user.id}")
            scores=user.db.cursor.fetchall()
            model=QStandardItemModel(0,3)
            model.setHorizontalHeaderLabels(['课程编号','课程名','分数'])
            self.home_ui.tableView.setModel(model)
            self.home_ui.tableView.horizontalHeader().setStretchLastSection(True)
            self.home_ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自动填充
            self.home_ui.tableView.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只能选中一行
            self.home_ui.tableView.setEditTriggers(QTableView.NoEditTriggers)  # 不可编辑
            for score in scores:
                model.appendRow([QStandardItem(str(course)) for course in score])
            self.home_ui.stackedWidget.setCurrentIndex(1)

    def action_System_1(self):
        # 获取选中项的索引
        result = self.home_ui.SystemSet_2.currentIndex().row()
        if result == 1:  # 如果选中第二个，则退出
            self.close()
        elif result == 0:  # 如果选中第一个，则返回首页
            self.home_ui.stackedWidget.setCurrentIndex(0)

    def action_Course_1(self):
        # 获取选中项的索引
        result = self.home_ui.CourseSelection_2.currentIndex().row()
        if result == 0:
            self.home_ui.stackedWidget.setCurrentIndex(5)  # 如果选中第一个，则跳转到开课界面
        elif result == 1:
            user.db.query(f"select Cid,Cname,Ctime,Cplace,status from courses where Tid={user.id}")
            scores = user.db.cursor.fetchall()
            model = QStandardItemModel(0, 5)
            model.setHorizontalHeaderLabels(['课程编号', '课程名', '上课时间','上课地点','课程申请情况'])
            self.home_ui.tableView_5.setModel(model)
            self.home_ui.tableView_5.horizontalHeader().setStretchLastSection(True)
            #self.home_ui.tableView_5.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自动填充
            self.home_ui.tableView_5.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只能选中一行
            self.home_ui.tableView_5.setEditTriggers(QTableView.NoEditTriggers)  # 不可编辑
            for score in scores:
                model.appendRow([QStandardItem(str(course)) for course in score])
            self.home_ui.stackedWidget.setCurrentIndex(6)  # 如果选中第一个，则跳转到课表

    def action_Score_1(self):
        # 获取选中项的索引
        result = self.home_ui.ScoreManager_2.currentIndex().row()
        if result == 0:
            user.db.query(f"select courses.Cid,courses.Cname,class,Sid,name,score"
                          f" from courses INNER JOIN scores ON courses.Cid=scores.Cid"
                          f" INNER JOIN users_info ON users_info.id=scores.Sid where Tid='{user.id}'")
            scores = user.db.cursor.fetchall()
            model = QStandardItemModel(0, 6)
            model.setHorizontalHeaderLabels(['课程编号','课程名','班级','学生学号','学生姓名','学生成绩'])
            self.home_ui.tableView_6.setModel(model)
            self.home_ui.tableView_6.horizontalHeader().setStretchLastSection(True)
            self.home_ui.tableView_6.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只能选中一行
            self.home_ui.tableView_6.setEditTriggers(QTableView.NoEditTriggers)  # 不可编辑
            for score in scores:
                model.appendRow([QStandardItem(str(course)) for course in score])
            self.home_ui.stackedWidget.setCurrentIndex(7)  # 如果选中第一个，则跳转到显示课程

    def action_System_2(self):
        # 获取选中项的索引
        result = self.home_ui.SystemSet_3.currentIndex().row()
        if result == 1:                                     # 如果选中第二个，则退出
            self.close()
        elif result == 0:                                   # 如果选中第一个，则返回首页
            self.home_ui.stackedWidget.setCurrentIndex(0)

    def action_Course_2(self):
        # 获取选中项的索引
        result = self.home_ui.CourseSelection_3.currentIndex().row()
        if result == 0:
            user.db.query(
                f"select Cid,cname,Tid,Cteacher,Ctime,Cplace from courses where status=0")
            scores = user.db.cursor.fetchall()
            model = QStandardItemModel(0, 6)
            model.setHorizontalHeaderLabels(['课程编号', '课程名','教师编号','教师姓名','上课时间','上课地点'])
            self.home_ui.tableView_7.setModel(model)
            self.home_ui.tableView_7.horizontalHeader().setStretchLastSection(True)
            self.home_ui.tableView_7.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置只能选中整行
            self.home_ui.tableView_7.setEditTriggers(QTableView.NoEditTriggers)  # 不可编辑
            for score in scores:
                model.appendRow([QStandardItem(str(course)) for course in score])
            self.home_ui.stackedWidget.setCurrentIndex(8)   # 如果选中第一个，则跳转到课程审批
        elif result == 1:
            user.db.query(
                f"select Cid,cname,Tid,Cteacher,Ctime,Cplace from courses where status=1")
            scores = user.db.cursor.fetchall()
            model = QStandardItemModel(0, 6)
            model.setHorizontalHeaderLabels(['课程编号', '课程名', '教师编号', '教师姓名', '上课时间', '上课地点'])
            self.home_ui.tableView_15.setModel(model)
            self.home_ui.tableView_15.horizontalHeader().setStretchLastSection(True)
            self.home_ui.tableView_15.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置只能选中整行
            self.home_ui.tableView_15.setEditTriggers(QTableView.NoEditTriggers)  # 不可编辑
            for score in scores:
                model.appendRow([QStandardItem(str(course)) for course in score])
            self.home_ui.stackedWidget.setCurrentIndex(9)  # 如果选中第一个，则跳转到课程删除
        elif result == 2:
            user.db.query(
                f"select Cid,cname,Tid,Cteacher,Ctime,Cplace,status from courses")
            scores = user.db.cursor.fetchall()
            model = QStandardItemModel(0, 7)
            model.setHorizontalHeaderLabels(['课程编号', '课程名', '教师编号', '教师姓名', '上课时间', '上课地点','申请状态'])
            self.home_ui.tableView_16.setModel(model)
            self.home_ui.tableView_16.horizontalHeader().setStretchLastSection(True)
            self.home_ui.tableView_16.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置只能选中整行
            self.home_ui.tableView_16.setEditTriggers(QTableView.NoEditTriggers)  # 不可编辑
            for score in scores:
                model.appendRow([QStandardItem(str(course)) for course in score])
            self.home_ui.stackedWidget.setCurrentIndex(10)  # 如果选中第一个，则跳转到课程总览

    def action_Score_2(self):
        # 获取选中项的索引
        result=self.home_ui.ScoreManager_3.currentIndex().row()
        if result==0:
            user.db.query(f"select Cid,Cname,sid,score from scores")
            scores = user.db.cursor.fetchall()
            model = QStandardItemModel(0, 4)
            model.setHorizontalHeaderLabels(['课程编号', '课程名','学号','分数'])
            self.home_ui.tableView_18.setModel(model)
            self.home_ui.tableView_18.horizontalHeader().setStretchLastSection(True)
            # self.home_ui.tableView_18.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自动填充
            self.home_ui.tableView_18.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只能选中一行
            self.home_ui.tableView_18.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置只能选中整行
            self.home_ui.tableView_18.setEditTriggers(QTableView.NoEditTriggers)  # 不可编辑
            for score in scores:
                model.appendRow([QStandardItem(str(course)) for course in score])
            self.home_ui.stackedWidget.setCurrentIndex(12)
        elif result==1:
            user.db.query(f"select Cid,Cname,sid,score from scores")
            scores = user.db.cursor.fetchall()
            model = QStandardItemModel(0, 4)
            model.setHorizontalHeaderLabels(['课程编号', '课程名', '学号', '分数'])
            self.home_ui.tableView_21.setModel(model)
            self.home_ui.tableView_21.horizontalHeader().setStretchLastSection(True)
            # self.home_ui.tableView_21.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自动填充
            self.home_ui.tableView_21.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只能选中一行
            self.home_ui.tableView_21.setEditTriggers(QTableView.NoEditTriggers)  # 不可编辑
            for score in scores:
                model.appendRow([QStandardItem(str(course)) for course in score])
            self.home_ui.stackedWidget.setCurrentIndex(11)

    def info_System(self):
        result = self.home_ui.Info_System.currentIndex().row()
        if result==0:
            user.db.query(f"select id,name,sex,age,class,phone from users_info")
            scores = user.db.cursor.fetchall()
            model = QStandardItemModel(0, 6)
            model.setHorizontalHeaderLabels(['学号', '姓名','性别','年龄','班级','联系方式'])
            self.home_ui.tableView_22.setModel(model)
            self.home_ui.tableView_22.horizontalHeader().setStretchLastSection(True)
            # self.home_ui.tableView_22.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自动填充
            self.home_ui.tableView_22.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只能选中一行
            self.home_ui.tableView_22.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置只能选中整行
            self.home_ui.tableView_22.setEditTriggers(QTableView.NoEditTriggers)  # 不可编辑
            for score in scores:
                model.appendRow([QStandardItem(str(course)) for course in score])
            self.home_ui.stackedWidget.setCurrentIndex(13)
        elif result==1:
            user.db.query(f"select id,name,sex,age,class,phone from users_info")
            scores = user.db.cursor.fetchall()
            model = QStandardItemModel(0, 6)
            model.setHorizontalHeaderLabels(['学号', '姓名', '性别', '年龄', '班级', '联系方式'])
            self.home_ui.tableView_23.setModel(model)
            self.home_ui.tableView_23.horizontalHeader().setStretchLastSection(True)
            self.home_ui.tableView_23.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只能选中一行
            self.home_ui.tableView_23.setEditTriggers(QTableView.NoEditTriggers)  # 不可编辑
            for score in scores:
                model.appendRow([QStandardItem(str(course)) for course in score])
            self.home_ui.stackedWidget.setCurrentIndex(14)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mpass=Password()
    user = User()
    login = Login()
    home = Home()
    sys.exit(app.exec_())
