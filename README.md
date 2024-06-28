# Kokomi_bot 部署教程 （V 4.0.0+） 

## 前言

1. Kokomi 并不是一个完整的bot，需要依赖 `频道SDK` 实现功能

2. 点击右边的Releases下载最新版本文件

3. **开发者交流群（462447502）**

## 第一步-配置环境

> 开发环境的 python 版本 3.8.10

### 1.1 安装需要使用的python模块

插件会使用到的模块有: `pillow` (PIL) , `opencv-python` (cv2) , `httpx`

使用以下的命令可以查看当前 python 环境内已安装的包。
```
pip list
```
对于没有进行过python开发的小白来说，python是没有自带这几个模块

如果上述需要模块不存在，您可以通过手动安装

<details>
<summary>手动安装python包</summary>

特别注意：如果使用了虚拟环境，请在虚拟环境内安装相关模块，需要先进入虚拟环境再安装python包(小白不建议使用虚拟环境)

```
# 安装指定模块
pip install 模块名

# 安装指定模块的指定版本
pip install 模块名==指定版本号

# 卸载指定模块
pip uninstall 模块名

# 示例
pip install pillow
```
当系统中同时存在多个 Python 版本时，可能会存在多个 pip 版本

当执行 pip install 命令时没有指定 Python 解释器时，pip 是与默认 Python 版本关联的

为了确保在多个 Python 版本的环境中正确安装和使用软件包，最好明确指定要使用的 Python 和 pip 版本。

</details>


### 1.2 安装字体(可能需要)


**linux**和**部分windows**系统需要将插件文件内的字体文件丢到系统的字体文件夹内才能加载字体

```
插件字体文件:kokomi_bot_plugin\seripts\fonts\xxxx.ttf

linux系统字体文件夹:/usr/share/font
windows系统字体文件夹:C:\Windows\Fonts
```

### 1.3 配置token和config

config文件路径：kokomi_bot_plugin\config.py

```python
class Plugin_Config:
    # 数据接口相关配置，以下数据默认配置已好
    API_URL = ''
    API_TYPE = ''
    API_USERNAME = ''
    API_PASSWORD = ''
    # 指令的开头
    CN_START_WITH = 'wws'
    EN_START_WITH = '/'

    VERSON = '4.0.2' # 文件版本
    REQUEST_TIMEOUT = 10 # 接口请求超时时长(s)
    LOCAL_TIME_ZONE = 8 # 服务器所在时区，8 表示UTC+8
    RETURN_PIC_TYPE = 'file' # file / base64
    # 返回图片的格式，qq_bot平台使用base64，其他平台使用file
    SHOW_DOG_TAG = True # 是否显示用户徽章
    SHOW_CLAN_TAG = True # 是否显示工会徽章
    SHOW_SPECIAL_TAG = True
    SHOW_CUSTOM_TAG = True
    
    BOT_PLATFORM = 'qq_bot' #当前支持平台 qq_bot / discord / qq_group / qq_guild，新增平台请联系作者
    BOT_INFO = {
        'en':f'Wows-Stats-Bot Kokomi-{VERSON}',
        'cn':f'Wows-Stats-Bot Kokomi-{VERSON}',
        'ja':f'Wows-Stats-Bot Kokomi-{VERSON}'
    }
    BOT_AUTHOR = 'Powered by Maoyu'
```

❗❗❗ 需要重点关注的配置是 BOT_PLATFORM 和 RETURN_PIC_TYPE ，请根据实际情况修改，其他默认已配置好

❗❗❗ 需要重点关注的配置是 BOT_PLATFORM 和 RETURN_PIC_TYPE ，请根据实际情况修改，其他默认已配置好

❗❗❗ 需要重点关注的配置是 BOT_PLATFORM 和 RETURN_PIC_TYPE ，请根据实际情况修改，其他默认已配置好

(重要的事情说三遍)


## 第二步-测试插件

### 2.1 运行测试文件

