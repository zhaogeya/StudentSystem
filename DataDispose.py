#数据处理函数定义
def Login_dis(str):
    str = str.replace("'", '').replace('"', '').replace('#', '').replace('-', '')
    str.strip()
    return str

def Course_dis(lists):
    course=[]
    for dicts in lists:
        strs = ""
        for dict in dicts:
            strs=strs+' '+str(dict)
        course.append(strs)
    return course
