# -*- coding: utf-8 -*-

from arknights_cards import *
import time

ak_config = arknights_config()

database_type, type_config = ak_config.load_config_database()
if database_type == 'sqlite3':
    sqlite_filename = type_config.get('filename')

accounts_config = ak_config.load_config_accounts()

for account_config in accounts_config:
    token = account_config.get('token')
    bark_config = account_config.get('bark')

    bark_body_config = bark_config.get('body')

    ak_cards = arknights_cards(token, sqlite_filename) 

    out_str = ''

    if bark_body_config.get('user_info').get('enabled') == 1:
        user_info_dict = ak_cards.show() # 显示当前用户数据
        uid = user_info_dict['uid']
        nickName = user_info_dict['nickName']
        user_info_str = bark_body_config.get('user_info').get('format').format(uid, nickName)
        if not out_str == '':
            out_str += '\n\n'
        s_title = bark_body_config.get('user_info').get('format_main')
        if not s_title == '':
            out_str += s_title
            out_str += '\n'
        out_str += user_info_str

    ak_cards.update_cards_db() # 将获取到的寻访记录增量更新到数据库中

    if bark_body_config.get('cards_record').get('enabled') == 1:
        cards_numbers = ak_cards.get_cards_number() # 获取抽卡详细数据，即总计抽数，以及每个星级的抽数
        cards_numbers_str = bark_body_config.get('cards_record').get('format').format(cards_numbers['all'], cards_numbers['6'], cards_numbers['5'], cards_numbers['4'], cards_numbers['3'])
        if not out_str == '':
            out_str += '\n\n'
        s_title = bark_body_config.get('cards_record').get('format_main')
        if not s_title == '':
            out_str += s_title
            out_str += '\n'
        out_str += cards_numbers_str

    if bark_body_config.get('cards_record_pool').get('enabled') == 1:
        pool_records = ak_cards.get_cards_number_pool()
        pool_records_str = ''
        for pool in pool_records:
            if not pool_records_str == '':
                pool_records_str += '\n'
            pool_records_str += bark_body_config.get('cards_record_pool').get('format').format(pool, pool_records[pool]['all'], pool_records[pool]['6'], pool_records[pool]['5'], pool_records[pool]['4'], pool_records[pool]['3'])

        if not out_str == '':
            out_str += '\n\n'
        s_title = bark_body_config.get('cards_record_pool').get('format_main')
        if not s_title == '':
            out_str += s_title
            out_str += '\n'
        out_str += pool_records_str

    if bark_body_config.get('cards_pool_guarantee').get('enabled') == 1:
        pool_records_guarantee = ak_cards.get_cards_pool_guarantee_count()
        pool_records_guarantee_str = ''
        for pool in pool_records_guarantee:
            if not pool_records_guarantee_str == '':
                pool_records_guarantee_str += '\n'
            pool_records_guarantee_str += bark_body_config.get('cards_pool_guarantee').get('format').format(pool, pool_records_guarantee[pool]['count'], pool_records_guarantee[pool]['probability_next'])

        if not out_str == '':
            out_str += '\n\n'
        s_title = bark_body_config.get('cards_pool_guarantee').get('format_main')
        if not s_title == '':
            out_str += s_title
            out_str += '\n'
        out_str += pool_records_guarantee_str

    if bark_body_config.get('cards_count_avg').get('enabled') == 1:
        count_avg = ak_cards.get_cards_count_avg()
        count_avg_str = ''
        for pool in count_avg:
            if not count_avg_str == '':
                count_avg_str += '\n'
            pool_name = pool
            if pool == 'global':
                pool_name = '全局'
            count_avg_str += bark_body_config.get('cards_count_avg').get('format').format(pool_name, count_avg[pool])

        if not out_str == '':
            out_str += '\n\n'
        s_title = bark_body_config.get('cards_count_avg').get('format_main')
        if not s_title == '':
            out_str += s_title
            out_str += '\n'
        out_str += count_avg_str

    if bark_body_config.get('cards_record_six').get('enabled') == 1:
        record_six = ak_cards.get_cards_six_history()
        record_six_str = ''
        for record_six_item in record_six:
            if not record_six_str == '':
                record_six_str += '\n'
            time_local = time.localtime(record_six_item['TIME'])
            datatime = time.strftime(bark_body_config.get('cards_record_six').get('format_datatime'), time_local)
            name = record_six_item['NAME']
            if record_six_item['ISNEW'] == True:
                name += '(NEW)'
            record_six_str += bark_body_config.get('cards_record_six').get('format').format(datatime, record_six_item['POOL'], name, record_six_item['COUNT'])

        if not out_str == '':
            out_str += '\n\n'
        s_title = bark_body_config.get('cards_record_six').get('format_main')
        if not s_title == '':
            out_str += s_title
            out_str += '\n'
        out_str += record_six_str

    print(out_str)

    bark_url = bark_config.get('url')
    data = {
        'title': bark_config.get('title'),
        'body': out_str,
        'device_key': bark_config.get('device_key'), 
        'badge': bark_config.get('badge'),
        'group': bark_config.get('group'),
        'isArchive': bark_config.get('isArchive')
    }
    arknights_api.request_api.post(bark_url, data)