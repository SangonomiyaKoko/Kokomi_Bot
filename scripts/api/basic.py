from .base import BaseAPI

class BasicAPI:
    async def get_bot_version():
        "从服务器端获取当前bot的最新版本"
        path = '/r/version/'
        result = BaseAPI.get(path)
        return result