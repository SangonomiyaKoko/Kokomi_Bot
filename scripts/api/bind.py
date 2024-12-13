from .base import BaseAPI

class BindAPI:
    async def get_user_bind(platform: dict, user: dict):
        "获取用户的绑定数据"
        path = '/r/user/bind/'
        params = {
            'platform': platform['type'],
            'user_id': user['id']
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