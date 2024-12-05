from pathlib import Path

# 日志等级
LOG_LEVEL = 'debug'
# 定义动态项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent
# 静态资源路径
ASSETS_DIR = PROJECT_ROOT / "assets"
# 代码资源路径
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
# 数据资源路径
ASSETS_DIR = PROJECT_ROOT / "data"
# 图片输出路径
OUTPUT_DIR = PROJECT_ROOT / "output"
# 日志输出路径
LOG_DIR = PROJECT_ROOT / "log"

class APIConfig:
    # 数据接口指定和默认配置
    API_URL = 'http://43.134.96.105:8000'
    API_TYPE = 'Bearer'
    API_USERNAME = 'user'
    API_PASSWORD = '123456'
    REQUEST_TIMEOUT = 10

class BotConfig:
    # 返回图片的格式，请根据实际需求选择
    RETURN_PIC_TYPE = 'file'
    # 是否显示徽章
    SHOW_DOG_TAG = True                                                                                              
    SHOW_CLAN_TAG = True
    SHOW_CUSTOM_TAG = True