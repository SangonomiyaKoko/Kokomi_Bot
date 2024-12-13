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
    API_9002_FuncNotFound = {'status': 'ok', 'code': 9002, 'message': 'FuncNotFound', 'data': None}
    API_9003_NameNotFound = {'status': 'ok', 'code': 9003, 'message': 'NameNotFound', 'data': None}
    API_9004_TagNotFound = {'status': 'ok', 'code': 9004, 'message': 'TagNotFound', 'data': None}
    API_9005_LinkSuccess = {'status': 'ok', 'code': 9005, 'message': 'LinkSuccess', 'data': None}
    API_9006_ChangeSuccess = {'status': 'ok', 'code': 9006, 'message': 'ChangeSuccess', 'data': None}
    API_9007_InvaildParams = {'status': 'ok', 'code': 9007, 'message': 'InvaildParams', 'data': None}