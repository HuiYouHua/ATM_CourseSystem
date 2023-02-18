# ========================
# Author: huayoyu
# Date: 2023/2/11
# 文件名： shop_interface
# ========================
'''
购物商城接口
'''

from db import db_hander
from lib import common

shop_logger = common.get_logger('shop')

# 商品准备结算接口
def shopping_interface(login_user, shopping_car):
    from interface import bank_interface

    # {'商品名称': ['单价', '数量']]}
    cost = 0
    for price_number in shopping_car.values():
        price, number = price_number

        cost += price * number

    flag, msg = bank_interface.pay_interface(login_user, cost)

    if flag:
        msg = f'用户：【{login_user}】支付 {cost}成功，准备发货！'
        shop_logger.info(msg)
        return True, msg

    return False, msg

# 购物车添加接口
def add_shop_car_interface(login_user, shopping_car):
    user_dic = db_hander.select(login_user)
    shop_car = user_dic['shop_car']

    for shop_name, price_number in shopping_car.items():
        number = price_number[1]

        if shop_name in shop_car:
            user_dic['shop_car'][shop_name] += number
        else:
            user_dic['shop_car'].update({shop_name: price_number})

    db_hander.save(user_dic)
    msg = '添加购物车成功！'
    shop_logger.info(msg)
    return True, msg

# 查看购物车接口
def check_shop_car_interface(login_user):
    user_dic = db_hander.select(login_user)
    return user_dic['shop_car']

