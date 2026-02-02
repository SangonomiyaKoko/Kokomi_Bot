import uuid
from typing import Optional, Literal, Union, Any, Dict, List
from typing_extensions import TypedDict


class ResponseDict(TypedDict):
    '''返回数据格式'''
    status: Literal['ok', 'error']
    code: int
    message: str
    data: Optional[Union[Dict, List]]

class JSONResponse:
    '''接口返回值
    
    1000      -> 成功
    2000-2999 -> [INFO]  业务层消息
    3000-3999 -> [INFO]  外部接口消息
    4000-4999 -> [ERROR] 业务层异常
    5000-5999 -> [ERROR] 外部接口异常
    6000-6999 -> 为前端程序预留
    '''
    API_1000_Success = {'status': 'ok','code': 1000,'message': 'Success','data': None}

    # INFO

    # 
    API_6001_TestMessage = {'status': 'ok','code': 6001,'message': 'TestMessage','data' : None}


    @staticmethod
    def get_success_response(
        data: Optional[Any] = None
    ) -> ResponseDict:
        "成功的返回值"
        return {
            'status': 'ok',
            'code': 1000,
            'message': 'Success',
            'data': data
        }
    
    @staticmethod
    def get_error_response(
        code: str,
        message: str,
        error_id: str = None
    ) -> ResponseDict:
        "失败的返回值"
        if error_id is None:
            error_id = str(uuid.uuid4())
        return {
            'status': 'error',
            'code': code,
            'message': message,
            'data': {
                'error_id': error_id,
                'platform': 'BOT'
            }
        }