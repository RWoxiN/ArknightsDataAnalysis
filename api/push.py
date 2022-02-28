# -*- coding: utf-8 -*-
from unicodedata import name
from .config import *
import time, requests

class ada_push():
    def __init__(self):
        a_config = ada_config()
        self.push_type, self.push_type_config = a_config.load_config_push()

    def parse_body(self, body):
        def parse_block(title, info):
            o_str = ''
            if not title == '':
                o_str += title
                o_str += '\n'
                if self.push_type == 'serverchan':
                    o_str += '\n'
            o_str += info
            return o_str

        def add_n(num=1):
            o_str = ''
            for i in range(1, num+1):
                o_str += '\n'
            if self.push_type == 'serverchan':
                o_str += '\n'
            return o_str
        
        out_str = ''
        
        title = '当前用户：'
        info_str = 'UID: {0}, NickName: {1}.'.format(
            body['acc_info']['uid'],
            body['acc_info']['nickName']
        )
        out_str += parse_block(title, info_str)


        title = '统计时间：'
        info_str = '{0} - {1}'.format(
            body['osr_info']['time']['start_time'],
            body['osr_info']['time']['end_time']
        )
        out_str += add_n(2)
        out_str += parse_block(title, info_str)


        title = '抽卡详细数据：'
        info_str = '总计 {0} 抽。'.format(
            body['osr_info']['osr_number']['total']['all']
        )
        for i in range(6, 2, -1):
            info_str += add_n()
            info_str += '{0} 星：{1} 抽，占 {2} %。'.format(
                i,
                body['osr_info']['osr_number']['total'][str(i)],
                round(body['osr_info']['osr_number']['total'][str(i)] / body['osr_info']['osr_number']['total']['all'] * 100, 2)
            )
        out_str += add_n(2)
        out_str += parse_block(title, info_str)


        title = '平均出货次数：'
        info_str = '六星 {0} 抽，五星 {1} 抽。'.format(
            round(body['osr_info']['osr_lucky_avg']['6'], 2),
            round(body['osr_info']['osr_lucky_avg']['5'], 2)
        )
        out_str += add_n(2)
        out_str += parse_block(title, info_str)


        title = '各卡池抽卡次数：'
        info_str = ''
        for item in body['osr_info']['osr_number']:
            if info_str != '':
                info_str += add_n()
            if item == 'total':
                continue
            info_str += '{0}: {1} 抽。'.format(
                item,
                body['osr_info']['osr_number'][item]
            )
        out_str += add_n(2)
        out_str += parse_block(title, info_str)


        title = '各卡池保底情况：'
        info_str = ''
        for item in body['osr_info']['osr_lucky_count']:
            if info_str != '':
                info_str += add_n()
            info_str += '{0}: 已累计 {1} 抽未出 6 星。'.format(
                item,
                body['osr_info']['osr_lucky_count'][item]['6']
            )
        out_str += add_n(2)
        out_str += parse_block(title, info_str)


        title = '每月抽卡次数：'
        info_str = ''
        for item in body['osr_info']['osr_number_month']:
            if info_str != '':
                info_str += add_n()
            info_str += '{0}:  {1} 抽。'.format(
                item,
                body['osr_info']['osr_number_month'][item]
            )
        out_str += add_n(2)
        out_str += parse_block(title, info_str)


        title = '六星历史记录：'
        info_str = ''
        for item in body['osr_info']['osr_six_record']:
            if info_str != '':
                info_str += add_n()
            info_str += '{0} [{1}] {2}{3} ({4})'.format(
                item['time'],
                item['count'],
                item['name'],
                '(NEW)' if item['is_new'] else '',
                item['pool']
            )
        out_str += add_n(2)
        out_str += parse_block(title, info_str)

        if int(body['pay_info']['total_money']) == 0:
            title = '充值记录（共 ￥0）'
            info_str = '无'
        else:
            title = '充值记录（共 ￥{0}）：'.format(body['pay_info']['total_money'])
            info_str = ''
            for item in body['pay_info']['pay_info']:
                if info_str != '':
                    info_str += add_n()
                info_str += '{0} ￥{1} {2} ({3})'.format(
                    item['time'],
                    item['amount'],
                    item['name'],
                    item['platform']
                )
        out_str += add_n(2)
        out_str += parse_block(title, info_str)

        # print(out_str)
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