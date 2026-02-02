import tomli
from typing import Literal
from pydantic import BaseModel

from .path import PROJECT_ROOT


class APIConfig(BaseModel):
    host: str
    port: int
    timeout: int
    token: str

class BotConfig(BaseModel):
    platform: str
    log_level: Literal['debug', 'info']
    language: str
    use_mock: bool
    file_type: Literal['png', 'jpg']
    show_dog_tag: bool
    show_clan_tag: bool
    show_costom_tag: bool
    root_users: str

class DefaultConfig(BaseModel):
    language: str
    theme: str
    show_rating: bool
    filter_valid_data: bool

class GlobalConfig(BaseModel):
    api: APIConfig
    bot: BotConfig
    default: DefaultConfig

def init_app_config() -> GlobalConfig:
    path = PROJECT_ROOT / 'config.toml'
    if not path.exists():
        raise FileNotFoundError("The `config.toml` file does not exist.")
    with open(path, "rb") as f:
        data = tomli.load(f)
    config = GlobalConfig(**data)
    return config