import os
import yaml
from typing import Literal

from .path import CONFIG_DIR

class API_Settings:
    def __init__(self, config_data):
        self.API_URL = config_data.get("API_URL", "")
        self.API_TYPE = config_data.get("API_TYPE", "")
        self.API_USERNAME = config_data.get("API_USERNAME", "")
        self.API_PASSWORD = config_data.get("API_PASSWORD", "")
        self.REQUEST_TIMEOUT = config_data.get("REQUEST_TIMEOUT", 30)

    def __repr__(self):
        return (
            f"Config(API_URL={self.API_URL}, "
            f"API_TYPE={self.API_TYPE}, "
            f"API_USERNAME={self.API_USERNAME}, "
            f"API_PASSWORD={self.API_PASSWORD}, "
            f"REQUEST_TIMEOUT={self.REQUEST_TIMEOUT})"
        )

class BOT_Settings:
    def __init__(self, config_data):
        self.LOG_LEVEL: Literal['debug', 'info'] = config_data.get("LOG_LEVEL", "debug")
        self.USE_MOCK: bool = config_data.get("USE_MOCK", False)
        self.RETURN_PIC_TYPE: Literal['png', 'webp'] = config_data.get("RETURN_PIC_TYPE", "png")
        self.SHOW_DOG_TAG: bool = config_data.get("SHOW_DOG_TAG", False)
        self.SHOW_CLAN_TAG: bool = config_data.get("SHOW_CLAN_TAG", False)
        self.SHOW_CUSTOM_TAG: bool = config_data.get("SHOW_CUSTOM_TAG", False)
        self.BOT_INFO: str = config_data.get("BOT_INFO", "No bot information available")

    def __repr__(self):
        return (
            f"Config(LOG_LEVEL={self.LOG_LEVEL}, "
            f"USE_MOCK+{self.USE_MOCK}, "
            f"RETURN_PIC_TYPE={self.RETURN_PIC_TYPE}, "
            f"SHOW_DOG_TAG={self.SHOW_DOG_TAG}, "
            f"SHOW_CLAN_TAG={self.SHOW_CLAN_TAG}, "
            f"SHOW_CUSTOM_TAG={self.SHOW_CUSTOM_TAG}, "
            f"BOT_INFO={self.BOT_INFO})"
        )

def load_config():
    config_path = os.path.join(CONFIG_DIR, 'config.yaml')
    if os.path.exists(config_path) == False:
        raise Exception("Missing config.yaml file")
    with open(config_path, "r") as file:
        config_data = yaml.safe_load(file)
    if "API" not in config_data or 'BOT' not in config_data:
        raise Exception("Missing API and BOT configuration information")
    api_settings = API_Settings(config_data=config_data.get('API'))
    bot_settings = BOT_Settings(config_data=config_data.get('BOT'))
    return api_settings, bot_settings

# 加载配置
api_settings, bot_settings = load_config()