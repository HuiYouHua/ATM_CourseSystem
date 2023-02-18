# ========================
# Author: huayoyu
# Date: 2023/2/11
# 文件名： common
# ========================
'''
存放公共方法
'''
import hashlib
from conf import setting
import logging.config

# MD5加密
def get_pwd_md5(password):
    md5_obj = hashlib.md5()
    md5_obj.update(password.encode('utf-8'))
    salt = '12345'
    md5_obj.update(salt.encode('utf-8'))
    return md5_obj.hexdigest()

# 登录装饰器
def login_auth(func):
    from core import src
    def inner(*args, **kwargs):
        if src.login_user:
            res = func(*args, **kwargs)
            return res
        else:
            print('用户未登录')
            src.login()

    return inner


import logging
# 添加日志功能
# 获取日志对象
def get_logger(log_type):
    '''
    :param log_type: 比如是 user日志，bank日志，购物商城日志
    :return:
    '''

    # 1、加载日志配置信息
    logging.config.dictConfig(
        setting.LOGGING_DIC
    )

    # 2、获取日志对象
    logger = logging.getLogger(log_type)

    return logger