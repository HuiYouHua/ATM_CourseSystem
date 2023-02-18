# ========================
# Author: huayoyu
# Date: 2023/2/11
# 文件名： bank_interface
# ========================
'''
银行相关业务的接口
'''
from db import db_hander
from lib import common

bank_logger = common.get_logger('bank')

# 提现接口（手续费5%）
def withdraw_interface(username, money):
    user_dic = db_hander.select(username)
    balance = int(user_dic['balance'])
    money2 = int(money) * 1.05

    if balance >= money2:
        user_dic['balance'] = balance - money2

        flow = f'用户【{username}】提现金额【{money}】成功，手续费为【{int(money)*0.05}】'
        user_dic['flow'].append(flow)

        db_hander.save(user_dic)

        bank_logger.info(flow)
        return True, flow
    else:
        return False, '余额不足！'

# 还款接口
def repay_interface(username, money):
    user_dic = db_hander.select(username)
    user_dic['balance'] += money

    flow = f'用户：【{username}】 还款：【{money}】成功！'
    user_dic['flow'].append(flow)
    db_hander.save(user_dic)
    bank_logger.info(flow)
    return True, flow

# 转账接口
def transfer_interface(login_user, to_user, money):
    login_user_dic = db_hander.select(login_user)
    to_user_dic = db_hander.select(to_user)

    if not to_user_dic:
        return False, '目标用户不存在'

    if login_user_dic['balance'] >= money:
        login_user_dic['balance'] -= money
        to_user_dic['balance'] += money

        login_user_flow = f'用户：【{login_user}】给 用户：【{to_user}】转账【{money}】成功'
        login_user_dic['flow'].append(login_user_flow)

        to_user_flow = f'用户：【{to_user}】接收到 用户：【{login_user}】转账【{money}】成功'
        to_user_dic['flow'].append(to_user_flow)

        db_hander.save(login_user_dic)
        db_hander.save(to_user_dic)
        bank_logger.info(login_user_flow)
        return True, login_user_flow
    else:
        return False, f'用户：【{login_user}】余额不足'

# 查看流水接口
def check_flow_interface(login_user):
    user_dic = db_hander.select(login_user)
    return user_dic['flow']

# 支付接口
def pay_interface(login_user, cost):
    user_dic = db_hander.select(login_user)

    if not user_dic:
        return False, '目标用户不存在'

    if user_dic['balance'] >= cost:
        user_dic['balance'] -= cost

        flow = f'用户消费金额：【{cost}】'
        user_dic['flow'].append(flow)

        db_hander.save(user_dic)

        return True, '支付成功！'
    return False, '余额不足！'