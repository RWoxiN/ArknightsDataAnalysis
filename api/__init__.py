# -*- coding: utf-8 -*-
from .database import *
from .http import *

from .config import *
from .push import *

class arknights_api():

    ################################
    # 初始化
    # params:
    #   token: token
    #   db_name: sqlite 数据库名称
    ################################
    def __init__(self, token, config_file=None):
        self.ak_http = arknights_http(token)
        self.ak_db = arknights_database(config_file)

        user_info_dict = self.ak_http.get_user_info()

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
    def get_user_info(self):
        user_info_dict = self.ak_http.get_user_info()
        # print('uid: {}, nickName: {}'.format(user_info_dict['uid'], user_info_dict['nickName']))
        return user_info_dict

    ################################
    # 将获取到的寻访记录增量更新到数据库中
    # return:
    #   最后一次抽卡时间戳
    ################################
    def update_cards_db(self):
        last_timestamp_dict = self.ak_db.get_last_timestamp(self.uid)
        cards_record_data_list = self.ak_http.get_cards_record(last_timestamp_dict['global'])
        self.ak_db.insert_cards(self.uid, cards_record_data_list)
        self.ak_db.update_count(self.uid, last_timestamp_dict)
        last_timestamp_dict = self.ak_db.get_last_timestamp(self.uid)
        return last_timestamp_dict['global']

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