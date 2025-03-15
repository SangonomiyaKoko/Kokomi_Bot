from typing import Optional, Literal, Union, Dict, List
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

    API_10001_RootRequired = {'status': 'ok','code': 10001,'message': 'RootRequired','data': None}
    API_10002_AdminOrRootRequired = {'status': 'ok','code': 10002,'message': 'AdminOrRootRequired','data': None}
    API_10003_UserNotBound = {'status': 'ok', 'code': 10003, 'message': 'UserNotBound', 'data': None}
    API_10004_CommandNotFound = {'status': 'ok', 'code': 10004, 'message': 'CommandNotFound', 'data': None}
    API_10005_InvalidArgs = {'status': 'ok', 'code': 10005, 'message': 'InvalidArgs', 'data': None}