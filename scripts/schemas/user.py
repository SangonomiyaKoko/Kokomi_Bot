from typing import Literal, Union, Dict, List
from typing_extensions import TypedDict


class UserInfoDict(TypedDict):
    id: Union[str, int]
    cid: Union[str, None]
    name: Union[str, None]
    avatar: Union[str, None]

class PlatformDict(TypedDict):
    type: str
    id: Union[str, int]
    cid: Union[str, int, None]
    name: Union[str, None]
    avatar: Union[str, None]
    users: Union[List[Dict], None]

class UserBindDict(TypedDict):
    '''返回数据格式'''
    region_id: Literal[1, 2, 3, 4, 5]
    account_id: int

class UserLocalDict(TypedDict):
    language: Literal['cn', 'en', 'ja']
    algorithm: Literal['pr', None]
    background: str
    content: Literal['dark', 'light']
    theme: str