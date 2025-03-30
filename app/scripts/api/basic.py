from .base import BaseAPI
from .mock import Mock
from ..logs import logging
from ..config import bot_settings

# 定义不同地区的常量映射
REGION_LIST = {
    1: 'asia',
    2: 'eu',
    3: 'na',
    4: 'ru',
    5: 'cn'
}

class BasicAPI:
    """
    BasicAPI 类提供了一些用于与平台交互的常见方法，如获取 bot 版本、搜索用户和工会等。
    """
    
    @staticmethod
    async def get_bot_version():
        """
        从服务器端获取当前 bot 的最新版本。

        如果 `bot_settings.USE_MOCK` 为 True，将使用模拟数据，不发起实际网络请求。
        
        返回:
            dict: 包含当前 bot 版本信息的字典。
        """
        path = '/api/v1/robot/version/'
        if bot_settings.USE_MOCK:
            # 使用模拟数据
            result = Mock.read_data('version.json')
            logging.debug('Using MOCK, skip network requests')
        else:
            # 发起真实的网络请求
            result = await BaseAPI.get(path, {})
        return result

    @staticmethod
    async def search_user(region_id: int, name: str):
        """
        根据区域和用户名搜索用户。

        参数:
            region_id (int): 区域 ID，基于 REGION_LIST 映射。
            name (str): 用户名。

        返回:
            dict: 包含搜索结果的字典。
        """
        region = REGION_LIST.get(region_id)
        path = '/api/v1/platform/search/user/'
        params = {
            'region': region,
            'nickname': name,
            'limit': 10,
            'check': 'true'
        }
        result = await BaseAPI.get(path, params)
        return result

    @staticmethod
    async def check_user(region_id: int, account_id: str):
        """
        根据区域和账号 ID 检查用户信息。

        参数:
            region_id (int): 区域 ID，基于 REGION_LIST 映射。
            account_id (str): 用户账号 ID。

        返回:
            dict: 包含用户信息的字典。
        """
        region = REGION_LIST.get(region_id)
        path = '/api/v1/platform/check/user/'
        params = {
            'region': region,
            'account_id': account_id
        }
        result = await BaseAPI.get(path, params)
        return result

    @staticmethod
    async def search_clan(region_id: int, tag: str):
        """
        根据区域和工会标签搜索工会。

        参数:
            region_id (int): 区域 ID，基于 REGION_LIST 映射。
            tag (str): 工会标签。

        返回:
            dict: 包含工会搜索结果的字典。
        """
        region = REGION_LIST.get(region_id)
        path = '/api/v1/platform/search/clan/'
        params = {
            'region': region,
            'tag': tag,
            'limit': 10,
            'check': 'true'
        }
        result = await BaseAPI.get(path, params)
        return result
