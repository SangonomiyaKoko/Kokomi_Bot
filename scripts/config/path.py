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