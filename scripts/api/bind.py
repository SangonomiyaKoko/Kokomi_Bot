from .base import BaseAPI
from scripts.schemas import KokomiUser

class BindAPI:
    async def get_user_bind(user: KokomiUser):
        "获取用户的绑定数据"
        path = '/r/user/bind/'
        params = {
            'platform': user.platform.name,
            'user_id': user.basic.id
        }
        result = await BaseAPI.get(
            path=path,
            params=params
        )
        return result
    
    async def post_user_bind(user_bind: dict):
        "新增或者修改用户的绑定数据"
        path = '/r/user/bind/'
        result = await BaseAPI.post(
            path=path,
            params={},
            body=user_bind
        )
        return result