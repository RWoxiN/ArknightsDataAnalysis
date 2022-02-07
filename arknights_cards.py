# -*- coding: utf-8 -*-

import requests
import json
import sqlite3
import os
import copy

class arknights_config():

    config = {
        "version": "v1.0",
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
        "bark": {
            "url": "",
            "device_key": "",
            "title": "Arnights 寻访记录",
            "group": "Arknights",
            "badge": 1,
            "isArchive": 1,
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
    
    def load_config(self):
        with open(self.config_file, encoding='utf-8') as json_file:
            self.config = json.load(json_file)
        return self.config

    def update_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as json_file:
            json.dump(self.config, json_file, indent=4, ensure_ascii=False)

    def load_config_database(self):
        database_config = self.config.get('database')
        database_type = database_config.get('type')
        type_config = database_config.get(database_type)
        return database_type, type_config

    def load_config_accounts(self):
        self.load_config()
        accounts_config = self.config.get('accounts')
        bark_config = self.config.get('bark')
        final_accounts_config = []
        for account in accounts_config:    
            account_bark_config = account.get('bark')
            if account_bark_config == None:
                account_bark_config = bark_config
            else:
                temp_bark_config = copy.copy(bark_config)
                temp_bark_config.update((key, value) for key, value in account_bark_config.items())
                account_bark_config = temp_bark_config
            account['bark'] = account_bark_config
            final_accounts_config.append(account)
        return final_accounts_config


class arknights_api():
    class request_api():
        def get(url):
            r = requests.get(url)
            if r.status_code == 200:
                return r.content
            return 'ERROR'

        def post(url, data):
            r = requests.post(url, data=data)
            if r.status_code == 200:
                return r.content
            return 'ERROR'

    url_user_info = 'https://as.hypergryph.com/u8/user/info/v1/basic'
    url_cards_record = 'http://ak.hypergryph.com/user/api/inquiry/gacha'

    def __init__(self, token):
        self.token = token

    def get_user_info(self):
        payload = '''
        {{
            "appId":1,
            "channelMasterId":1,
            "channelToken":{{
                "token":"{}"
            }}
        }}    
        '''.format(self.token)
        source_from_server = self.request_api.post(self.url_user_info, payload)
        if source_from_server == 'ERROR':
            print('ERROR: arknights_api::get_user_info, token: {}'.format(self.token))
            exit(1)
        user_info_source = json.loads(source_from_server).get('data')
        user_info_dict = {
            'uid': user_info_source.get('uid'),
            'nickName': user_info_source.get('nickName')
        }
        return user_info_dict

    def get_cards_record(self, last_timestamp=None):
        def get_cards_record_by_page(page):
            url_cards_record_page = '{}?page={}&token={}'.format(self.url_cards_record, page, self.token)
            source_from_server = self.request_api.get(url_cards_record_page)
            if source_from_server == 'ERROR':
                print('ERROR: arknights_api::get_cards_record::get_cards_record_by_page, page: {}, token: {}'.format(page, self.token))
                exit(1)
            cards_record_page_source = json.loads(source_from_server)
            cards_record_page_data_list = cards_record_page_source.get('data').get('list')
            return cards_record_page_data_list

        cards_record_data_list = []
        flag_outdate = False
        for page in range(1, 75):
            if flag_outdate == True:
                break
            cards_record_page_data_list = get_cards_record_by_page(page)
            if cards_record_page_data_list == []:
                break
            if last_timestamp == None:
                cards_record_data_list.extend(cards_record_page_data_list)
            else:
                for cards_record_page_data_item in cards_record_page_data_list:
                    if int(cards_record_page_data_item['ts']) > int(last_timestamp):
                        cards_record_data_list.append(cards_record_page_data_item)
                    else:
                        flag_outdate = True
                        break

        cards_record_data_list = reversed(cards_record_data_list)
        return cards_record_data_list

class arknights_database():
    def __init__(self, db_name):
        self.db_name = db_name
        conn = sqlite3.connect(self.db_name)
        try:
            create_tb_cmd = 'CREATE TABLE IF NOT EXISTS CHARS (ID INTEGER PRIMARY KEY AUTOINCREMENT, UID TEXT, TS TIMESTAMP, POOL TEXT, NAME TEXT, RARITY INTEGER, ISNEW INTEGER, COUNT INTEGER)'
            conn.execute(create_tb_cmd)
            conn.commit()
        except:
            pass
        conn.close()

    def insert_cards(self, uid, cards_record_data_list):
        conn = sqlite3.connect(self.db_name)
        try:
            for cards_record_data_item in cards_record_data_list:
                ts = cards_record_data_item['ts']
                pool = cards_record_data_item['pool']
                chars_list = cards_record_data_item['chars']
                for chars_item in chars_list:
                    chars_name = chars_item['name']
                    chars_rarity = chars_item['rarity'] + 1
                    chars_isnew = int(chars_item['isNew'])
                    insert_dt_cmd = 'INSERT INTO CHARS (UID, TS, POOL, NAME, RARITY, ISNEW, COUNT) VALUES (\'{}\', \'{}\', \'{}\', \'{}\', {}, {}, -1)'.format(uid, ts, pool, chars_name, chars_rarity, chars_isnew)
                    conn.execute(insert_dt_cmd)
            conn.commit()
        except:
            print('ERROR: arknights_database::insert_cards, uid: {}'.format(uid))
        conn.close()

    def get_pools(self, uid):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        select_dt_cmd = 'SELECT DISTINCT POOL FROM CHARS WHERE UID = \'{}\''.format(uid)
        # print(select_dt_cmd)
        cursor = cur.execute(select_dt_cmd)
        pools = []
        for row in cursor:
            pools.append(row[0])
        conn.close()
        return pools

    def get_last_timestamp(self, uid):
        last_timestamp_dict = {}
        pools = self.get_pools(uid)
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        select_dt_cmd = 'SELECT MAX(TS) TS FROM CHARS WHERE UID = \'{}\''.format(uid)
        cursor = cur.execute(select_dt_cmd)
        for row in cursor:
            last_timestamp_dict['global'] = row[0]
        for pool in pools:
            select_dt_cmd = 'SELECT MAX(TS) TS FROM CHARS WHERE UID = \'{}\' AND POOL = \'{}\''.format(uid, pool)
            cursor = cur.execute(select_dt_cmd)
            for row in cursor:
                last_timestamp_dict[pool] = row[0]
        conn.close()
        return last_timestamp_dict

    def update_count(self, uid, last_timestamp_dict):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()

        pools = self.get_pools(uid)

        for pool in pools:
            if not pool in last_timestamp_dict:
                last_timestamp_dict[pool] = None
            last_ts = last_timestamp_dict[pool]
            if last_ts == None:
                select_dt_cmd = 'SELECT ID, RARITY, COUNT FROM CHARS WHERE UID = \'{}\' AND POOL = \'{}\' ORDER BY TS ASC'.format(uid, pool)
            else:
                select_dt_cmd = 'SELECT ID, RARITY, COUNT FROM CHARS WHERE UID = \'{}\' AND TS >= \'{}\' AND POOL = \'{}\' ORDER BY TS ASC'.format(uid, last_ts, pool)
            # print(select_dt_cmd)
            cursor = cur.execute(select_dt_cmd)
            count = 1
            flag = 0
            for row in cursor:
                if flag == 0:
                    flag = 1
                    if row[2] == -1:
                        update_dt_cmd = 'UPDATE CHARS SET COUNT = {} WHERE ID = {}'.format(count, row[0])
                        conn.execute(update_dt_cmd)
                        count += 1
                    else:
                        if row[1] == 6:
                            count = 1
                        else:
                            count = int(row[2])
                            count += 1
                else:
                    update_dt_cmd = 'UPDATE CHARS SET COUNT = {} WHERE ID = {}'.format(count, row[0])
                    conn.execute(update_dt_cmd)
                    count += 1
                    if int(row[1]) == 6:
                        count = 1
        conn.commit()
        conn.close()
    
    def get_cards_record_number(self, uid, pool=None, rarity=None):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        select_dt_cmd = ''
        if rarity is None:
            if pool is None:
                select_dt_cmd = 'SELECT COUNT(UID) FROM CHARS WHERE UID = \'{}\''.format(uid)
            else:
                select_dt_cmd = 'SELECT COUNT(UID) FROM CHARS WHERE UID = \'{}\' AND POOL = \'{}\''.format(uid, pool)
        else:
            if pool is None:
                select_dt_cmd = 'SELECT COUNT(UID) FROM CHARS WHERE UID = \'{}\' AND RARITY = {}'.format(uid, rarity)
            else:
                select_dt_cmd = 'SELECT COUNT(UID) FROM CHARS WHERE UID = \'{}\' AND POOL = \'{}\' AND RARITY = {}'.format(uid, pool, rarity)
        # print(select_dt_cmd)
        cursor = cur.execute(select_dt_cmd)
        for row in cursor:
            num = int(row[0])
        conn.close()
        return num

    def get_cards_guarantee_count(self, uid, pool):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        select_dt_cmd = 'SELECT COUNT, RARITY, TS FROM CHARS WHERE UID = \'{}\' AND POOL = \'{}\' ORDER BY ID DESC LIMIT 1'.format(uid, pool)
        # print(select_dt_cmd)
        cursor = cur.execute(select_dt_cmd)
        for row in cursor:
            num = int(row[0])
            rar = int(row[1])
            if rar == 6:
                num = 0
        conn.close()
        return num

    def get_cards_history(self, uid, rarity):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        select_dt_cmd = 'SELECT TS, POOL, NAME, ISNEW, COUNT FROM CHARS WHERE UID = \'{}\' AND RARITY = {} ORDER BY TS DESC, ID DESC'.format(uid, rarity)
        # print(select_dt_cmd)
        cursor = cur.execute(select_dt_cmd)
        history = []
        for row in cursor:
            history.append(row)
        conn.close()
        return history

    def get_cards_rarity_six_count_avg(self, uid, pool=None):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        select_dt_cmd = ''
        if pool == None:
            select_dt_cmd = 'SELECT AVG(COUNT) FROM CHARS WHERE UID = \'{}\' AND RARITY = {}'.format(uid, 6)
        else:
            select_dt_cmd = 'SELECT AVG(COUNT) FROM CHARS WHERE UID = \'{}\' AND RARITY = {} AND POOL = \'{}\''.format(uid, 6, pool)
        # print(select_dt_cmd)
        cursor = cur.execute(select_dt_cmd)
        for row in cursor:
            num = row[0]
        conn.close()
        if not num == None:
            num = format(num, '.1f')
        return num


class arknights_cards():

    ################################
    # 初始化
    # params:
    #   token: token
    #   db_name: sqlite 数据库名称
    ################################
    def __init__(self, token, db_name):
        self.ak_api = arknights_api(token)
        self.ak_db = arknights_database(db_name)

        user_info_dict = self.ak_api.get_user_info()

        self.uid = user_info_dict['uid']
        self.nickName = user_info_dict['nickName']

    ################################
    # 显示当前用户数据
    # return:
    #   {
    #       "uid": "用户UID",
    #       "nickName": "昵称"
    #   }
    ################################
    def show(self):
        user_info_dict = self.ak_api.get_user_info()
        # print('uid: {}, nickName: {}'.format(user_info_dict['uid'], user_info_dict['nickName']))
        return user_info_dict

    ################################
    # 将获取到的寻访记录增量更新到数据库中
    # return:
    #   None
    ################################
    def update_cards_db(self):
        last_timestamp_dict = self.ak_db.get_last_timestamp(self.uid)
        cards_record_data_list = self.ak_api.get_cards_record(last_timestamp_dict['global'])
        self.ak_db.insert_cards(self.uid, cards_record_data_list)
        self.ak_db.update_count(self.uid, last_timestamp_dict)

    ################################
    # 获取抽卡详细数据，即总计抽数，以及每个星级的抽数
    # return:
    #   {
    #       "all": 总抽数,
    #       "3": 抽到的三星总数,
    #       "4": 抽到的四星总数,
    #       "5": 抽到的五星总数,
    #       "6": 抽到的六星总数
    #   }
    ################################
    def get_cards_number(self):
        numbers = {
            'all': self.ak_db.get_cards_record_number(self.uid),
            '3': self.ak_db.get_cards_record_number(self.uid, None, 3),
            '4': self.ak_db.get_cards_record_number(self.uid, None, 4),
            '5': self.ak_db.get_cards_record_number(self.uid, None, 5),
            '6': self.ak_db.get_cards_record_number(self.uid, None, 6),
        }
        # print('抽卡详细数据: {}'.format(numbers))
        return numbers

    ################################
    # 获取各卡池抽卡次数，以及各卡池中每个星级的抽数
    # return:
    #   {
    #       "池子": {
    #           "all": 该池子总抽数,
    #           "3": 该池子抽到的三星总数,
    #           "4": 该池子抽到的四星总数,
    #           "5": 该池子抽到的五星总数,
    #           "6": 该池子抽到的六星总数
    #       },
    #       ...
    #   }
    ################################
    def get_cards_number_pool(self):
        pools = self.ak_db.get_pools(self.uid)
        numbers = {}
        for pool in pools:
            pool_numbers = {
                'all': self.ak_db.get_cards_record_number(self.uid, pool),
                '3': self.ak_db.get_cards_record_number(self.uid, pool, 3),
                '4': self.ak_db.get_cards_record_number(self.uid, pool, 4),
                '5': self.ak_db.get_cards_record_number(self.uid, pool, 5),
                '6': self.ak_db.get_cards_record_number(self.uid, pool, 6),
            }
            numbers[pool] = pool_numbers
        # print('各卡池抽卡数据: {}'.format(numbers))
        return numbers

    ################################
    # 获取各卡池保底状况，即已累计多少抽未出六星，以及下一抽概率
    # return:
    #   {
    #       "池子": {
    #           "count": 该池子当前保底抽数,
    #           "probability_next": 该池子下一抽出货概率
    #       },
    #       ...
    #   }
    ################################
    def get_cards_pool_guarantee_count(self):
        pools = self.ak_db.get_pools(self.uid)
        numbers = {}
        for pool in pools:
            count = self.ak_db.get_cards_guarantee_count(self.uid, pool)
            probability = 2
            if count >= 50:
                probability += (count + 1 - 50) * 2
            pool_number = {
                'count': count,
                'probability_next': probability
            }
            numbers[pool] = pool_number
        # print('各卡池保底数据: {}'.format(numbers))
        return numbers

    ################################
    # 获取抽到的六星历史记录
    # return:
    #   [
    #       {
    #           "TIME": 该六星出货的时间戳,
    #           "POOL": 该六星出货的池子,
    #           "NAME": 该六星名称,
    #           "ISNEW": 该六星是否首次获得,
    #           "COUNT": 该六星出货时的抽数
    #       },
    #       ...
    #   ]
    ################################
    def get_cards_six_history(self):
        histories = self.ak_db.get_cards_history(self.uid, 6)
        res = []
        for history in histories:
            item = {
                'TIME': history[0],
                'POOL': history[1],
                'NAME': history[2],
                'ISNEW': bool(history[3]),
                'COUNT': history[4]
            }
            res.append(item)
        # print('六星历史记录: {}'.format(res))
        return res

    ################################
    # 获取各卡池平均出货抽数
    # return:
    #   {
    #       "global": 全局平均出货抽数,
    #       "池子": 该池子平均出货抽数
    #       ...
    #   }
    ################################
    def get_cards_count_avg(self):
        pools = self.ak_db.get_pools(self.uid)
        numbers = {}
        numbers['global'] = self.ak_db.get_cards_rarity_six_count_avg(self.uid)
        for pool in pools:
            numbers[pool] = self.ak_db.get_cards_rarity_six_count_avg(self.uid, pool)
        # print('各卡池平均出货数据: {}'.format(numbers))
        return numbers
