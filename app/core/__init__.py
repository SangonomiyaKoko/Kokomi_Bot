from .context import AppContext
from .version import read_version
from .config import init_app_config
from .exceptions import (
    AppInitError, I18nRegisterError
)
from .path import ASSETS_DIR, OUTPUT_DIR, STORAGE_DIR

Config = init_app_config()

__all__ = [
    'AppContext',
    'Config',
    'read_version',
    'init_app_config',
    'ASSETS_DIR',
    'OUTPUT_DIR',
    'STORAGE_DIR'
]