from .base import BaseAPI



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
        path = '/r/version/'
        result = BaseAPI.get(path)
        return result
    
    async def search_user(region_id: int, name: str):
        "获取用户名称搜索结果"
        region = REGION_LIST.get(region_id)
        path = '/p/search/user/'
        params = {
            'region': region,
            'nickname': name,
            'limit': 10,
            'check': 'true'
        }
        result = BaseAPI.get(path, params)
        return result
    
    async def search_clan(region_id: int, tag: str):
        "获取工会名称搜索结果"
        region = REGION_LIST.get(region_id)
        path = '/p/search/clan/'
        params = {
            'region': region,
            'tag': tag,
            'limit': 10,
            'check': 'true'
        }
        result = BaseAPI.get(path, params)
        return result
