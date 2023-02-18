# ========================
# Author: huayoyu
# Date: 2023/2/11
# 文件名： user_interface
# ========================
'''
用户接口层
'''
import json
import os
from conf import setting
from db import db_hander
from lib import common

user_logger = common.get_logger('user')

# 注册接口
def register_interface(username, password, balance = 15000):
    # 查看用户是否存在
    user_dic = db_hander.select(username)
    if user_dic:
        return False, '用户名已存在！'

    password = common.get_pwd_md5(password)
    user_dic = {
        'username': username,
        'password': password,
        'balance': balance,
        'flow': [],
        'shop_car': {},
        'locked': False
    }

    db_hander.save(user_dic)

    msg = f'{username}注册成功！'
    user_logger.info(msg)
    return True, msg

# 登录接口
def login_interface(username, password):
    # 查看用户是否存在
    user_dic = db_hander.select(username)

    if user_dic:
        if user_dic['locked']:
            return False, '当前账户被冻结'

        # 校验密码
        password = common.get_pwd_md5(password)
        if password == user_dic.get('password'):
            msg = f'用户：【{username}】登录成功！'
            user_logger.info(msg)
            return True, msg
        else:
            msg = f'用户：【{username}】密码错误！'
            user_logger.warn(msg)
            return False, msg

    msg = f'用户：【{username}】不存在，请重新输入！'
    user_logger.warn(msg)
    return False, msg

# 查看余额接口
def check_bal_interface(username):
    user_dic = db_hander.select(username)
    return user_dic['balance']






