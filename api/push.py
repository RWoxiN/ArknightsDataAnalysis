# -*- coding: utf-8 -*-

import time, requests
from .config import *

class arknights_push():

    def __init__(self, config_file=None):
        if config_file is None:
            ak_config = arknights_config()
        else:
            ak_config = arknights_config(config_file)
        self.push_type, self.push_type_config = ak_config.load_config_push()
        self.push_body_config = ak_config.load_config_push_body()

    def parse_body(self, ak_api):
        out_str = ''

        if self.push_body_config.get('user_info').get('enabled') == 1:
            user_info_dict = ak_api.get_user_info() # 显示当前用户数据
            uid = user_info_dict['uid']
            nickName = user_info_dict['nickName']
            user_info_str = self.push_body_config.get('user_info').get('format').format(uid, nickName)
            if not out_str == '':
                out_str += '\n\n'
                if self.push_type == 'serverchan':
                    out_str += '\n'
            s_title = self.push_body_config.get('user_info').get('format_main')
            if not s_title == '':
                out_str += s_title
                out_str += '\n'
                if self.push_type == 'serverchan':
                    out_str += '\n'
            out_str += user_info_str

        if self.push_body_config.get('cards_record').get('enabled') == 1:
            cards_numbers = ak_api.get_cards_number() # 获取抽卡详细数据，即总计抽数，以及每个星级的抽数
            cards_numbers_str = self.push_body_config.get('cards_record').get('format').format(cards_numbers['all'], cards_numbers['6'], cards_numbers['5'], cards_numbers['4'], cards_numbers['3'])
            if not out_str == '':
                out_str += '\n\n'
                if self.push_type == 'serverchan':
                    out_str += '\n'
            s_title = self.push_body_config.get('cards_record').get('format_main')
            if not s_title == '':
                out_str += s_title
                out_str += '\n'
                if self.push_type == 'serverchan':
                    out_str += '\n'
            out_str += cards_numbers_str

        if self.push_body_config.get('cards_record_pool').get('enabled') == 1:
            pool_records = ak_api.get_cards_number_pool()
            pool_records_str = ''
            for pool in pool_records:
                if not pool_records_str == '':
                    pool_records_str += '\n'
                    if self.push_type == 'serverchan':
                        pool_records_str += '\n'
                pool_records_str += self.push_body_config.get('cards_record_pool').get('format').format(pool, pool_records[pool]['all'], pool_records[pool]['6'], pool_records[pool]['5'], pool_records[pool]['4'], pool_records[pool]['3'])

            if not out_str == '':
                out_str += '\n\n'
                if self.push_type == 'serverchan':
                    out_str += '\n'
            s_title = self.push_body_config.get('cards_record_pool').get('format_main')
            if not s_title == '':
                out_str += s_title
                out_str += '\n'
                if self.push_type == 'serverchan':
                    out_str += '\n'
            out_str += pool_records_str

        if self.push_body_config.get('cards_pool_guarantee').get('enabled') == 1:
            pool_records_guarantee = ak_api.get_cards_pool_guarantee_count()
            pool_records_guarantee_str = ''
            for pool in pool_records_guarantee:
                if not pool_records_guarantee_str == '':
                    pool_records_guarantee_str += '\n'
                    if self.push_type == 'serverchan':
                        pool_records_guarantee_str += '\n'
                pool_records_guarantee_str += self.push_body_config.get('cards_pool_guarantee').get('format').format(pool, pool_records_guarantee[pool]['count'], pool_records_guarantee[pool]['probability_next'])

            if not out_str == '':
                out_str += '\n\n'
                if self.push_type == 'serverchan':
                    out_str += '\n'
            s_title = self.push_body_config.get('cards_pool_guarantee').get('format_main')
            if not s_title == '':
                out_str += s_title
                out_str += '\n'
                if self.push_type == 'serverchan':
                    out_str += '\n'
            out_str += pool_records_guarantee_str

        if self.push_body_config.get('cards_count_avg').get('enabled') == 1:
            count_avg = ak_api.get_cards_count_avg()
            count_avg_str = ''
            for pool in count_avg:
                if not count_avg_str == '':
                    count_avg_str += '\n'
                    if self.push_type == 'serverchan':
                        count_avg_str += '\n'
                pool_name = pool
                if pool == 'global':
                    pool_name = '全局'
                count_avg_str += self.push_body_config.get('cards_count_avg').get('format').format(pool_name, count_avg[pool])

            if not out_str == '':
                out_str += '\n\n'
                if self.push_type == 'serverchan':
                    out_str += '\n'
            s_title = self.push_body_config.get('cards_count_avg').get('format_main')
            if not s_title == '':
                out_str += s_title
                out_str += '\n'
                if self.push_type == 'serverchan':
                    out_str += '\n'
            out_str += count_avg_str

        if self.push_body_config.get('cards_record_six').get('enabled') == 1:
            record_six = ak_api.get_cards_six_history()
            record_six_str = ''
            for record_six_item in record_six:
                if not record_six_str == '':
                    record_six_str += '\n'
                    if self.push_type == 'serverchan':
                        record_six_str += '\n'
                time_local = time.localtime(record_six_item['TIME'])
                datatime = time.strftime(self.push_body_config.get('cards_record_six').get('format_datatime'), time_local)
                name = record_six_item['NAME']
                if record_six_item['ISNEW'] == True:
                    name += '(NEW)'
                record_six_str += self.push_body_config.get('cards_record_six').get('format').format(datatime, record_six_item['POOL'], name, record_six_item['COUNT'])

            if not out_str == '':
                out_str += '\n\n'
                if self.push_type == 'serverchan':
                    out_str += '\n'
            s_title = self.push_body_config.get('cards_record_six').get('format_main')
            if not s_title == '':
                out_str += s_title
                out_str += '\n'
                if self.push_type == 'serverchan':
                    out_str += '\n'
            out_str += record_six_str
        
        return out_str

    def push_by_bark(self, body):
        bark_url = self.push_type_config.get('url')
        data = {
            'title': self.push_type_config.get('title'),
            'body': body,
            'device_key': self.push_type_config.get('device_key'), 
            'badge': self.push_type_config.get('badge'),
            'group': self.push_type_config.get('group'),
            'isArchive': self.push_type_config.get('isArchive')
        }
        r = requests.post(bark_url, data=data)
        if r.status_code == 200:
            return r.content
        return 'ERROR'

    def push_by_serverchan(self, body):
        serverchan_url = 'https://sctapi.ftqq.com/{}.send'.format(self.push_type_config.get('send_key'))
        data = {
            'title': self.push_type_config.get('title'),
            'desp': body
        }
        r = requests.post(serverchan_url, data=data)
        response = json.loads(r.content)
        if r.status_code == 200:
            return r.content
        print('ERROR: ServerChan Refused! Response: {}'.format(response))
        return 'ERROR'

    def push(self, body):
        push_type_list =['bark', 'serverchan']
        if not self.push_type in push_type_list:
            print(body)
        if self.push_type == 'bark':
            self.push_by_bark(body)
        if self.push_type == 'serverchan':
            self.push_by_serverchan(body)
