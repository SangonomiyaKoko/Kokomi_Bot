# 具体的指令处理函数，必须async修饰的异步函数

from ...resources import (
    test, bind
)

from .parsers import (
    get_region_id_from_aid,
    get_region_id_from_input,
    search_user,
    check_user
)

async def handle_test(raw_args: str) -> tuple:
    """测试功能
    
    包含指令：
        - /test [test_msg]

    返回值：
        (callback_func, extra_kwargs) or 
        (None, None) or 
        (None, dixt)
    """
    if test_msg == '' or test_msg == None:
        test_msg = '123456789'
    else:
        test_msg = raw_args
    return test.main, {'test_msg': test_msg}

async def handle_bind(raw_args: str):
    """绑定指令
    
    包含指令：
        - /link <IGN/AID>

    返回值：
        (callback_func, extra_kwargs) or 
        (None, None) or 
        (None, dixt)
    """
    params = {
        'region_id': None,
        'account_id': None,
        'nickname': None
    }
    if raw_args == '':
        return None, None
    if raw_args.isdigit():
        # 通过UID绑定
        account_id = int(raw_args)
        region_id = get_region_id_from_aid(account_id)
        if not region_id:
            return None, None
        check_result = await check_user(region_id=region_id,account_id=account_id)
        if check_result['code'] == 1001:
            return None, None
        if check_result['code'] != 1000:
            return None, check_result
        params['nickname'] = check_result['data']['name']
        params['account_id'] = account_id
        params['region_id'] = region_id
    else:
        # 通过 IGN方式
        parts = raw_args.split(maxsplit=1)
        if len(parts) <= 1:
            return None, None
        region_id = get_region_id_from_input(parts[0])
        if not region_id:
            return None, None
        search_result = await search_user(region_id=region_id, nickname=parts[1])
        if search_result['code'] != 1000:
            return None, search_result
        params['account_id'] = search_result['data'][0]['account_id']
        params['region_id'] = search_result['data'][0]['region_id']
        params['nickname'] = search_result['data'][0]['name']
    return bind.post_bind, params
