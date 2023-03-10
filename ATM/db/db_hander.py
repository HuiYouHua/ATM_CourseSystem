# ========================
# Author: huayoyu
# Date: 2023/2/11
# 文件名： db_hander
# ========================
'''
数据处理层
    - 专门用户处理数据的
'''
import json
import os
from conf import setting

# 查看数据
def select(username):
    # 1.接收接口层传过来的username， 拼接用户json文件路径
    user_path = os.path.join(
        setting.USER_PATH_PATH, f'{username}.json'
    )

    # 2.校验用户json文件是否存在
    if os.path.exists(user_path):
        # 3.打开文件，并返回给接口层
        with open(user_path, 'r', encoding='utf-8') as f:
            user_dic = json.load(f)
            return user_dic

    # 4.不return 默认return None

# 保存数据（添加或更新）
def save(user_dic):
    # 1.拼接用户的数据字典
    username = user_dic.get('username')

    user_path = os.path.join(
        setting.USER_PATH_PATH, f'{username}.json'
    )

    # 2.保存用户数据
    with open(user_path, 'w', encoding='utf-8') as f:
        json.dump(user_dic, f, ensure_ascii=False)
