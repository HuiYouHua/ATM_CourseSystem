'''
学生接口层
'''
from db import models


# 学生注册接口
def student_register_interface(user, pwd):
    # 1.判断用户是否存在
    # 调用Student类中的，select方法，
    # 由该方法去调用db_handler中的select_data功能获取对象
    student_obj = models.Student.select(user)

    # 1.1) 若存在不允许注册，返回用户已存在给视图层
    if student_obj:
        return False, '学生用户已存在!'

    # 1.2) 若不存在则允许注册，调用类实例化得到对象并保存
    student_obj = models.Student(user, pwd)
    # 对象调用save() 会将 admin_obj传给save方法
    student_obj.save()

    return True, '注册成功!'


# 学生登录接口
'''
def student_login_interface(user, pwd):
    # 1.判断用户是否存在
    student_obj = models.Student.select(user)

    # 2.若不存在，则证明用户不存在并返回给视图层
    if not student_obj:
        return False, '用户名不存在!'

    # 3.若用户存在，则校验密码
    if pwd == student_obj.pwd:
        return True, '登录成功! '
    else:
        return False, '密码错误!'
'''


# 学生选择学校接口
def add_school_interface(school_name, student_name):
    # 1、判断当前学生是否存在学校
    student_obj = models.Student.select(student_name)

    if student_obj.school:
        return False, '当前学生已经选择过学校了!'

    # 2、若不存在学校，则给调用学生对象中选择学校的方法，实现学生添加学校
    student_obj.add_school(school_name)
    return True, '选择学校成功!'


# 获取学生所在学校所有课程接口
def get_course_list_interface(student_name):
    # 1、获取当前学生对象
    student_obj = models.Student.select(student_name)
    school_name = student_obj.school
    # 2、判断当前学生是有学校，若没有则返回False
    if not school_name:
        return False, '没有学校，请先选择学校'

    # 3、开始获取学校对象中的课程列表
    school_obj = models.School.select(school_name)

    # 3.1、判断当前学校中是否有课程，若没有，则联系管理员
    course_list = school_obj.course_list
    if not course_list:
        return False, '没有课程，请先联系管理员创建'

    # 3.2、若有则，返回课程列表
    return True, course_list


# 学生选择学校接口
def add_course_interface(course_name, student_name):
    # 1、先判断当前课程是否已经存在学生课程列表中
    student_obj = models.Student.select(student_name)

    if course_name in student_obj.course_list:
        return False, '该课程已经选择过了!'

    # 2、调用学生对象中添加课程的方法
    student_obj.add_course(course_name)

    return True, f'[{course_name}] -- 课程添加成功!'


# 学生会查看分数接口
def check_score_interface(student_name):
    student_obj = models.Student.select(student_name)
    if student_obj.score_dict:
        return student_obj.score_dict
