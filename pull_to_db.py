# -*- coding: utf-8 -*-

# 服务器定时运行，仅拉取保存到数据库

from arknights_cards import *

ak_config = arknights_config()

database_type, type_config = ak_config.load_config_database()
if database_type == 'sqlite3':
    sqlite_filename = type_config.get('filename')

accounts_config = ak_config.load_config_accounts()

for account_config in accounts_config:
    token = account_config.get('token')

    ak_cards = arknights_cards(token, sqlite_filename)
    ak_cards.update_cards_db() # 将获取到的寻访记录增量更新到数据库中更新