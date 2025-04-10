# 具体的指令处理函数，必须async修饰的异步函数
from typing import Callable, Dict, Tuple, Optional, Any, Union, Awaitable

from ...resources import (
    test, bind, overall, clear, admin, theme, alias, help
)
from ...schemas import KokomiUser, JSONResponse

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
        (None, dict)
    """
    if raw_args == '' or raw_args == None:
        test_msg = '123456789'
    else:
        test_msg = raw_args
    return test.main, {'test_msg': test_msg}

async def handler_help(
    user: KokomiUser, 
    raw_args: str
) -> Tuple[Optional[Callable[[Any], dict]], Optional[Dict[str, Any]]]:
    """help文档
    
    包含指令：
        - /help

    返回值：
        (callback_func, extra_kwargs) or 
        (None, None) or 
        (None, dict)
    """
    return help.help, {}

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
        (None, dict)
    """
    if raw_args == '-h' or raw_args == 'help':
        return admin.help, {}
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
        (None, dict)
    """
    if raw_args == '-h' or raw_args == 'help':
        return clear.help, {}
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
        (None, dict)
    """
    if raw_args == '-h' or raw_args == 'help':
        return bind.help, {}
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

async def handler_alias(
    user: KokomiUser, 
    raw_args: str
) -> Tuple[Optional[Callable[[Any], dict]], Optional[Dict[str, Any]]]:
    """绑定指令
    
    包含指令：
        - /alias list
        - /alias add <alias> <IGN/AID>
        - /alias del <alias_index>

    返回值：
        (callback_func, extra_kwargs) or 
        (None, None) or 
        (None, dict)
    """
    if raw_args == '-h' or raw_args == 'help':
        return alias.help, {}
    alias_data = {
        'alias': None,
        'region_id': None,
        'account_id': None,
        'nickname': None
    }
    if raw_args == '':
        return None, None
    if raw_args == 'list':
        # list
        return alias.alias_list, None
    args_list = raw_args.split(' ')
    args_len = len(args_list)
    if args_list[0] == 'del':
        # del
        if (
            args_len == 2 and 
            args_list[1].isdigit() and
            0 <= int(args_list[1]) - 1 < len(user.local.alias_list)
        ):
            return alias.del_alias, {'alias_index': int(args_list[1]) - 1}
        else:
            return None, None
    elif args_list[0] == 'add':
        # add
        if args_len == 4:
            # 通过IGN方式
            alias_data['alias'] = args_list[1]
            if args_list[1].isdigit():
                return None, JSONResponse.API_10013_AliasCannotBeNumericOnly
            if len(args_list[1]) >= 10:
                return None, JSONResponse.API_10014_AliasTooLong
            region_id = get_region_id_from_input(args_list[2])
            if not region_id:
                return None, None
            search_result = await search_user(region_id=region_id, nickname=args_list[3])
            if search_result['code'] != 1000:
                return None, search_result
            alias_data['account_id'] = search_result['data'][0]['account_id']
            alias_data['region_id'] = search_result['data'][0]['region_id']
            alias_data['nickname'] = search_result['data'][0]['name']
            return alias.add_alias, {'alias_data': alias_data}
        elif args_len == 3:
            # 通过AID方式
            alias_data['alias'] = args_list[1]
            if args_list[1].isdigit():
                return None, JSONResponse.API_10013_AliasCannotBeNumericOnly
            if len(args_list[1]) >= 10:
                return None, JSONResponse.API_10014_AliasTooLong
            if not args_list[2].isdigit():
                return None, None
            account_id = int(args_list[2])
            region_id = get_region_id_from_aid(account_id)
            if not region_id:
                return None, None
            check_result = await check_user(region_id=region_id,account_id=account_id)
            if check_result['code'] == 1001:
                return None, None
            if check_result['code'] != 1000:
                return None, check_result
            alias_data['account_id'] = check_result['data']['account_id']
            alias_data['region_id'] = check_result['data']['region_id']
            alias_data['nickname'] = check_result['data']['name']
            return alias.add_alias, {'alias_data': alias_data}
        else:
            return None, None
    else:
        return None, None

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
    if raw_args == '-h' or raw_args == 'help':
        return bind.lang_help, {}
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
    if raw_args == '-h' or raw_args == 'help':
        return bind.mode_help, {}
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
    if raw_args == '-h' or raw_args == 'help':
        return theme.help, {}
    if raw_args == 'list':
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
    if raw_args == '-h' or raw_args == 'help':
        return bind.algo_help, {}
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
        - /stat [@/IGN/AID] [BattleType]    # 注释中简写为BT

    返回值：
        (callback_func, extra_kwargs) or 
        (None, None) or 
        (None, dict)
    """
    if raw_args == '-h' or raw_args == 'help':
        return overall.help, {}
    if raw_args == '':
        return overall.main, None
    params = {
        'region_id': None,
        'account_id': None
    }
    filter_dict = {
        'pvp': 'random', 'random': 'random', '随机': 'random', 'ランダム戦': 'random',
        'rank': 'ranked', 'ranked': 'rankded', '排位': 'ranked', 'ランク戦': 'ranked',
        'solo': 'pvp_solo', '单野': 'pvp_solo', 'div2': 'pvp_div2', '双排': 'pvp_div2',
        'div3': 'pvp_div3', '三排': 'pvp_div3', 'aircarrier': 'aircarrier', 'cv': 'aircarrier', 
        'battleship': 'battleship', 'bb': 'battleship', 'cruiser': 'cruiser', 'ca': 'cruiser', 
        'cl': 'cruiser', 'destroyer': 'destroyer', 'dd': 'destroyer', 'ss': 'submarine', 
        'sub': 'submarine', 'submarine': 'submarine', '航母': 'aircarrier', '战列': 'battleship', 
        '巡洋': 'cruiser', '驱逐': 'destroyer', '潜艇': 'submarine', '水下小人': 'submarine', 
        '空中小人': 'aircarrier', 'surface': 'surface_ships', '水面': 'surface_ships'
    }
    args_list = raw_args.split(' ')
    args_len = len(args_list)
    if args_len == 1:
        # 长度为1只有三种形式 /basic @ | /basic AID | /basic BT
        if '@' in args_list[0] or '!' in args_list[0]:
            # 通过解析@字符串的方式
            match = extract_mention_id(args_list[0])
            if match:
                user.basic.id = match
            else:
                return None, None
            if args_list[1].lower() in filter_dict:
                return overall.main, {'filter_type': filter_dict.get(args_list[0].lower())}
            else:
                return None, None
        elif args_list[0].isdigit():
            # 通过UID绑定
            account_id = int(args_list[0])
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
            if args_list[0].lower() in filter_dict:
                return overall.main, {'filter_type': filter_dict.get(args_list[0].lower())}
            else:
                return None, None
    elif args_len == 2:
        # 长度为1只有三种形式 /basic @ BT | /basic AID BT | /basic IGN
        if '@' in args_list[0] or '!' in args_list[0]:
            # 通过解析@字符串的方式
            match = extract_mention_id(args_list[0])
            if match:
                user.basic.id = match
            else:
                return None, None
            if args_list[1].lower() in filter_dict:
                return overall.main, {'filter_type': filter_dict.get(args_list[1].lower())}
            else:
                return None, None
        elif args_list[0].isdigit():
            # 通过UID绑定
            account_id = int(args_list[0])
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
            if args_list[1].lower() in filter_dict:
                return overall.main, {'filter_type': filter_dict.get(args_list[1].lower())}
            else:
                return None, None
        else:
            # 通过 IGN 方式
            region_id = get_region_id_from_input(args_list[0])
            if not region_id:
                return None, None
            search_result = await search_user(region_id=region_id, nickname=args_list[1])
            if search_result['code'] != 1000:
                return None, search_result
            params['account_id'] = search_result['data'][0]['account_id']
            params['region_id'] = search_result['data'][0]['region_id']
            user.set_user_bind(params)
    elif args_len == 3:
        # 长度为1只有一种形式 /basic IGN BT
        # 通过 IGN 方式
        region_id = get_region_id_from_input(args_list[0])
        if not region_id:
            return None, None
        search_result = await search_user(region_id=region_id, nickname=args_list[1])
        if search_result['code'] != 1000:
            return None, search_result
        params['account_id'] = search_result['data'][0]['account_id']
        params['region_id'] = search_result['data'][0]['region_id']
        user.set_user_bind(params)
        if args_list[2].lower() in filter_dict:
            return overall.main, {'filter_type': filter_dict.get(args_list[2].lower())}
        else:
            return None, None
    else:
        return None, None