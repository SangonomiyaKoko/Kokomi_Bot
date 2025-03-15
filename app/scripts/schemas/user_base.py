from .type_dict import UserLocalDict, UserBindDict

class Platform:
    "平台类"
    def __init__(self, name: str, id: str, cid: str):
        self.name = name
        self.id = id    # 平台id或者服务器id
        self.cid = cid    # 频道id，一个服务器可能有多个频道
        self.sname = None
        self.cname = None
        self.avatar = None
        self.users = None
    
    def set_platform_info(self, sname: str, cname: str, avatar: str, users: dict | list):
        "写入平台详细数据"
        self.sname = sname
        self.cname = cname
        self.avatar = avatar
        self.users = users

class UserBasic:
    "用户基础信息类"
    def __init__(self, id: str, cid: str):
        self.id = id    # 查询用户id
        self.cid = cid    # 原始用户id，处理@查询请求中，可能需要的对原始用户id的溯源
        self.name = None
        self.avatar = None
        self.level = 2
    
    def set_user_info(self, name: str, avatar: str):
        "写入用户详细数据"
        self.name = name
        self.avatar = avatar

    def set_user_level(self, level: int):
        "写入用户的权限等级"
        self.level = level

class UserBind:
    "用户绑定信息类"
    def __init__(self):
        self.region_id = None
        self.account_id = None

    def set_user_bind(self, user_bind: UserBindDict):
        self.region_id = user_bind['region_id']
        self.account_id = user_bind['account_id']
    
class UserLocal:
    "用户本地信息类"
    def __init__(self, platform: Platform):
        "先按默认值初始化类"
        self.language = self.__get_default_language(platform)
        self.algorithm = self.__get_default_algorithm()
        self.background = self.__get_default_picture('background')
        self.content = self.__get_default_picture('content')
        self.theme = self.__get_default_picture('theme')

    @staticmethod
    def __get_default_algorithm() -> str:
        "获取默认评分算法"
        return 'pr'
    
    @staticmethod
    def __get_default_language(platform: Platform) -> str:
        "获取平台默认的语言"
        if platform.name in ['qq_bot', 'qq_group', 'qq_guild']:
            return 'cn'
        else:
            return 'en'

    @staticmethod
    def __get_default_picture(key: str) -> str:
        "获取默认图片格式"
        defaults = {
            'background': '#F8F9FB',
            'content': 'light',
            'theme': 'default'
        }
        return defaults.get(key)

    def set_user_local(self, user_local: UserLocalDict):
        "使用用户数据覆写属性值"
        self.language = user_local['language']
        self.algorithm = user_local['algorithm']
        self.background = user_local['background']
        self.content = user_local['content']
        self.theme = user_local['theme']

class KokomiUser:
    "继承自Platform类和UserBasic类"
    def __init__(self, platform: Platform, user_basic: UserBasic):
        "初始化用户信息"
        self.platform = platform
        self.basic = user_basic
        self.bind = UserBind()
        self.local = UserLocal(platform)

    def set_user_level(self, user_level: int):
        "更新用户的等级权限"
        self.basic.set_user_level(user_level)

    def set_user_bind(self, user_bind: UserBindDict):
        "更新用户的bind数据"
        self.bind.set_user_bind(user_bind)
    
    def set_user_local(self, user_local: UserLocalDict):
        "更新用户的local数据"
        self.local.set_user_local(user_local)