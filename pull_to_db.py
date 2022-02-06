from arknights_cards import *

# 服务器定时运行，仅拉取保存到数据库
tokens = ['token1', 'token2'] # TODO Token
for token in tokens:
    ak_cards = arknights_cards(token, 'ak_server.db') # TODO 数据库名称需要统一
    ak_cards.update_cards_db() # 将获取到的寻访记录增量更新到数据库中更新