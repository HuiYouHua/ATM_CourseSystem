# ========================
# Author: huayoyu
# Date: 2023/2/12
# 文件名：admin
# ========================
from core import src
from interface import admin_interface

# 添加用户
def add_user():
    src.register()

# 修改用户额度
def change_balance():
    while True:
        change_user = input('请输入需要修改额度的用户：').strip()
        money = input('请输入需要修改的额度').strip()

        if not money.isdigit():
            continue

        flag, msg = admin_interface.change_balance_interface(change_user, money)
        if flag:
            print(msg)
            break
        else:
            print(msg)


# 冻结账户
def lock_user():
    while True:
        username = input('请输入需要冻结的用户名').strip()

        flag, msg = admin_interface.lock_user_interface(username)
        if flag:
            print(msg)
            break
        else:
            print(msg)

def admin_run():

    # 管理员功能字典
    admin_func = {
        '1': add_user,
        '2': change_balance,
        '3': lock_user
    }

    while True:
        print('''
                    1、添加用户
                    2、修改用户额度
                    3、冻结账户
                    ''')

        choice = input('请输入管理员功能编号：').strip()

        if choice not in admin_func:
            print("请输入正确的理员功能编号！")
            continue

        # 根据编号调用功能
        admin_func.get(choice)()