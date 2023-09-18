# Kokomi_bot_plugin 部署教程 （V 3.3.0） 

## 前言

1. Kokomi 本质是一个**插件**，并不是一个完整的bot，需要依赖 `NoneBot2` 或者相关 `频道SDK` 实现功能

2. 默认采用作者的公开数据接口，如果您有一定的编程经验且对此有兴趣，也可以找作者获取数据接口&数据库的搭建方法

3. 如果你还没有安装 `NoneBot2` ，请自行搜索教程，相关链接。

    - [Nonebot2官网](https://v2.nonebot.dev/)
    - [go-cqhttp官网](https://docs.go-cqhttp.org/)

4. 以下教程以 `NoneBot2` 如何配置并加载kokomi插件为例，适配器为 `onebot.v11`。

5. 如果您对python虚拟环境不了解，推荐在nb2创建bot时选择不使用虚拟环境

6. **获取token以及开发者交流群（462447502）**

## 第一步-配置环境

> 开发环境的 python 版本 3.8.10

### 1.1 安装需要使用的python模块

插件会使用到的模块有: `pillow` (PIL) , `opencv-python` (cv2) , `httpx`

**注意： `pillow` 的版本不能大于等于 `10.0.0` 版本， `9.1.0` ~ `9.5.0` 版本均可**

使用以下的命令可以查看当前 python 环境内已安装的包。
```
pip list
```
对于没有进行过python开发的小白来说，python是没有自带这几个模块

如果上述需要模块不存在，**在下面进行测试时会自动安装**，您也可以通过手动安装

<details>
<summary>手动安装python包</summary>

特别注意：如果使用了虚拟环境，请在虚拟环境内安装相关模块，需要先进入虚拟环境再安装python包(所以小白不建议使用虚拟环境)

```
# 安装指定模块
pip install 模块名

# 安装指定模块的指定版本
pip install 模块名==指定版本号

# 卸载指定模块
pip uninstall 模块名

# 示例
pip install pillow==9.5.0
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

### 1.3 配置文件

> token配置文件路径：kokomi_bot_plugin\token.json
> config配置文件路径：kokomi_bot_plugin\scripts\config.py

1. 将token配置文件中 `kokomi_basic_api` 的 `token` 配置为作者给你的token（没有token请看 [前言](#前言) ）

2. 将config配置文件中 `PIC_TYPE` 配置为 `file` (测试用)，**测试完记得改回 `base64`**

3. 其他配置项保持默认

## 第二步-测试插件

### 2.1 运行测试文件

1. 下载 [testbot.py](https://github.com/SangonomiyaKoko/nonebot_plugin_kokomi/blob/main/testbot.py) 文件

2. 将文件放到与 nonebot_plugin_kokomi **同一文件夹**下

3. 将 nonebot_plugin_kokomi 内 `__init__.py` 文件拿出来和 `testbot.py` 放一起，文件结构如下所示

> 这一步是因为部分用户加载__init__文件会出现ImportError报错的问题

```
-- testbot.py
-- __init__.py
-- nonebot_plugin_kokomi/
    -- json/
    -- scripts/
    -- temp/ 
    -- data_source.py   
    -- command_select.py
```

4. 使用命令窗口（cmd）运行 testbot.py

```
python testbot.py
```

运行后会默认检查环境并安装相应模块

### 2.2 测试结果

1. 如果返回值为 `ok 发送图片`，并且在图片文件夹（kokomi_bot_plugin\temp）能看到生成的图片，说明插件正常运行
    - 将上一步移出来的 `__init__.py` 文件放回去，与 `data_source.py` 位于同一文件夹下
    - 将 **config文件** 中 `PIC_TYPE` 项改为 `base64` (别忘了)
    - 即可直接跳到 [第三步 - 加载插件](#第三步-加载插件)

2. 如果运行结果报错,请打开错误日志查看错误信息,下面一节将列举了常见的报错及解决办法

> **错误日志文件路径：kokomi_bot_plugin\scripts\log\error.log**

### 2.3 报错处理
<details>
<summary>常见报错的处理方式</summary>
1.程序运行返回值为

```json
{
    "status": "info", 
    "message": "当前token不可用，请联系作者申请接口token"
}
```

- 解决办法：检查config文件是否正确配置token

2.程序运行返回值为

```json
{
    "status": "info", 
    "message": "数据接口请求失败\\网络请求超时,请稍后重试"
}
```
- 解决办法：检查网络是否正常或者是否使用了VPN软件


3.运行提示:
```
ImportError:no module named cv2/pil/httpx
```
- 解决办法：检查 python 环境内是否正确安装了对应的包，如安装过依然报错请检查是否为存在多个 python 版本或nb2使用虚拟环境导致的

4.运行提示：
```
OSError:cannot open resource
```
- 解决办法：系统未安装字体导致，按照 **1.2 安装字体** 操作即可

5.运行提示 `程序内部错误` ,查看错误日志提示为：
```
AttributeError: module font has no attribute getsize
```
- 解决办法：`pillow` 版本不支持，请更改为 `9.1.0` ~ `9.5.0` 版本
</details>


### 2.4 请求协助

如遇到无法解决的报错或问题，随时可以联系作者获取帮助（不一定能及时回复），但请提前准备好材料，包括：
- **错误描述**
- **运行报错代码截图**
- **错误日志截图**

> 没有错误截图我怎么debug

## 第三步-加载插件

由于每个人使用及启动 `NoneBot2` 的版本或者方式有所不同，具体请参考 `NoneBot2` 官网关于如何加载插件的 [文章](https://nonebot.dev/docs/tutorial/create-plugin)，里面有非常详细且易懂的教程，在此就不过多赘述。

当你做完这一步，Kokomi也就成功运行了，快去群聊里面狠狠的wws me吧！

> 此外，`NoneBot2` 还有非常多的官方以及第三方现成的插件，可以去官网的 [商店](https://nonebot.dev/store) 下载到这些丰富有趣的插件，来丰富你机器人的功能！

## 第四步-自定义图片界面（选读）

如果你想更改图片的相关界面，请阅读以下 [文章](https://github.com/SangonomiyaKoko/Kokomibot_docs/blob/main/docs/picture.md)

## 结尾

**很高兴你能看到这里**

**如果您觉得Kokomi还不错的话，还请给项目点个小小的star 或者 [投喂](http://www.wows-coral.com/article/Introduction.html#%E8%B5%9E%E5%8A%A9%E9%80%9A%E9%81%93) 以支持服务器每月的开销，谢谢喵~！**

<h4 class='text'>
    <br>
        作者：Maoyu          
    </br>
    <br>
        时间：2023/9/18 12:36
    </br>
</h4>
<style>
    .text {
        text-align: right;
    }
</style>

</h4>



