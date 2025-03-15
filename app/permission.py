from .scripts.config import bot_settings

def get_user_level(user_id: str):
    """ 获取用户的权限，在yaml里配置root或者admins用户 """
    if user_id in bot_settings.ROOT_USERS:
        return 0
    elif user_id in bot_settings.ADMINS_USERS:
        return 1
    else:
        return 2