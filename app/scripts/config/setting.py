import os
import yaml
from typing import Literal, Any

from .path import CONFIG_DIR

class APISettings:
    """
    API 配置类，存储 API 相关的配置信息。
    """

    def __init__(self, config_data: dict[str, Any]):
        """
        初始化 API 配置。

        参数:
            config_data (dict): 读取的 API 配置数据字典。
        """
        self.API_URL = config_data.get("API_URL", "")
        self.API_TYPE = config_data.get("API_TYPE", "")
        self.API_USERNAME = config_data.get("API_USERNAME", "")
        self.API_PASSWORD = config_data.get("API_PASSWORD", "")
        self.REQUEST_TIMEOUT = config_data.get("REQUEST_TIMEOUT", 30)

    def __repr__(self) -> str:
        """返回 APISettings 对象的字符串表示。

        返回:
            str: APISettings 对象的详细信息。
        """
        return (
            f"APISettings(api_url={self.API_URL}, "
            f"api_type={self.API_TYPE}, "
            f"api_username={self.API_USERNAME}, "
            f"api_password=******, "  # 避免暴露密码
            f"request_timeout={self.REQUEST_TIMEOUT})"
        )


class BotSettings:
    """
    机器人配置类，存储 Bot 相关的配置信息。
    """

    def __init__(self, config_data: dict[str, Any]):
        """
        初始化 Bot 配置。

        参数:
            config_data (dict): 读取的 BOT 配置数据字典。
        """
        self.PLATFORM: str = config_data.get("PLATFORM", "KokomiBot")
        self.LOG_LEVEL: Literal['debug', 'info'] = config_data.get("LOG_LEVEL", "debug")
        self.USE_MOCK: bool = config_data.get("USE_MOCK", False)
        self.RETURN_PIC_TYPE: Literal['png', 'webp'] = config_data.get("RETURN_PIC_TYPE", "png")
        self.SHOW_DOG_TAG: bool = config_data.get("SHOW_DOG_TAG", False)
        self.SHOW_CLAN_TAG: bool = config_data.get("SHOW_CLAN_TAG", False)
        self.SHOW_CUSTOM_TAG: bool = config_data.get("SHOW_CUSTOM_TAG", False)
        self.BOT_INFO: str = config_data.get("BOT_INFO", "No bot information available")
        self.ROOT_USERS: list = config_data.get("ROOT_USERS", [])
        self.ADMINS_USERS: list = config_data.get("ADMINS_USERS", [])

    def __repr__(self) -> str:
        """返回 BotSettings 对象的字符串表示。

        返回:
            str: BotSettings 对象的详细信息。
        """
        return (
            f"BotSettings(log_level={self.LOG_LEVEL}, "
            f"use_mock={self.USE_MOCK}, "
            f"return_pic_type={self.RETURN_PIC_TYPE}, "
            f"show_dog_tag={self.SHOW_DOG_TAG}, "
            f"show_clan_tag={self.SHOW_CLAN_TAG}, "
            f"show_custom_tag={self.SHOW_CUSTOM_TAG}, "
            f"bot_info={self.BOT_INFO})"
        )


def load_config() -> tuple[APISettings, BotSettings]:
    """加载并解析配置文件，返回 API 和 Bot 的配置信息。

    该函数从指定路径加载配置文件，解析其中的 API 和 Bot 配置数据。
    如果配置文件不存在或格式错误，将抛出相应的异常。

    返回:
        tuple: 包含 APISettings 和 BotSettings 对象的元组。

    异常:
        FileNotFoundError: 如果配置文件缺失。
        ValueError: 如果配置文件格式不正确或缺少必要的配置信息。
    """
    config_path = os.path.join(CONFIG_DIR, 'config.yaml')

    if not os.path.exists(config_path):
        raise FileNotFoundError("Missing config.yaml file")

    with open(config_path, "r", encoding="utf-8") as file:
        config_data = yaml.safe_load(file) or {}

    if "API" not in config_data or "BOT" not in config_data:
        raise ValueError("Missing API and BOT configuration information")

    api_settings = APISettings(config_data=config_data.get('API', {}))
    bot_settings = BotSettings(config_data=config_data.get('BOT', {}))

    return api_settings, bot_settings



