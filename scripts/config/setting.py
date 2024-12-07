from pydantic_settings import BaseSettings
from typing import Literal


class APISettings(BaseSettings):
    # 数据接口指定和默认配置
    API_URL: str
    API_TYPE: str
    API_USERNAME: str
    API_PASSWORD: str
    REQUEST_TIMEOUT: int

    class Config:
        extra = "allow"
        env_file = ".env"
        env_file_encoding = "utf-8"

class BotSettings(BaseSettings):
    # 日志等级
    LOG_LEVEL: Literal['debug','info']
    # 返回图片的格式，请根据实际需求选择
    RETURN_PIC_TYPE: Literal['png','webp']
    # 是否显示徽章
    SHOW_DOG_TAG: bool                                                         
    SHOW_CLAN_TAG: bool
    SHOW_CUSTOM_TAG: bool

    class Config:
        extra = "allow"
        env_file = ".env"
        env_file_encoding = "utf-8"

# 加载配置
api_settings = APISettings()
bot_settings = BotSettings()