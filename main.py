# -*- coding: utf-8 -*-

from api import *

a_config = ada_config()

push_when_changed_enabled = a_config.load_config_push_when_changed()
force_refresh_enabled = a_config.load_config_force_refresh()


tokens = []
for dbuser in DBUser.select():
    for acc in dbuser.ark_accs:
        tokens.append(acc.token)


# accounts_config = a_config.load_config_accounts()

# for account_config in accounts_config:
for token in tokens:
    # token = account_config.get('token')
    a_api = ada_api(token, force_refresh=force_refresh_enabled)

    # if push_when_changed_enabled == 1:
    #     if 'push_time' not in account_config:
    #         account_config['push_time'] = -1
    #     account_config['push_time'] = a_api.push(account_config['push_time'])
    #     a_config.update_config()
    # else:
    #     a_api.push()

