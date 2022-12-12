##教师申请课程模块
class Teacher:
    def __init__(self, name, password, dic_course=[]):
        self.name = name
        self.password = password
        self.dic_course = dic_course

    def add_course(self, password, course):
        """
        添加课程
        param password: 密码
        param course: 字符类型
        """
        if password == self.password:
            self.dic_course.append(course)
            print(f'{self.name}老师成功添加课程{course}')
            self.print_course()
            return self.dic_course
        return False

    def delete_course(self, password, course):
        if password == self.password:
            if isinstance(course, (str,)):
                try:
                    self.dic_course.remove(course)
                    print(f'{self.name}老师成功删除课程{course}')
                    self.print_course()
                    return self.dic_course
                except Exception:
                    print(f"不存在{course}课程")
            else:
                print("请输入正确的课程名字")

        return False

    def change_course(self, password, course, course_new):
        """
        修改课程表
        param password: 密码
        param course: 修改的课程
        param course_new: 修改后的课程
        """
        if password == self.password:
            if isinstance(course, (str,)):
                if self.dic_course.count(course) != 0:
                    try:
                        # 修改元素
                        for index_course in self.dic_course:
                            if index_course == course:
                                self.dic_course.remove(index_course)
                                self.dic_course.append(course_new)
                                print("修改成功")
                        return self.dic_course
                    except Exception:
                        print(f"不存在{course}课程")
                else:
                    print(f"不存在{course}课程")
            else:
                print("请输入正确的课程名字")

        return False

    def find_course(self, password):
        """
        查找课程
        param password:  密码
        """
        if password == self.password:
            self.print_course()
            return self.dic_course
        return False

    def close(self, password):
        if password == self.password:
            self.name = ''
            self.password = ''
            print('注销成功')
            return self.dic_course
        else:
            print('请输入正确的账户密码')

    def print_course(self):
        """
        输出课程函数
        """
        print("已有课程", end="")
        for index_course in self.dic_course:
            print(f'{index_course}', end=" ")


if __name__ == "__main__":
    test = Teacher(name="小明", password="123")
    test.add_course("123", course="软件工程")
    test.add_course("123", course="数据结构")
    # test.print_course()
    #test.delete_course("123", '数据结构')