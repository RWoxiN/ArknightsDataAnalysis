# Arknights_Cards_Analysis

 明日方舟寻访记录拉取，从官网拉取保存在本地，并汇总分析后推送到手机。

https://github.com/RWoxiN/Arknights_Cards_Analysis

# 使用

1. 在需要放置脚本的目录 `git clone https://github.com/RWoxiN/Arknights_Cards_Analysis.git`，无法连接 github 的话，可使用 gitee 库 `git clone https://gitee.com/RWoxiN/Arknights_Cards_Analysis.git `。

2. 自行配置 python3 环境，并使用 pip 安装依赖库 `pip install -r requirments.txt`。

3. 运行 `python main.py`。初次使用会生成 config.json 然后结束程序运行，待完成配置文件修改后再次运行即可正常使用。配置文件版本较旧时会根据配置进行推送警告，为了程序正常运行，请尽快修改配置文件。

4. 在配置文件完成修改后运行 `python main.py` 即可拉取寻访记录到数据库并根据配置进行推送。

5. 通过 crontab 定时执行。

## 通过 shell 脚本定时执行

1. git clone 后进入目录，并运行 `python -m venv venv` 在本地创建虚拟环境。

2. 创建 start.sh 脚本。

    ```bash
    #!/bin/bash
    vardate=$(date +%c)
    varpath="/home/rian/arknights/Arknights_Cards_Analysis"
    cd ${varpath}
    source ./venv/bin/activate
    python ./main.py
    echo "${vardate}: runing succeed!" >> ./start.log 2>&1
    ```

3. 给 Shell 脚本添加权限。`chmod u+x start.sh`

4. 执行 `sh start.sh` 测试运行，并配置配置文件。

5. 设置定时任务 `crontab -e`：

    ```
    */5 * * * * /home/rian/arknights/Arknights_Cards_Analysis/start.sh >> /home/rian/arknights/Arknights_Cards_Analysis/start.log 2>&1
    ```

## token 获取

进入官网个人中心，即 https://ak.hypergryph.com/user/home

按 F12 打开控制台，进入 Network 一栏，刷新该页面。在请求中找到 token_by_cookie 一项，找到其 Response 中的 token，记录下来。

该 token 仅能查询官网能查到的相关数据。

