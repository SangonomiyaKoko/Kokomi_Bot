# 具体的指令处理函数，必须async修饰的异步函数
from typing import Callable, Dict, Tuple, Optional, Any, Union, Awaitable

from ...resources import (
    test, bind, overall, clear, admin, theme
)
from ...schemas import KokomiUser

from .parsers import (
    get_region_id_from_aid,
    get_region_id_from_input,
    extract_mention_id,
    search_user,
    check_user
)

async def handler_test(
    user: KokomiUser, 
    raw_args: str
) -> Tuple[Optional[Callable[[Any], dict]], Optional[Dict[str, Any]]]:
    """测试功能
    
    包含指令：
        - /test [test_msg]

    返回值：
        (callback_func, extra_kwargs) or 
        (None, None) or 
        (None, dixt)
    """
    if raw_args == '' or raw_args == None:
        test_msg = '123456789'
    else:
        test_msg = raw_args
    return test.main, {'test_msg': test_msg}

async def handler_admin(
    user: KokomiUser, 
    raw_args: str
) -> Tuple[Optional[Callable[[Any], dict]], Optional[Dict[str, Any]]]:
    """测试功能
    
    包含指令：
        - /admin

    返回值：
        (callback_func, extra_kwargs) or 
        (None, None) or 
        (None, dixt)
    """
    
    return admin.main, {}

async def handler_cls(
    user: KokomiUser, 
    raw_args: str
) -> Tuple[Optional[Callable[[Any], dict]], Optional[Dict[str, Any]]]:
    """绑定指令
    
    包含指令：
        - /cls

    返回值：
        (callback_func, extra_kwargs) or 
        (None, None) or 
        (None, dixt)
    """
    return clear.main, {}

async def handler_bind(
    user: KokomiUser, 
    raw_args: str
) -> Tuple[Optional[Callable[[Any], dict]], Optional[Dict[str, Any]]]:
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
        'account_id': None
    }
    if raw_args == '':
        return None, None
    if raw_args.isdigit():
        # 通过UID绑定
        account_id = int(raw_args)
        region_id = get_region_id_from_aid(account_id)
        if not region_id:
            return None, None
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
    return bind.post_bind, params

async def handler_lang(
    user: KokomiUser, 
    raw_args: str
) -> tuple[Optional[Callable[..., Awaitable[Dict[str, Any]]]], Union[Dict[str, Any], None]]:
    """绑定指令
    
    包含指令：
        - /lang <cn/en/ja>

    返回值：
        (callback_func, extra_kwargs) or 
        (None, None) or 
        (None, dict)
    """
    if raw_args == '':
        return None, None
    if raw_args not in ['cn', 'en', 'ja']:
        return None, None
    params = {
        'language': raw_args
    }
    return bind.update_language, params

async def handler_content(
    user: KokomiUser, 
    raw_args: str
) -> tuple[Optional[Callable[..., Awaitable[Dict[str, Any]]]], Union[Dict[str, Any], None]]:
    """绑定指令
    
    包含指令：
        - /mode <dark/light>

    返回值：
        (callback_func, extra_kwargs) or 
        (None, None) or 
        (None, dict)
    """
    if raw_args == '':
        return None, None
    if raw_args not in ['dark', 'light']:
        return None, None
    params = {
        'content': raw_args
    }
    return bind.update_content, params

async def handler_theme(
    user: KokomiUser, 
    raw_args: str
) -> tuple[Optional[Callable[..., Awaitable[Dict[str, Any]]]], Union[Dict[str, Any], None]]:
    """绑定指令
    
    包含指令：
        - /theme <default/mavuika/furina>

    返回值：
        (callback_func, extra_kwargs) or 
        (None, None) or 
        (None, dict)
    """
    if raw_args == '':
        return theme.main, {}
    if raw_args not in ['default', 'mavuika', 'furina']:
        return None, None
    params = {
        'theme': raw_args
    }
    return bind.update_theme, params

async def handler_algo(
    user: KokomiUser, 
    raw_args: str
) -> tuple[Optional[Callable[..., Awaitable[Dict[str, Any]]]], Union[Dict[str, Any], None]]:
    """绑定指令
    
    包含指令：
        - /algo <default/none>

    返回值：
        (callback_func, extra_kwargs) or 
        (None, None) or 
        (None, dict)
    """
    if raw_args == '':
        return None, None
    algo_dict = {
        'default': 'pr',
        'none': ''
    }
    if raw_args not in algo_dict:
        return None, None
    params = {
        'algorithm': algo_dict.get(raw_args)
    }
    return bind.update_algorithm, params

async def handler_basic(
    user: KokomiUser, 
    raw_args: str
) -> tuple[Optional[Callable[..., Awaitable[Dict[str, Any]]]], Union[Dict[str, Any], None]]:
    """绑定指令
    
    包含指令：
        - /basic [@/IGN/AID]

    返回值：
        (callback_func, extra_kwargs) or 
        (None, None) or 
        (None, dict)
    """
    if raw_args == '':
        return overall.main, None
    params = {
        'region_id': None,
        'account_id': None
    }
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
        params['account_id'] = account_id
        params['region_id'] = region_id
        user.set_user_bind(params)
        return overall.main, None
    else:
        parts = raw_args.split(maxsplit=1)
        if len(parts) == 1:
            # 通过解析@字符串的方式
            match = extract_mention_id(parts[0])
            if match:
                user.basic.id = match
            else:
                return None, None
        else:
            # 通过 IGN 方式
            region_id = get_region_id_from_input(parts[0])
            if not region_id:
                return None, None
            search_result = await search_user(region_id=region_id, nickname=parts[1])
            if search_result['code'] != 1000:
                return None, search_result
            params['account_id'] = search_result['data'][0]['account_id']
            params['region_id'] = search_result['data'][0]['region_id']
            user.set_user_bind(params)
        return overall.main, None
    