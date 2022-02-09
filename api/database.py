# -*- coding: utf-8 -*-
import sqlite3
from .config import *

class arknights_database():
    def __init__(self, config_file=None):
        if config_file is None:
            ak_config = arknights_config()
        else:
            ak_config = arknights_config(config_file)
        self.database_type, self.database_type_config = ak_config.load_config_database()

        if self.database_type == 'sqlite3':
            self.db_name = self.database_type_config.get('filename')

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

