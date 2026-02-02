from typing import Literal, Union, Dict, List, Optional
from typing_extensions import TypedDict


class UserLocalDict(TypedDict):
    theme: str
    language: Literal['cn', 'en']
    show_rating: bool
    filter_valid_data: bool

class UserBindDict(TypedDict):
    '''返回数据格式'''
    region_id: Literal[1, 2, 3, 4, 5]
    account_id: int