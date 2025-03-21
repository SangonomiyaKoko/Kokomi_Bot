from .base import BaseAPI
from .mock import Mock
from ..logs import logging
from ..config import bot_settings

REGION_LIST = {
    1: 'asia',
    2: 'eu',
    3: 'na',
    4: 'ru',
    5: 'cn'
}

class BasicAPI:
    async def get_bot_version():
        "从服务器端获取当前bot的最新版本"
        path = '/api/v1/robot/version/'
        if bot_settings.USE_MOCK:
            result = Mock.read_data('version.json')
            logging.debug('Using MOCK, skip network requests')
        else:
            result = await BaseAPI.get(path, {})
        return result
    
    async def search_user(region_id: int, name: str):
        "获取用户名称搜索结果"
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
    
    async def check_user(region_id: int, account_id: str):
        "获取用户名称搜索结果"
        region = REGION_LIST.get(region_id)
        path = '/api/v1/platform/check/user/'
        params = {
            'region': region,
            'account_id': account_id
        }
        result = await BaseAPI.get(path, params)
        return result
    
    async def search_clan(region_id: int, tag: str):
        "获取工会名称搜索结果"
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
