from .base import BaseAPI

class BindAPI:
    async def get_user_bind(platform: str, user: str):
        "获取用户的绑定数据"
        path = '/r/bind/'
        params = {
            'platform': platform,
            'user': user
        }
        result = await BaseAPI.get(
            path=path,
            params=params
        )
        return result
    
    async def post_user_bind(user_bind: dict):
        "新增用户的绑定数据"
        path = '/r/bind/'
        result = await BaseAPI.post(
            path=path,
            body=user_bind
        )
        return result
    
    async def put_user_bind(user_bind: dict):
        "修改用户的绑定数据"
        path = '/r/bind/'
        result = await BaseAPI.put(
            path=path,
            body=user_bind
        )
        return result