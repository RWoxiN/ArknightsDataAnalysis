# Arknights_Cards_Analysis
 明日方舟寻访记录拉取，从官网拉取保存在本地，并汇总分析后推送到手机。

# 使用

1. 自行配置 python3 环境，并使用 pip 安装 requests 包。
2. 在需要放置脚本的目录 `git clone https://github.com/RWoxiN/Arknights_Cards_Analysis.git`，如果是腾讯云之类墙了 github 的话，可使用 `git clone https://hub.fastgit.xyz/RWoxiN/Arknights_Cards_Analysis.git `。
3. 运行 `python pull_to_db.py` 生成 config.json。如本地已有 config.json 可忽略此步骤，如本地 config.json 版本落后于仓库版本，则需删除后重新生成。当前 config.json 版本为 v1.0。
4. 修改 config.json 配置文件。详见下文。
5. 此时使用 `python pull_to_db.py` 即可拉取寻访记录到数据库。使用 `python push_to_bark.py` 即可分析数据并进行推送。
6. 通过 crontab 定时执行。



## token 获取

进入官网个人中心，即 https://ak.hypergryph.com/user/home

按 F12 打开控制台，进入 Network 一栏，刷新该页面。在请求中找到 token_by_cookie 一项，找到其 Response 中的 token，记录下来。

该 token 仅能查询官网能查到的相关数据。

![image-20220206222024946](https://gitee.com/RWoxiN/image-bed/raw/master/Image/202202062220152.png)

## 配置文件

首次运行 pull_to_db.py 时会在本地目录自动生成 config.json。需手动修改配置文件后方可正常运行程序。

### 数据库配置


目前仅支持 sqlite3。

```json
"database": {
    "type": "sqlite3",
    "sqlite3": {
        "filename": "arknights_cards.db"
    }
}
```
可通过 database -> sqlite3 -> filename 来修改 sqlite 数据库文件名。

### 账号配置

```json
"accounts": [
    {
        "name": "",
        "token": ""
    },
    {
        "name": "",
        "token": ""
    }
]
```

name: 没有用处，多账号时供用户辨别不同 token 的归属账号。

token: 前文获取到的 token。

可自行增加项来添加账号，别忘了逗号 `,`。

### Bark 配置

Bark: https://github.com/Finb/Bark

iOS 端用户可直接在 app store 下载安装 Bark。

如需自行架设 Bark 服务，可参考 https://github.com/Finb/bark-server

```json
"bark": {
    "url": "",
    "device_key": "",
    "title": "Arnights 寻访记录",
    "group": "Arknights",
    "badge": 1,
    "isArchive": 1,
    "body": {}
}
```

| 参数       | 描述                                                         |
| ---------- | ------------------------------------------------------------ |
| url        | Bark Post 方式推送所使用的 url，使用 Bark 官方服务则为 `https://api.day.app/push`。 |
| device_key | 设备码，可自行在 Bark 客户端查看。                           |
| title      | 推送标题。                                                   |
| group      | 推送消息分组。                                               |
| badge      | 推送设置角标。                                               |
| isArchive  | 自动保存通知消息。                                           |

以上参数均可在 Bark 客户端查看详细说明。

#### 不同账号自定义 Bark 配置

可通过在 accounts 项中 添加 bark 项的方式自定义配置不同账号使用的不同推送方式，除 body 项（推送内容配置）外，如需配置 body 项，则需要将全局 bark 配置中的 body 项全部复制过去再进行修改。优先使用 accounts 中配置的 bark 配置，如果找不到则使用全局配置。

```json
"accounts": [
    {
        "name": "Hello",
        "token": "this is a token",
        "bark": {
            "title": "this is a new title created by accounts"
        }
    },
    {
        "name": "World",
        "token": "this is a token"
    }
]
```

以上配置中，Hello 这一项的推送标题会被改变，而 World 这一项使用全局默认配置。

#### Bark 推送内容配置

```json
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
    "cards_record_six": {
        "enabled": 1,
        "format_main": "历史抽取六星：",
        "format": "{0}: {1}: {2}, 抽数: {3}",
        "format_datatime": "%Y-%m-%d %H:%M",
        "description": "显示抽卡详细数据，即总计抽数，以及每个星级的抽数",
        "params_description": "{0}: 该六星出货的时间. {1}: 该六星出货的池子. {2}: 该六星名称. {3}: 该六星出货时的抽数."
    }
}
```

| 参数               | 描述                                       |
| ------------------ | ------------------------------------------ |
| enabled            | 该项内容启用状态                           |
| format_main        | 该项内容总览标题。                         |
| format             | 该项内容格式。                             |
| description        | 该项内容描述，仅作说明。                   |
| params_description | 该项内容各参数描述及其对应序号，仅作说明。 |

##### user_info

显示当前用户数据。

params:

| 参数序号 | 描述    |
| -------- | ------- |
| 0        | 用户UID |
| 1        | 昵称    |

##### cards_record

显示抽卡详细数据，即总计抽数，以及每个星级的抽数。

params:

| 参数序号 | 描述           |
| -------- | -------------- |
| 0        | 总抽数         |
| 1        | 抽到的六星总数 |
| 2        | 抽到的五星总数 |
| 3        | 抽到的四星总数 |
| 4        | 抽到的三星总数 |

##### cards_record_pool

获取各卡池抽卡次数，以及各卡池中每个星级的抽数

params:

| 参数序号 | 描述                 |
| -------- | -------------------- |
| 0        | 池子                 |
| 1        | 该池子总抽数         |
| 2        | 该池子抽到的六星总数 |
| 3        | 该池子抽到的五星总数 |
| 4        | 该池子抽到的四星总数 |
| 5        | 该池子抽到的三星总数 |

##### cards_pool_guarantee

获取各卡池保底状况，即已累计多少抽未出六星

params:

| 参数序号 | 描述                 |
| -------- | -------------------- |
| 0        | 池子                 |
| 1        | 该池子当前保底抽数   |
| 2        | 该池子下一抽出货概率 |

##### cards_count_avg

获取各卡池平均出货抽数

params:

| 参数序号 | 描述               |
| -------- | ------------------ |
| 0        | 池子               |
| 1        | 该池子平均出货抽数 |

##### cards_record_six

获取抽到的六星历史记录

params:

| 参数序号 | 描述               |
| -------- | ------------------ |
| 0        | 该六星出货的时间   |
| 1        | 该六星出货的池子   |
| 2        | 该六星名称         |
| 3        | 该六星出货时的抽数 |

## 预设脚本

### pull_to_db.py

运行前请自行修改配置文件。

运行该 py 文件后会从官网拉取寻访记录数据并存入数据库。适合于在服务器中使用定时任务每隔一段时间运行一次，自行同步数据到服务器，防止官网数据超过一个月自动清理。

### push_to_bark.py

运行前请自行修改配置文件。

该文件会先从官网同步一次数据后再将 arknights_cards 中处理过的数据格式化输出推送出来。因笔者个人习惯，此处使用了 Bark 推送，如需 ServerChan 等其他推送，可自行二次开发。

## 自定义脚本

### arknights_cards.py

arknights_cards.py 中的 arknights_cards 类提供了所有可使用的功能，arknights_database 类为 arknights_cards 类提供了数据库操作，arknights_api 类则负责对官网 api 的请求。

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

