from .base import BaseAPI
from .mock import Mock
from ..logs import logging
from ..config import bot_settings
from ..schemas import KokomiUser

class BindAPI:
    async def get_user_bind(user: KokomiUser):
        "获取用户的绑定数据"
        path = '/api/v1/robot/user/bind/'
        params = {
            'platform': user.platform.name,
            'user_id': user.basic.id
        }
        if bot_settings.USE_MOCK:
            result = Mock.read_data('bind.json')
            logging.debug('Using MOCK, skip network requests')
        else:
            result = await BaseAPI.get(
                path=path,
                params=params
            )
        return result
    
    async def post_user_bind(user_bind: dict):
        "新增或者修改用户的绑定数据"
        path = '/api/v1/robot/user/bind/'
        result = await BaseAPI.post(
            path=path,
            params={},
            body=user_bind
        )
        return result