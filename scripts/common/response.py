from typing import Optional, Literal, Union, Any, Dict, List
from typing_extensions import TypedDict


class ResponseDict(TypedDict):
    '''返回数据格式'''
    status: Literal['ok', 'error']
    code: int
    message: str
    data: Optional[Union[Dict, List]]


class JSONResponse:
    API_9001_UserNotLinked = {'status': 'ok', 'code': 9001, 'message': 'UserNotLinked', 'data': None}