![image-20220206222024946](https://gitee.com/RWoxiN/image-bed/raw/master/Image/202202062220152.png)

## 配置文件

首次运行时会在本地目录自动生成 config.json。需手动修改配置文件后方可正常运行程序。

### 当前版本

```json
"version": "v1.0.1"
```

### 数据库配置


目前支持 sqlite3、mysql。

```json
"database": {
    "type": "sqlite3",
    "sqlite3": {
        "filename": "ak_server.db"
    },
    "mysql": {
        "host": "",
        "user": "",
        "password": "",
        "database": ""
    }
}
```
| type    | 描述          |
| ------- | ------------- |
| sqlite3 | SQLite 数据库 |
| mysql   | MySQL 数据库  |

#### sqlite3

| 参数     | 描述                  |
| -------- | --------------------- |
| filename | SQLite 数据库默认路径 |

#### mysql

使用 mysql 前请自行创建一个数据库，并将其名称填入 database 参数中，数据表会在库中自动创建。

| 参数     | 描述                                         | 必填 |
| -------- | -------------------------------------------- | ---- |
| host     | 数据库主机地址，本地数据库地址为 localhost。 | True |
| user     | 数据库用户名                                 | True |
| password | 数据库密码                                   | True |
| database | 数据库库名                                   | True |

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

| 参数           | 描述                                                         | 必填 |
| -------------- | ------------------------------------------------------------ | ---- |
| name           | 没有用处，多账号时供用户在配置文件中辨别不同 token 的归属账号。 |      |
| token          | 前文获取到的账号 token。                                     | True |
| push_timestamp | 根据配置自动生成，无需修改。截止上一次推送时的最后一次抽卡时间。 |      |

可自行增加项来添加账号，别忘了逗号 `,`。

### 推送配置

```json
"push": {
    "enabled": 1,
    "type": "bark",
    "push_when_changed": {
        "enabled": 1
    },
    "bark": {
        "url": "https://bark.rianng.cn/push",
        "device_key": "7uCfQUL363kCTQt2nibf2C",
        "title": "Arnights 寻访记录",
        "group": "Arknights",
        "badge": 1,
        "isArchive": 1
    },
    "body": {}
}
```

| 参数    | 描述                                     |
| ------- | ---------------------------------------- |
| enabled | 推送状态，0 为不启用推送，1 为启用推送。 |
| type    | 推送类型。                               |

| type | 描述             |
| ---- | ---------------- |
| bark | iOS 端推送 APP。 |

#### push_when_changed

 仅当数据变化时推送。可开启该项部署在服务器短间隔定时运行程序，当用户抽卡后即会自动推送；如果不开启此项，则每次运行程序都会推送一次。

| 参数    | 描述                   |
| ------- | ---------------------- |
| enabled | 0 为不启用，1 为启用。 |

#### bark

Bark: https://github.com/Finb/Bark

iOS 端用户可直接在 app store 下载安装 Bark。

如需自行架设 Bark 服务，可参考 https://github.com/Finb/bark-server

| 参数       | 描述                                                         | 必填 |
| ---------- | ------------------------------------------------------------ | ---- |
| url        | Bark Post 方式推送所使用的 url，使用 Bark 官方服务则为 `https://api.day.app/push`。 | True |
| device_key | 设备码，可自行在 Bark 客户端查看。                           | True |
| title      | 推送标题。                                                   |      |
| group      | 推送消息分组。                                               |      |
| badge      | 推送设置角标。                                               |      |
| isArchive  | 自动保存通知消息。                                           |      |

以上参数均可在 Bark 客户端查看详细说明。

#### body

推送内容配置

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

| 通用参数           | 描述                                       |
| ------------------ | ------------------------------------------ |
| enabled            | 该项内容启用状态                           |
| format_main        | 该项内容总览标题。                         |
| format             | 该项内容格式。                             |
| description        | 该项内容描述，仅作说明。                   |
| params_description | 该项内容各参数描述及其对应序号，仅作说明。 |

format 项中使用 `{}` 内置整数作为变量调用。比如 user_info 中，`{0}` 代表用户 UID，`{1}` 代表用户昵称，format 设为 `"我的UID是 {0}，昵称是 {1}."`，format_main 设为 `这是我的用户信息:`，假设该用户 UID 为 12345，用户名为 粉毛，那么该项内容结果为：

```
这是我的用户信息:
我的UID是 12345，昵称是 粉毛.
```

##### user_info

显示当前用户数据。

| 参数序号 | 描述    |
| -------- | ------- |
| 0        | 用户UID |
| 1        | 昵称    |

##### cards_record

显示抽卡详细数据，即总计抽数，以及每个星级的抽数。

| 参数序号 | 描述           |
| -------- | -------------- |
| 0        | 总抽数         |
| 1        | 抽到的六星总数 |
| 2        | 抽到的五星总数 |
| 3        | 抽到的四星总数 |
| 4        | 抽到的三星总数 |

##### cards_record_pool

获取各卡池抽卡次数，以及各卡池中每个星级的抽数

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

| 参数序号 | 描述                 |
| -------- | -------------------- |
| 0        | 池子                 |
| 1        | 该池子当前保底抽数   |
| 2        | 该池子下一抽出货概率 |

##### cards_count_avg

获取各卡池平均出货抽数

| 参数序号 | 描述               |
| -------- | ------------------ |
| 0        | 池子               |
| 1        | 该池子平均出货抽数 |

##### cards_record_six

获取抽到的六星历史记录

| 参数            | 描述                                       |
| --------------- | ----------------------------------------- |
| format_datatime | `{0}` 时间的格式，默认为 `%Y-%m-%d %H:%M`。 |

| 参数序号 | 描述               |
| -------- | ------------------ |
| 0        | 该六星出货的时间   |
| 1        | 该六星出货的池子   |
| 2        | 该六星名称         |
| 3        | 该六星出货时的抽数 |
