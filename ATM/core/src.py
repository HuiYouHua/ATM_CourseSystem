# ========================
# Author: huayoyu
# Date: 2023/2/11
# 文件名： src
# ========================
'''
用户视图层
'''
import os.path
from interface import user_interface, bank_interface, shop_interface
from lib import common

# 记录用户是否登录
login_user = None

# 1、注册功能
# 面条版
'''def register():
    while True:
        username = input("请输入用户名：").strip()
        password = input("请输入密码：").strip()
        re_password = input("请确认密码：").strip()

        if password == re_password:
            # 接收到注册之后的结果
            import json
            from conf import setting
            user_path = os.path.join(
                setting.USER_PATH_PATH, f'{username}.json'
            )

            if os.path.exists(user_path):
                with open(user_path, 'r', encoding='utf-8') as f:
                    user_dic = json.load(f)

                if user_dic:
                    print('用户已存在，请重新输入！')
                    continue

            user_dic = {
                'username': username,
                'password': password,
                'blance': 15000,
                'flow': [],
                'shop_car': {},
                'locked': False
            }

            with open(user_path, 'w', encoding='utf-8') as f:
                json.dump(user_dic, f, ensure_ascii=False)'''

# 分层版
def register():
    while True:
        username = input("请输入用户名：").strip()
        password = input("请输入密码：").strip()
        re_password = input("请确认密码：").strip()

        if password == re_password:
            falg, msg = user_interface.register_interface(username, password)
            if falg:
                print(msg)
                break
            else:
                print(msg)


# 2、登录功能
def login():
    while True:
        username = input("请输入用户名：").strip()
        password = input("请输入密码：").strip()

        flag, msg = user_interface.login_interface(username, password)
        if flag:
            print(msg)
            global login_user
            login_user = username
            break
        else:
            print(msg)

# 3、查看余额
@common.login_auth
def check_balance():
    balance = user_interface.check_bal_interface(login_user)
    print(f'用户{login_user} 账户余额为：{balance}')

# 4、提现功能
@common.login_auth
def withdraw():
    while True:
        input_money = input('请输入提现金额：').strip()

        if not input_money.isdigit():
            print('请重新输入')
            break

        flag, msg = bank_interface.withdraw_interface(login_user, input_money)

        if flag:
            print(msg)
            break
        else:
            print(msg)

# 5、还款功能
@common.login_auth
def repay():
    while True:
        input_money = input('请输入需要还款的金额：').strip()
        if not input_money.isdigit():
            print('请输入正确的金额')
            continue

        input_money = int(input_money)
        if input_money > 0:
            flag, msg = bank_interface.repay_interface(login_user, input_money)
            if flag:
                print(msg)
                break
        else:
            print('输入的金额不能小于0')


# 6、转账功能
@common.login_auth
def transfer():
    while True:
        to_user = input('请输入转账目标用户：').strip()
        money = input('请输入转账金额：').strip()

        if not money.isdigit():
            print('请输入正确的金额！')
            continue

        money = int(money)

        if money > 0:
            flag, msg = bank_interface.transfer_interface(login_user, to_user, money)
            if flag:
                print(msg)
                break
            else:
                print(msg)
        else:
            print('输入的金额不能小于0')

# 7、查看流水
@common.login_auth
def check_flow():
    flow_list = bank_interface.check_flow_interface(login_user)
    if flow_list:
        for flow in flow_list:
            print(flow)
    else:
        print('当前用户没有流水！')

# 8、购物功能
@common.login_auth
def shopping():
    shop_list = [
        ['上海灌汤包', 30],  # 0
        ['矮跟写真抱枕', 250],  # 1
        ['广东凤爪', 28],
        ['香港地道鱼丸', 15],
        ['坦克', 100000],
        ['macbook', 20000],
    ]

    shopping_car = {} # {'商品名称': ['单价', '数量']]}

    while True:
        print('============欢迎来到有趣用品商城============')
        for index, shop in enumerate(shop_list):
            shop_name, shop_price = shop
            print(f'商品编号为:[{index}]',
                  f'商品名称:[{shop_name}]',
                  f'商品单价:[{shop_price}]')
        print('================24小时服务哦==============')

        choice = input('请输入商品编号（是否结账输入 y or n）：').strip()

        if choice == 'y':
            if not shopping_car:
                print('购物车是空的，不能支付，请重新输入！')
                continue
            else:
                flag, msg = shop_interface.shopping_interface(login_user, shopping_car)
                if flag:
                    print(msg)
                    break
                else:
                    print(msg)

        elif choice == 'n': # 先添加购物车
            if not shopping_car:
                print('购物车是空的，不能添加，请重新输入！')
                continue
            flag, msg = shop_interface.add_shop_car_interface(login_user, shopping_car)
            if flag:
                print(msg)
                break

        if not choice.isdigit():
            continue

        choice = int(choice)

        if choice not in range(len(shop_list)):
            print('请输入正确的编号！')
            continue

        shop_name, shop_price = shop_list[choice]
        if shop_name in shopping_car:
            shopping_car[shop_name][1] += 1
        else:
            shopping_car[shop_name] = [shop_price, 1]

        print('当前购物车：', shopping_car)


# 9、查看购物车
@common.login_auth
def check_shop_car():
    shop_car = shop_interface.check_shop_car_interface(login_user)
    print(shop_car)

# 10、管理员功能
@common.login_auth
def admin():
    from core import admin

    admin.admin_run()

# 创建函数功能字典
func_dic = {
    '1': register,
    '2': login,
    '3': check_balance,
    '4': withdraw,
    '5': repay,
    '6': transfer,
    '7': check_flow,
    '8': shopping,
    '9': check_shop_car,
    '10': admin,
}

# 视图层主程序
def run():
    while True:
        print('''
        ==== ATM + 购物车 ====
            1、注册功能
            2、登录功能
            3、查看余额
            4、提现功能
            5、还款功能
            6、转账功能
            7、查看流水
            8、购物功能
            9、查看购物车
            10、管理员功能
        ==== end ====
        ''')

        choice = input('请输入功能编号：').strip()

        if choice not in func_dic:
            print("请输入正确的功能编号！")
            continue

        # 根据编号调用功能
        func_dic.get(choice)()
