# -*- coding: utf-8 -*-

from api import *

ak_config = arknights_config()
ak_push = arknights_push()

check_version_res = ak_config.check_version()
if not check_version_res is None:
    ak_push.push(check_version_res)
    exit(1)

push_when_changed_enabled = ak_config.load_config_push_when_changed()

accounts_config = ak_config.load_config_accounts()

for account_config in accounts_config:
    token = account_config.get('token')
    ak_api = arknights_api(token)
    db_timestamp = int(ak_api.update_cards_db())

    if push_when_changed_enabled == 1:
        if 'push_timestamp' not in account_config:
            account_config['push_timestamp'] = -1
        if db_timestamp > account_config['push_timestamp']:
            push_body = ak_push.parse_body(ak_api)
            print(push_body)
            ak_push.push(push_body)
            account_config['push_timestamp'] = db_timestamp
    else:
        push_body = ak_push.parse_body(ak_api)
        print(push_body)
        ak_push.push(push_body)
ak_config.update_config_accounts(accounts_config)