1. 下载 [run_bot.py](https://github.com/SangonomiyaKoko/Kokomi_Bot/blob/main/run_bot.py) 文件（对于该文件的原理，在下文会有详细介绍）

2. 将文件放到与 kokomi_bot **同一文件夹** 下

3. 确认文件的第二行的 ```from 文件夹名.command_select ....``` 中的文件夹名和你的文件夹名一致，如不一致会导致找不到文件

3. 将config配置文件中 `RETURN_PIC_TYPE` 配置为 `file`  

> **`file`表示生成的图片会保存在temp文件夹内，方便查看运行结果，测试完记得修改回你需要的格式**



```
-- run_bot.py
-- Kokomi_Bot/
    -- scripts/
    -- temp/ 
    -- ...
```

4. 使用命令窗口（cmd）运行 run_bot.py

```
python run_bot.py
```


### 2.2 测试结果

1. 如果返回值为 `PIC 图片文件路径`，并且在图片文件夹（kokomi_bot\temp）能看到生成的战绩图片，说明插件正常运行

2. 如果运行结果报错,请打开错误日志查看错误信息,下面一节将列举了常见的报错及解决办法

> **错误日志文件路径：kokomi_bot\log\error**

### 2.3 报错处理
<details>
<summary>常见报错的处理方式</summary>
1.运行提示:
```
ImportError:no module named cv2/pil/httpx
```
- 解决办法：检查 python 环境内是否正确安装了对应的包，如安装过依然报错请检查是否为存在多个 python 版本或nb2使用虚拟环境导致的

2.运行提示：
```
OSError:cannot open resource
```
- 解决办法：系统未安装字体导致，按照 **1.2 安装字体** 操作即可

</details>


### 2.4 请求协助

如遇到无法解决的报错或问题，随时可以联系作者获取帮助（不一定能及时回复），但请提前准备好材料，包括：
- **错误描述**
- **运行报错代码截图**
- **错误日志截图**


## 第三步-对接社交平台接口

Kokomi本身的可拓展性很强，可以轻松兼容不同平台的不同接口

整体逻辑如下
```
获取用户发出的消息(msg)，用户id(user_id)，当前平台(platform)
            ↓
处理收到的消息，按照空格进行切片得到一个list
            ↓
将处理后的消息，用户id和当前平台 作为参数传入 command_select.py 文件中的 select_funtion.main 函数
            ↓
根据函数的返回值类型(msg/img)，向用户发送文字消息或者图片消息
```

### 最小实例

就如我们上面测试时用的文件 run_bot.py

```
import asyncio
from Kokomi_Bot.command_select import select_funtion # 从bot文件中导入接口函数

async def main():
    result = await select_funtion.main(
        msg = ['wws','help'],    # 处理切片后的消息
        user_id = '319720677',   # 用户id
        user_data = {},
        platform = 'qq_bot',     # 当前平台
        platform_id = '123456',
        channel_id = '123456',
        platform_data = {}
    )
    return_type = result['type']        # 返回消息的类型 msg/img
    return_data = result[return_type]   # 返回消息的数据
    print(return_type.upper(),return_data)  # 因为只是测试，所以这里只是简单print出来

asyncio.run(
    main()
)
```
### 实际演示

接下以Discord平台为例，介绍如何搭建一个KokomiBot

1. 注册一个Discord平台的机器人，获取到你的token

2. (可选)查看Discord平台的[文档](https://discordpy.readthedocs.io/en/latest/quickstart.html)

3. 编写主函数，代码如下
```python 
import traceback
import logging
import discord    # dc平台sdk
import os
from command_select import select_funtion
from config import Plugin_Config

file_path = os.path.dirname(__file__)

# dc平台相关代码
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:    # 防止自己响应自己发的消息
        return
    if (
        message.content.startswith('wws') or  # 检查消息是以wws或者/开头的的指令
        message.content.startswith('/')
    ):
        try:
            user_id = str(message.author.id)    # 获取用户id
            gruop_id = None
            group_name = 'None'
            group_data = None
            split_msg = str(message.content).split()  # 将用户发送的消息按照空格切片
            # 这里请注意，国服玩家id可能带空格，需要特殊处理，此处没写
            fun = await select_funtion.main(    # 调用bot的入口函数
                msg=split_msg,
                user_id=user_id,
                user_data={},
                platform=Plugin_Config.BOT_PLATFORM,
                platform_id='123456',
                channel_id='123456',
                platform_data={}
            )
            if fun['type'] == 'msg':    # 如果消息类型为msg，则返回文字消息
                await message.channel.send(fun['msg']) # 发送文字消息
                return
            elif fun['type'] == 'img':    # 如果消息类型为img，则返回图片消息
                await message.channel.send(file=discord.File(fun['img'])) # 发送图片消息
                os.remove(fun['img'])    # 删除图片
                return
        except Exception:
            logging.error(traceback.format_exc())

client.run('这里填你的token')
```
4. 保存并运行，就ok了

### 其他平台

从上述示例中可以看出，想要搭建一个平台所需的接口非常少，你只需要

- 获取用户发送的消息
- 获取用户的id
- 发送文字消息的接口
- 发送图片消息的接口

所以对于其他平台，只需要有这个四个数据或者接口就能兼容Kokomi_Bot

如果你想搭建的平台作者并没有写兼容，可以根据上述描述自己研究！


## 结尾

**很高兴你能看到这里**

**如果您觉得Kokomi还不错的话，还请给项目点个小小的star或者赞助以支持服务器每月的开销，谢谢喵~！**

### 赞助通道

收到的赞助将会用于支持Kokomibot数据服务器的运行

<details>
<summary>爱发电</summary>

![图片，如果打不开可点击跳转查看](https://github.com/SangonomiyaKoko/Kokomibot_docs/tree/main/docs/support/afd.jpg)

</details>


<details>
<summary>微信</summary>

![图片，如果打不开可点击跳转查看](https://github.com/SangonomiyaKoko/Kokomibot_docs/tree/main/docs/support/wx.png)

</details>


<details>
<summary>支付宝</summary>

![图片，如果打不开可点击跳转查看](https://github.com/SangonomiyaKoko/Kokomibot_docs/tree/main/docs/support/zfb.jpg)

</details>

<h4 style="text-align:right;">
    <br>
        作者：Maoyu          
    </br>
    <br>
        时间：2024/5/15 12:36
    </br>
</h4>
