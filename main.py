# -*- coding: utf-8 -*-

from api import *

a_config = ada_config()

push_when_changed_enabled = a_config.load_config_push_when_changed()

accounts_config = a_config.load_config_accounts()

for account_config in accounts_config:
    token = account_config.get('token')
    a_api = ada_api(token)

    if push_when_changed_enabled == 1:
        if 'push_time' not in account_config:
            account_config['push_time'] = -1
        account_config['push_time'] = a_api.push(account_config['push_time'])
        a_config.update_config()
    else:
        a_api.push()

