from pathlib import Path

# 定义动态项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

# 静态资源路径
ASSETS_DIR = PROJECT_ROOT / "app/assets"
# 代码资源路径
SCRIPTS_DIR = PROJECT_ROOT / "app/scripts"
# 数据资源路径
DATA_DIR = PROJECT_ROOT / "app/data"
# MOCK文件路径
MOCK_DIR = PROJECT_ROOT / "app/mock"
# 配置文件路径
CONFIG_DIR = PROJECT_ROOT / "app"
# 图片输出路径
OUTPUT_DIR = PROJECT_ROOT / "output"
# 日志输出路径
LOG_DIR = PROJECT_ROOT / "log"