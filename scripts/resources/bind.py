
from scripts.logs import ExceptionLogger
from scripts.api import BasicAPI, BindAPI
from scripts.common import JSONResponse, UserLocalDB
from scripts.schemas import KokomiUser


@ExceptionLogger.handle_program_exception_async
async def post_bind(
    user: KokomiUser,
    region_id: int,
    nickname: str
) -> dict:
    result = await BasicAPI.search_user(region_id, nickname)
    if result['code'] != 1000:
        return result
    if len(result['data']) != 1:
        return JSONResponse.API_9003_NameNotFound
    data = {
        'platform': user.platform.name,
        'user_id': user.basic.id,
        'region_id': result['data'][0]['region_id'],
        'account_id': result['data'][0]['account_id']
    }
    result = await BindAPI.post_user_bind(data)
    if result['code'] != 1000:
        return result
    return JSONResponse.API_9005_LinkSuccess

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