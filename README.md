# Arknights_Cards_Analysis
 明日方舟寻访记录拉取，从官网拉取保存在本地，并汇总分析后推送到手机。

# 使用

自行配置 python 环境，并使用 pip 安装 requests 包。

## token 获取

进入官网个人中心，即 https://ak.hypergryph.com/user/home。

按 F12 打开控制台，进入 Network 一栏，刷新该页面。在请求中找到 token_by_cookie 一项，找到其 Response 中的 token，记录下来。

该 token 仅能查询官网能查到的相关数据。

![image-20220206222024946](https://gitee.com/fateicr/image-bed/raw/master/Image/202202062220152.png)

## 预设脚本

将 arknights_cards.py, pull_to_db.py, push_to_bark.py 放入同一目录下。而后通过定时任务每隔一段时间（半个小时或其他）运行 pull_to_db.py 拉取数据到本地数据库，并通过定时任务每天一次运行 push_to_bark.py 推送当日寻访数据到手机。

### pull_to_db.py

运行前请自行修改该文件中的 tokens 列表，填入 token。如果多账号即按照 python 列表规则在 tokens 中追加。

运行该 py 文件后会从官网拉取寻访记录数据并存入数据库。适合于在服务器中使用定时任务每隔一段时间运行一次，自行同步数据到服务器，防止官网数据超过一个月自动清理。

### push_to_bark.py

运行前同样需要修改 tokens 列表填入 token。

该文件将 arknights_cards 中处理过的数据格式化输出推送出来。因笔者个人习惯，此处使用了 Bark 推送，如需 ServerChan 等其他推送，可自行二次开发。

## 自定义脚本

### test.py

该文件中展示了所有可使用的功能及其输出。

```python
from arknights_cards import *

tokens = ['tokne1', 'token2'] # TODO Token
for token in tokens:
    ak_cards = arknights_cards(token, 'ak_server.db') # TODO 数据库名称需要统一
    ak_cards.show() # 显示当前用户数据
    ak_cards.update_cards_db() # 将获取到的寻访记录增量更新到数据库中

    ak_cards.get_cards_number() # 获取抽卡详细数据，即总计抽数，以及每个星级的抽数
    ak_cards.get_cards_number_pool() # 获取各卡池抽卡次数
    ak_cards.get_cards_pool_guarantee_count() # 获取各卡池保底状况，即已累计多少抽未出六星
    ak_cards.get_cards_six_history() # 获取抽到的六星历史记录
    ak_cards.get_cards_count_avg() # 获取各卡池平均出货抽数
```

### arknights_cards.py

arknights_cards.py 中的 arknights_cards 类提供了所有可使用的功能，arknights_database 类 arknights_cards 类提供了数据库操作，arknights_api 类则负责对官网 api 的请求。

arknights_cards:

```python
################################
# 初始化
# params:
#   token: token
#   db_name: sqlite 数据库名称
################################
def __init__(self, token, db_name)

################################
# 显示当前用户数据
# return:
#   {
#       "uid": "用户UID",
#       "nickName": "昵称"
#   }
################################
def show(self)

################################
# 将获取到的寻访记录增量更新到数据库中
# return:
#   None
################################
def update_cards_db(self)

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
def get_cards_number(self)

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
def get_cards_number_pool(self)

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
def get_cards_pool_guarantee_count(self)

################################
# 获取抽到的六星历史记录
# return:
#   [
#       {
#           "TIME": 该六星出货的时间戳,
#           "POOL": 该六星出货的池子,
#           "NAME": 该六星名称,
#           "ISNEW": 该六星是否首次获得,
#           "COUNT": 该六星出货时的保底抽数
#       },
#       ...
#   ]
################################
def get_cards_six_history(self)

################################
# 获取各卡池平均出货抽数
# return:
#   {
#       "global": 全局平均出货抽数,
#       "池子": 该池子平均出货抽数
#       ...
#   }
################################
def get_cards_count_avg(self)
```

