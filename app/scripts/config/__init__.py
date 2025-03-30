from .setting import load_config
from .path import (
    PROJECT_ROOT, ASSETS_DIR,
    OUTPUT_DIR, SCRIPTS_DIR,
    LOG_DIR, DATA_DIR, MOCK_DIR,
    CONFIG_DIR
)
# 加载配置
api_settings, bot_settings = load_config()
__all__ = [
    'api_settings',
    'bot_settings',
    'PROJECT_ROOT',
    'ASSETS_DIR',
    'OUTPUT_DIR',
    'SCRIPTS_DIR',
    'LOG_DIR',
    'DATA_DIR',
    'MOCK_DIR',
    'CONFIG_DIR'
]