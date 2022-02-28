# -*- coding: utf-8 -*-
import os, json

class ada_config():
    version = 'v2.0.1'
    config = {
        "version": "{}".format(version),
        "database": {
            "type": "sqlite3",
            "sqlite3": {
                "filename": "ak_server.db"
            },
            "mysql": {
                "host": "",
                "user": "",
                "password": "",
                "database": ""
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
            "serverchan": {
                "send_key": "",
                "title": "Arnights 寻访记录"
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
            self.check_version()
            self.load_config()

    def update_config_version(self, local_config):
        if local_config.get('version') == 'v2.0.0':
            local_config['version'] = 'v2.0.1'
        self.config = local_config
        self.update_config()

    def check_version(self):
        with open(self.config_file, encoding='utf-8') as json_file:
            local_config = json.load(json_file)
        if not local_config.get('version') == self.version:
            self.update_config_version(local_config)
    
    def load_config(self):
        with open(self.config_file, encoding='utf-8') as json_file:
            self.config = json.load(json_file)
        return self.config

    def update_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as json_file:
            json.dump(self.config, json_file, indent=4, ensure_ascii=False)

    def load_config_accounts(self):
        self.load_config()
        accounts_config = self.config.get('accounts')
        return accounts_config

    def load_config_database(self):
        self.load_config()
        database_config = self.config.get('database')
        database_type = database_config.get('type')
        database_type_list = ['sqlite3', 'mysql']
        if not database_type in database_type_list:
            exit("ERROR: DATABASE_TYPE must be in {}".format(database_type_list))
        type_config = database_config.get(database_type)
        return database_type, type_config
    
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