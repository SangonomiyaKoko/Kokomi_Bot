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

    API_10001_RootRequired = ResponseDict(status='ok', code=10001, message='RootRequired')
    API_10002_AdminOrRootRequired = ResponseDict(status='ok', code=10002, message='AdminOrRootRequired')
    API_10003_UserNotBound = ResponseDict(status='ok', code=10003, message='UserNotBound')
    API_10004_CommandNotFound = ResponseDict(status='ok', code=10004, message='CommandNotFound')
    API_10005_InvalidArgs = ResponseDict(status='ok', code=10005, message='InvalidArgs')
    API_10006_ClearCacheSuccess = ResponseDict(status='ok', code=10006, message='ClearCacheSuccess')
    API_10007_SaveImageFailed = ResponseDict(status='ok', code=10007, message='SaveImageFailed')
    API_10008_ImageResourceMissing = ResponseDict(status='ok', code=10008, message='ImageResourceMissing')
    API_10009_ImageTooLarge = ResponseDict(status='ok', code=10009, message='ImageTooLarge')
    API_10010_AliasAddedSuccessfully = ResponseDict(status='ok', code=10010, message='AliasAddedSuccessfully')
    API_10011_AliasDeletedSuccessfully = ResponseDict(status='ok', code=10011, message='AliasDeletedSuccessfully')
    API_10012_AliasNotSet = ResponseDict(status='ok', code=10012, message='AliasNotSet')
    API_10013_AliasCannotBeNumericOnly = ResponseDict(status='ok', code=10013, message='AliasCannotBeNumericOnly')
    API_10014_AliasTooLong = ResponseDict(status='error', code=10014, message='AliasTooLong')





