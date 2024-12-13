
from scripts.logs import ExceptionLogger
from scripts.api import BasicAPI, BindAPI
from scripts.common import JSONResponse, UserLocal
from scripts.schemas import (
    PlatformDict, UserInfoDict, UserBindDict, UserLocalDict
)


@ExceptionLogger.handle_program_exception_async
async def post_bind(
    platform: PlatformDict,
    user_info: UserInfoDict,
    user_bind: UserBindDict,
    user_local: UserLocalDict,
    region_id: int,
    nickname: str
) -> dict:
    result = await BasicAPI.search_user(region_id, nickname)
    if result['code'] != 1000:
        return result
    if len(result['data']) != 1:
        return JSONResponse.API_9003_NameNotFound
    data = {
        'platform': platform['type'],
        'user_id': user_info['id'],
        'region_id': result['data'][0]['region_id'],
        'account_id': result['data'][0]['account_id']
    }
    result = await BindAPI.post_user_bind(data)
    if result['code'] != 1000:
        return result
    return JSONResponse.API_9005_LinkSuccess

@ExceptionLogger.handle_program_exception_async
async def update_language(
    platform: PlatformDict,
    user_info: UserInfoDict,
    user_bind: UserBindDict,
    user_local: UserLocalDict,
    language: str
) -> dict:
    result = UserLocal.update_language(platform,user_info,language)
    if result['code'] != 1000:
        return result
    else:
        return JSONResponse.API_9006_ChangeSuccess

@ExceptionLogger.handle_program_exception_async
async def update_algorithm(
    platform: PlatformDict,
    user_info: UserInfoDict,
    user_bind: UserBindDict,
    user_local: UserLocalDict,
    algorithm: str
) -> dict:
    result = UserLocal.update_algorithm(platform,user_info,algorithm)
    if result['code'] != 1000:
        return result
    else:
        return JSONResponse.API_9006_ChangeSuccess