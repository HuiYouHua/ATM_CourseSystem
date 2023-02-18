# ========================
# Author: huayoyu
# Date: 2023/2/12
# 文件名：admin_interface
# ========================

from db import db_hander
from lib import common

admin_logger = common.get_logger('admin')

# 修改额度接口
def change_balance_interface(username, money):
    user_dic = db_hander.select(username)

    if user_dic:
        user_dic['balance'] = int(money)
        db_hander.save(user_dic)

        msg = f'管理员修改用户：【{username}】额度修改成功！'
        admin_logger.info(msg)
        return True, msg

    return False, '修改额度用户不存在！'

# 冻结账户接口
def lock_user_interface(username):
    user_dic = db_hander.select(username)

    if user_dic:
        user_dic['locked'] = True
        db_hander.save(user_dic)
        msg = f'冻结账户【{username}】成功！'
        admin_logger.info(msg)
        return True, msg

    return False, '用户不存在！'
