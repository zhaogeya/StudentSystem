import os
import pymssql

# 学生
class Student:
    def __init__(self, no, name, chinese, math, english):
        self.no = no
        self.name = name
        self.chinese = int(chinese)
        self.math = int(math)
        self.english = int(english)


class StudentList:
    def __init__(self):
        self.stulist = []

    def __exists(self, no):
        # 判断学号是否存在
        for stu in self.stulist:
            if stu.no == no:
                return True
        else:
            return False

    def insert(self):
        stu_lst = []
        while True:
            no = int(input('请输入学号（例如1001）:'))
            if not no:
                break
            name = input('请输入姓名:')
            if not name:
                break
            try:
                c = int(input('请输入C语言成绩:'))
                python = int(input('请输入Python的成绩:'))
                java = int(input('请输入Java的成绩:'))
            except:
                print('输入无效，请重新输入！')
                continue
            student = {'id': no, 'name': name, 'C语言': c, 'Python': python, 'Java': java}
            stu_lst.append(student)
            self.save(filename)
            print('信息录入成功！')
            stu_lst.clear()
            choice = input('是否继续？y/n:')
            if choice == 'y' or choice == 'Y':
                continue
            else:
                break


    # 删除
    def delete(self):
        while True:
            student_id = int(input('请输入学生的id:'))
            if student_id:
                if os.path.exists(filename):
                    with open(filename, 'r', encoding='utf-8') as file:
                        student_old = file.readlines()
                else:
                    student_old = []
                flag = False
                if student_old:
                    with open(filename, 'w', encoding='utf-8') as files:
                        for item in student_old:
                            d = dict(eval(item))
                            if d['id'] != student_id:
                                files.write(str(d) + '\n')
                            else:
                                flag = True
                        if flag:
                            print(f'学号为{student_id}的学生信息已删除！')
                        else:
                            print(f'没有找到id为{student_id}的学生信息')
                else:
                    print('无学生记录')
                    break
                self.show()
                choice = input('是否继续？y/n:')
                if choice == 'y':
                    continue
                else:
                    break

    def show(self):
        student_lst = []
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                student = file.readlines()
                for item in student:
                    student_lst.append(eval(item))
                if student_lst:
                    self.show_student(student_lst)
        else:
            print('暂未保存学生数据！')

    # 修改
    def modify(self):
        self.show()
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                student_lst = file.readlines()
        else:
            return
        student_id = int(input('请输入学生id:'))
        with open(filename, 'w', encoding='utf-8') as file1:
            for item in student_lst:
                d = dict(eval(item))
                if d['id'] == student_id:
                    print(f'已经找到id为{student_id}的学生')
                    while True:
                        try:
                            d['name'] = input('请输入学生姓名:')
                            d['C语言'] = int(input('请输入C语言成绩:'))
                            d['Python'] = int(input('请输入Python的成绩:'))
                            d['Java'] = int(input('请输入Java的成绩:'))
                        except:
                            print('输入的信息有误，重新输入！！')
                        else:
                            break
                    file1.write(str(d) + '\n')
                    print('修改信息成功！！！！！！！')
                else:
                    file1.write(str(d) + '\n')
            switch = input('是否要修改信息？y/n:')
            if switch == 'y':
                self.modify()

    def load(self, fn):
        # 导入学生信息
        if os.path.exists(fn):
            try:
                with open(fn, 'r', encoding='utf-8') as fp:
                    while True:
                        fs = fp.readline().strip('\n')
                        if not fs:
                            break
                        else:
                            stu = Student(*fs.split(','))
                            if self.__exists(stu.no):
                                print('该学号已存在')
                            else:
                                self.stulist.append(stu)
                print('导入完毕')
            except:
                print('error...')  # 要导入的文件不是utf-8编码，或是字段数不匹配等
        else:
            print('要导入的文件不存在')

    def save(self, fn):
        # 导出学生信息
        with open(fn, 'w', encoding='utf-8') as fp:
            for stu in self.stulist:
                fp.write(stu.no + ',')
                fp.write(stu.name + ',')
                fp.write(str(stu.chinese) + ',')
                fp.write(str(stu.math) + ',')
                fp.write(str(stu.english) + '\n')
            print("导出完毕")

    def infoprocess(self):
        # 基本信息管理
        print('学生基本信息管理'.center(20, '-'))
        print('insert--------添加学生信息')
        print('delete--------删除学生信息')
        print('update--------修改学生信息')
        print('return--------返回')
        print('-' * 28)
        while True:
            s = input('info>').strip().lower()
            if s == 'insert':
                self.insert()
            elif s == 'delete':
                self.delete()
            elif s == 'update':
                self.update()
            elif s == 'return':
                break
            else:
                print('输入错误')

    def scoreprocess(self):
        # 学生成绩统计
        print('学生成绩统计'.center(24, '='))
        print('avg    --------课程平均分')
        print('max    --------课程最高分')
        print('min    --------课程最低分')
        print('return --------返回')
        print(''.center(30, '='))

    def main(self):
        # 主控函数
        while True:
            print('学生信息管理系统V1.0'.center(24, '='))
            print('info  -------学生基本信息管理')
            print('score -------学生成绩统计')
            print('exit  -------退出系统')
            print(''.center(32, '='))
            s = input('main>').strip().lower()
            if s == 'info':
                self.infoprocess()
            elif s == 'score':
                self.scoreprocess()
            elif s == 'exit':
                break
            else:
                print('输入错误')
# 选退课

# 审批
class ADCourse:
    def add_course(db, cursor):
        course = input('请输入你要插入的课程：')
        try:
            sql = "INSERT INTO course(c_name) VALUES ('%s')" % course
            cursor.execute(sql)
            db.commit()  # 执行插入语句
        except pymssql.err.IntegrityError:
            print('课程已经存在，不能重复！')
        else:
            print('添加成功')

    def delete_course(db, cursor):
        try:
            course = input('请输入你要删除的课程编号：')
            sql = f'DELETE FROM course WHERE c_id = %s ' % course
            cursor.execute(sql)
            db.commit()
        except:
            print('删除失败！')
        else:
            print('删除成功 ^_^')

if __name__ == '__main__':
    filename="./student.txt"
    st = StudentList()
    st.main()