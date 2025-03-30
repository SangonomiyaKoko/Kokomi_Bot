from .base import BaseAPI
from .mock import Mock
from ..logs import logging
from ..config import bot_settings
from ..schemas import KokomiUser

class BindAPI:
    """
    BindAPI 类提供了与用户绑定数据相关的接口方法，如获取绑定数据和新增或修改绑定数据。
    """

    @staticmethod
    async def get_user_bind(user: KokomiUser):
        """
        获取用户的绑定数据。

        根据给定的用户对象，发送请求获取该用户的绑定信息。
        
        参数:
            user (KokomiUser): 包含用户信息的对象，需包含平台名和用户ID。
        
        返回:
            dict: 包含用户绑定数据的字典。

        如果 `bot_settings.USE_MOCK` 为 True，将使用模拟数据返回结果。
        """
        path = '/api/v1/robot/user/bind/'
        params = {
            'platform': user.platform.name,  # 用户平台名称
            'user_id': user.basic.id  # 用户ID
        }
        if bot_settings.USE_MOCK:
            # 使用模拟数据
            result = Mock.read_data('bind.json')
            logging.debug('Using MOCK, skip network requests')
        else:
            # 发起真实的网络请求获取绑定数据
            result = await BaseAPI.get(
                path=path,
                params=params
            )
        return result

    @staticmethod
    async def post_user_bind(user_bind: dict):
        """
        新增或修改用户的绑定数据。

        通过 POST 请求将用户的绑定数据提交到服务器，以进行新增或修改。
        
        参数:
            user_bind (dict): 包含用户绑定信息的字典。
        
        返回:
            dict: 服务器返回的处理结果。

        请求体 `user_bind` 应该包含所需的绑定信息，如平台名、用户ID及绑定数据。
        """
        path = '/api/v1/robot/user/bind/'
        # 发起 POST 请求提交用户绑定数据
        result = await BaseAPI.post(
            path=path,
            params={},
            body=user_bind
        )
        return result
