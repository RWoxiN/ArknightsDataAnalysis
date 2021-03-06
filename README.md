# Arknights_Data_Analysis

 明日方舟寻访记录拉取，从官网拉取保存在本地，并汇总分析后推送到手机。

https://github.com/RWoxiN/ArknightsDataAnalysis

更新日志：

v2.2.0 加入用户账号功能，用以区分个人 Arknights 账号。删除配置文件中账号配置选项，暂时取消推送功能，如需推荐可以先退回旧版本。

v2.1.1 加入强制刷新数据功能，需从配置中开启，web 端中自带强制刷新按钮，用于解决卡池刚更新时官网数据中存在未知寻访的问题。

v2.1.0 加入 web 端，完成新增账号功能。

v2.0.1 加入充值记录功能。

v2.0.0 内容重构，使用 ORM 框架 peewee 对数据进行存储操作，并取消了推送自定义内容功能。

v1.0.2: 添加 mysql 数据库和 ServerChan 推送的支持。增加了配置文件动态适配新版本的功能。

v1.0.1: 完成基础功能，支持 sqlite3 数据库以及 bark 推送。

# 图示

![image-20220304234523725](https://gitee.com/RWoxiN/image-bed/raw/master/Image/202203042345845.png)

![image-20220304234729841](https://gitee.com/RWoxiN/image-bed/raw/master/Image/202203042347956.png)

![image-20220304234742023](https://gitee.com/RWoxiN/image-bed/raw/master/Image/202203042347141.png)

# 使用

## 安装

### 手动安装

1. 在需要放置脚本的目录 `git clone https://github.com/RWoxiN/ArknightsDataAnalysis.git`，无法连接 github 的话，可使用 gitee 库 `git clone https://gitee.com/RWoxiN/ArknightsDataAnalysis.git `。
2. 自行配置 python3 环境，并使用 pip 安装依赖库 `pip install -r requirments.txt`。
3. 运行 `python main.py`。初次使用会生成 config.json 然后结束程序运行，待完成配置文件修改后再次运行即可正常使用。配置文件版本较旧时会根据配置进行推送警告，为了程序正常运行，请尽快修改配置文件。
4. 在配置文件完成修改后运行 `python main.py` 即可拉取寻访记录到数据库并根据配置进行推送。
5. 通过 crontab 定时执行。

更新：在文件目录下 `git pull` 即可获取最新版到本地。

## 通过 shell 脚本定时执行

1. git clone 后进入目录，并运行 `python -m venv venv` 在本地创建虚拟环境。

2. 创建 start.sh 脚本。

    ```bash
    #!/bin/bash
    vardate=$(date +%c)
    varpath="/home/rian/arknights/ArknightsDataAnalysis"
    cd ${varpath}
    source ./venv/bin/activate
    python ./main.py
    echo "${vardate}: runing succeed!" >> ./start.log 2>&1
    ```

3. 给 Shell 脚本添加权限。`chmod u+x start.sh`

4. 执行 `sh start.sh` 测试运行，并配置配置文件。

5. 设置定时任务 `crontab -e`：

    ```
    */5 * * * * /home/rian/arknights/ArknightsDataAnalysis/start.sh >> /home/rian/arknights/ArknightsDataAnalysis/start.log 2>&1
    ```

## web 端使用

web 端尚未开发完全，目前仍需要定时运行 `main.py` 来保证数据的定时爬取录入数据库。

1. 进入 python 虚拟环境，运行 `python app.py`。

2. 默认端口为 8900，可自行修改 `app.py` 来改变端口。

3. 通过 nginx 将端口反代到域名，或直接使用 `yourip:8900` 测试访问。

使用方式：

获取 token 后输入 token，点击 Refresh。如果下方显示正确的账号信息，则点击 Add 将该账号添加到账号列表中，而后便可以在左侧的账号列表中查看详情。


## token 获取

进入官网个人中心，即 https://ak.hypergryph.com/user/home

按 F12 打开控制台，进入 Network 一栏，刷新该页面。在请求中找到 token_by_cookie 一项，找到其 Response 中的 token，记录下来。

该 token 仅能查询官网能查到的相关数据。

![image-20220206222024946](https://gitee.com/RWoxiN/image-bed/raw/master/Image/202202062220152.png)

## 配置文件

首次运行时会在本地目录自动生成 config.json。需手动修改配置文件后方可正常运行程序。

在版本更新后，程序会自动更新配置文件，将旧版本迁移到新版本，配置文件中新增的功能如要使用还需手动配置。

### 强制刷新配置

强制刷新用于解决卡池刚更新时官网数据中存在未知寻访的问题。

普通刷新只会从官网拉取数据库中存储的最后一次寻访以后的数据，而强制刷新会从数据库中拉取所有数据，并覆盖数据库过往数据中卡池名称不匹配的数据。

如账号较多建议关闭，每次卡池更新后，出现未知寻访记录的话待官网数据恢复正常手动强制刷新一次。

根据个人需求自行取舍。一者单次刷新耗时长但会自动修复错误数据；一者单次刷新时间短但需要偶尔手动刷新，如果忘记刷新导致官网数据过期，该条未知寻访卡池的记录将无法弥补，除非自己进数据库慢慢改...

```json
"force_refresh": {
    "enabled": 0
}
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

### 推送配置

```json
"push": {
    "enabled": 1,
    "type": "bark",
    "push_when_changed": {
        "enabled": 1
    },
    "bark": {
        "url": "",
        "device_key": "",
        "title": "Arnights 寻访记录",
        "group": "Arknights",
        "badge": 1,
        "isArchive": 1
    },
    "serverchan": {
        "send_key": "",
        "title": "Arnights 寻访记录"
    }
}
```

| 参数    | 描述                                     |
| ------- | ---------------------------------------- |
| enabled | 推送状态，0 为不启用推送，1 为启用推送。 |
| type    | 推送类型。                               |

| type       | 描述                                    |
| ---------- | --------------------------------------- |
| bark       | iOS 端推送 APP。                        |
| serverchan | Server酱推送，SendKey 需要是 SCT 开头。 |

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

#### serverchan

Server 酱: https://sct.ftqq.com

| 参数     | 描述                                        | 必填 |
| -------- | ------------------------------------------- | ---- |
| send_key | SendKey，请前往 Server 酱官网自行注册获取。 | True |
| title    | 推送标题。                                  |      |

