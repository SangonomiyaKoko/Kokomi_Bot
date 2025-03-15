# 战舰世界解包工具
[![License](https://img.shields.io/github/license/WoWs-Info/wows_unpack)](./LICENSE)

基于 [EdibleBug/WoWS-GameParams](https://github.com/EdibleBug/WoWS-GameParams) 开发，这个 fork 使用 `wowsunpack.exe` 在解包前先获取 `GameParams.data` 文件，然后再解包，一步到位。

## 可选功能
- 解码游戏语言
- 解包游戏地图
- 解包游戏图标
- 解包游戏资源

## 设置
- 使用 Python 3 运行 `python3 -m venv .env` 创建虚拟环境
- 使用 `pip install -r requirements.txt` 安装全部依赖
- 运行 `python3 run.py`
- 粘贴游戏路径到 `game.path`
- 再次运行 `python3 run.py` 即可解包

## 如何不安装 Python 使用
- 下载最新的版本
- 双击 `run.exe`
- 粘贴游戏路径到 `game.path`
- 再次双击 `run.exe` 即可解包

系统也许会在第一次打开 `run.exe` 的时候进行扫描，扫描仅此一次之后不会。本工具使用 `pyinstaller` 编译打包。如果 `pyinstaller` 在打包的时候注入任何恶意代码， `WoWsUnpack` 不会负任何责任，请自行承担风险。

## 参数
- `--lang`: 解码游戏语言
- `--map`: 解包游戏地图
- `--icon`: 解包游戏图标
- `--res`: 解包游戏资源（会放入各自的文件夹）

如果传入其他参数，程序会返回 -1 并且关闭。在终端里，输入例如 `./run.exe --lang` 来传入参数。双击 `run.exe` 不会传入任何参数。
