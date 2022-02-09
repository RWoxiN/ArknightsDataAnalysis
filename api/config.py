# -*- coding: utf-8 -*-
import os, json

class arknights_config():
    version = "v1.0.1"
    config = {
        "version": "{}".format(version),
        "database": {
            "type": "sqlite3",
            "sqlite3": {
                "filename": "ak_server.db"
            } 
        },
        "accounts": [
            {
                "name": "",
                "token": ""
            }
        ],
        "push": {
            "enabled": 1,
            "type": "bark",
            "push_when_changed": {
                "enabled": 1
            },
            "bark": {
                "url": "",
                "device_key": "",
                "title": "Arnights 寻访记录",
                "group": "Arknights",
                "badge": 1,
                "isArchive": 1 
            },
            "body": {
                "user_info": {
                    "enabled": 1,
                    "format_main": "当前用户：",
                    "format": "UID: {0}, NickName: {1}.",
                    "description": "显示当前用户数据。",
                    "params_description": "{0}: 用户UID. {1}: 昵称."
                },
                "cards_record": {
                    "enabled": 1,
                    "format_main": "抽卡详细数据：",
                    "format": "共抽卡 {0} 次，其中六星 {1} 次，五星 {2} 次。",
                    "description": "显示抽卡详细数据，即总计抽数，以及每个星级的抽数。",
                    "params_description": "{0}: 总抽数. {1}: 抽到的六星总数. {2}: 抽到的五星总数. {3}: 抽到的四星总数. {4}: 抽到的三星总数."
                },
                "cards_record_pool": {
                    "enabled": 1,
                    "format_main": "各卡池抽卡数据：",
                    "format": "{0}: 总抽数: {1}，其中六星 {2} 次，五星 {3} 次。",
                    "description": "获取各卡池抽卡次数，以及各卡池中每个星级的抽数",
                    "params_description": "{0}: 池子. {1}: 该池子总抽数. {2}: 该池子抽到的六星总数. {3}: 该池子抽到的五星总数. {4}: 该池子抽到的四星总数. {5}: 该池子抽到的三星总数."

                },
                "cards_pool_guarantee": {
                    "enabled": 1,
                    "format_main": "保底情况：",
                    "format": "{0}: 抽数: {1}, 下一抽概率: {2}%",
                    "description": "获取各卡池保底状况，即已累计多少抽未出六星",
                    "params_description": "{0}: 池子. {1}: 该池子当前保底抽数. {2}: 该池子下一抽出货概率."
                },
                "cards_count_avg": {
                    "enabled": 1,
                    "format_main": "平均出货抽数：",
                    "format": "{0}: 抽数: {1}",
                    "description": "获取各卡池平均出货抽数",
                    "params_description": "{0}: 池子. {1}: 该池子平均出货抽数."
                },
                "cards_record_six": {
                    "enabled": 1,
                    "format_main": "历史抽取六星：",
                    "format": "{0}: {1}: {2}, 抽数: {3}",
                    "format_datatime": "%Y-%m-%d %H:%M",
                    "description": "获取抽到的六星历史记录",
                    "params_description": "{0}: 该六星出货的时间. {1}: 该六星出货的池子. {2}: 该六星名称. {3}: 该六星出货时的抽数."
                }
            }
        }
    }

    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        if not os.path.exists(self.config_file):
            self.update_config()
            print('初始化 {} 完成，请前往完成相关配置！'.format(self.config_file))
            exit(1)
        else:
            self.load_config()

    def check_version(self):
        self.load_config()
        if not self.config.get('version') == self.version:
            warning_str = 'WARNING: \n配置文件版本较旧，程序运行可能出现问题，请尽快更新！\n\n当前版本：{}，最新版本：{}'.format(self.config.get('version'), self.version)
            return warning_str
        return None

    def load_config(self):
        with open(self.config_file, encoding='utf-8') as json_file:
            self.config = json.load(json_file)
        return self.config

    def update_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as json_file:
            json.dump(self.config, json_file, indent=4, ensure_ascii=False)

    def load_config_database(self):
        self.load_config()
        database_config = self.config.get('database')
        database_type = database_config.get('type')
        type_config = database_config.get(database_type)
        return database_type, type_config

    def load_config_accounts(self):
        self.load_config()
        accounts_config = self.config.get('accounts')
        return accounts_config

    def update_config_accounts(self, accounts_config):
        self.load_config()
        self.config['accounts'] = accounts_config
        self.update_config()

    def load_config_push(self):
        self.load_config()
        push_config = self.config.get('push')
        push_enabled = push_config.get('enabled')
        if push_enabled == 0:
            return None, None
        push_type = push_config.get('type')
        type_config = push_config.get(push_type)
        return push_type, type_config

    def load_config_push_when_changed(self):
        self.load_config()
        push_config = self.config.get('push')
        push_when_changed_config = push_config.get('push_when_changed')
        push_when_changed_enabled = push_when_changed_config.get('enabled')
        return push_when_changed_enabled
 
    def load_config_push_body(self):
        self.load_config()
        push_config = self.config.get('push')
        push_body = push_config.get('body')
        return push_body