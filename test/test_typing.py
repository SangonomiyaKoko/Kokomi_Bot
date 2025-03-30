from typing import Optional, Literal, Union, Dict, List
from typing_extensions import TypedDict


class ResponseDict(TypedDict):
    '''返回数据格式'''
    status: Literal['ok', 'error']
    code: int
    message: str
    data: Optional[Union[Dict, List]]

API_10007_SaveImageFailed = ResponseDict(status='ok', code=10007, message='SaveImageFailed')
