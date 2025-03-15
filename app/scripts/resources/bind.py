
from ..logs import ExceptionLogger
from ..api import BasicAPI, BindAPI
from ..schemas import JSONResponse
from ..db import UserLocalDB
from ..schemas import KokomiUser


@ExceptionLogger.handle_program_exception_async
async def post_bind(
    user: KokomiUser,
    region_id: int,
    account_id: int,
    nickname: str
) -> dict:
    data = {
        'platform': user.platform.name,
        'user_id': user.basic.id,
        'region_id': region_id,
        'account_id': account_id
    }
    result = await BindAPI.post_user_bind(data)
    if result['code'] != 1000:
        return result
    result = JSONResponse.API_9005_LinkSuccess
    result['data'] = {
        'region_id': region_id,
        'account_id': account_id,
        'nickname': nickname
    }
    return result

@ExceptionLogger.handle_program_exception_async
async def update_language(
    user: KokomiUser,
    language: str
) -> dict:
    result = UserLocalDB.update_language(user,language)
    if result['code'] != 1000:
        return result
    else:
        return JSONResponse.API_9006_ChangeSuccess

@ExceptionLogger.handle_program_exception_async
async def update_algorithm(
    user: KokomiUser,
    algorithm: str
) -> dict:
    result = UserLocalDB.update_algorithm(user,algorithm)
    if result['code'] != 1000:
        return result
    else:
        return JSONResponse.API_9006_ChangeSuccess