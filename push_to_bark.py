from arknights_cards import *
import time

tokens = ['token1', 'token2'] # TODO Token
for token in tokens:
    ak_cards = arknights_cards(token, 'ak_server.db') # TODO 数据库名称需要统一

    user_info_dict = ak_cards.show() # 显示当前用户数据
    uid = user_info_dict['uid']
    nickName = user_info_dict['nickName']
    user_info_str = 'UID: {}, NickName: {}\n'.format(uid, nickName)

    ak_cards.update_cards_db() # 将获取到的寻访记录增量更新到数据库中

    cards_numbers = ak_cards.get_cards_number() # 获取抽卡详细数据，即总计抽数，以及每个星级的抽数
    cards_numbers_str = '\n共抽卡 {} 次，其中六星 {} 次，五星 {} 次。\n'.format(cards_numbers['all'], cards_numbers['6'], cards_numbers['5'])

    pool_counts = ak_cards.get_cards_pool_guarantee_count() # 获取各卡池保底状况，即已累计多少抽未出六星
    pool_counts_str = '\n保底情况：\n'
    for pool in pool_counts: 
        pool_counts_str += '{}: 抽数: {}, 下一抽概率: {}%\n'.format(pool, pool_counts[pool]['count'], pool_counts[pool]['probability_next'])

    six_history = ak_cards.get_cards_six_history() # 获取抽到的六星历史记录
    six_history_str = '\n历史抽取六星：'
    for six_item in six_history:
        time_local = time.localtime(six_item['TIME'])
        dt = time.strftime('%Y-%m-%d %H:%M', time_local)
        if six_item['ISNEW'] == True:
            six_history_str += '\n{}: {}: {}(NEW), 抽数: {}'.format(dt, six_item['POOL'], six_item['NAME'], six_item['COUNT'])
        else:
            six_history_str += '\n{}: {}: {}, 抽数: {}'.format(dt, six_item['POOL'], six_item['NAME'], six_item['COUNT'])


    out_str = user_info_str + cards_numbers_str + pool_counts_str + six_history_str
    print(out_str)

    bark_url = 'https://bark.rianng.cn/push'
    data = {
        'title': 'Arknights 寻访记录',
        'body': out_str,
        'device_key': 'aaaaaaa', # TODO Bark 设备码
        'badge': 1,
        'group': 'Arknights'
    }
    arknights_api.request_api.post(bark_url, data)