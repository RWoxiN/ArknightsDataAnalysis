# -*- coding: utf-8 -*-
from tkinter import N
from .config import *
from .data import *
from .push import *

class ada_api():
    ################################
    # 初始化并将官网数据增量更新到数据库
    # params:
    #   token: token
    ################################
    def __init__(self, token, only_read=False, force_refresh=False):
        self.a_data = ada_data(token)
        if not only_read:
            self.a_data.fetch_data(force_refresh)
            self.a_push = ada_push()
        else:
            self.a_data.fetch_account_info()
        self.account = self.a_data.account

    ################################
    # 显示当前用户数据
    # return:
    #   {
    #       "uid": "用户UID",
    #       "nickName": "昵称"
    #   }
    ################################
    def get_account_info(self):
        acc_info = {
            'uid': self.account.uid,
            'nickName': self.account.nickname,
            'token': self.account.token
        }
        # print(acc_info)
        return acc_info

    ################################
    # 获取抽卡详细数据，即总计抽数，以及每个星级的抽数
    # return:
    #   {
    #       'time': {
    #           'start_time': "抽卡记录开始时间",
    #           'end_time': "抽卡记录结束时间"
    #       },
    #       'osr_number': "抽卡详细数据及各卡池抽卡次数"
    #       'osr_lucky_avg': "平均出货次数",
    #       'osr_lucky_count': "各卡池保底情况",
    #       'osr_six_record': "6星历史记录",
    #       'osr_number_month': "每月抽卡次数"
    #   }
    ################################
    def get_osr_info(self):
        osr_info = self.a_data.get_osr_info()
        return osr_info

    ################################
    # 获取充值记录
    # return:
    #   'total_money': "重置总记录"
    #   'pr_info': [{
    #       'time': "时间"
    #       'name': "名称",
    #       'amount': "金额",
    #       'platform': "平台"
    #   },...]
    ################################
    def get_pay_record(self):
        total_money, pr_info = self.a_data.get_pay_record()
        return total_money, pr_info
    
    ################################
    # 获取所有信息
    ################################
    def get_all_info(self):
        osr_info = self.get_osr_info()
        acc_info = self.get_account_info()
        total_money, pay_info = self.get_pay_record()
        info = {
            'acc_info': acc_info,
            'osr_info': osr_info,
            'pay_info': {
                'total_money': total_money, 
                'pay_info': pay_info
            }
        }
        return info

    ################################
    # 发送推送
    ################################
    def push(self, push_time=None):
        end_time = self.account.records.order_by(OperatorSearchRecord.time.desc()).limit(1)[0].time
        end_ts = time.mktime(end_time.timetuple())
        if push_time is not None:
            if end_ts <= push_time:
                return end_ts

        info = self.get_all_info()

        push_body = self.a_push.parse_body(info)
        self.a_push.push(push_body)
        return end_ts

