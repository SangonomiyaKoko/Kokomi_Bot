from .common import JSONResponse, Utils
from .resources import (
    overall,
    bind,
    signature,
    rank_user,
    rank_page,
    test
)

class SelectFunc:
    def return_data(callback_func, extra_kwargs: dict | None):
        return {
            'status': 'ok',
            'code': 1000,
            'message': 'Success',
            'data': {
                'callback_func': callback_func,
                'extra_kwargs': extra_kwargs if extra_kwargs else {}
            }
        }

    @classmethod
    def main(cls, user_binding_status: bool, message_list: list):
        '''
        /test
        /link
            <link> <>
            <link> <UserID>
        /set
            <set> <language> <LanguageList>
            <set> <rating> <Show/Hide>
            <set> <background> <HexColor>
            <set> <theme> <Dark/Light>
            <set> <picture> <PictureList>
        /me
            <me/overall>
            <me/overall> <>
        /signature
            <signature/card>
            <signature/card> <>
        /lifetime
            <lifetime>
        /random
            <pvp/random>
            <pvp/random> <>
        /ranked
            <rank/ranked>
            <rank/ranked> <>
        /ranked [season]
            <rank/ranked> <s><SeasonID>
            <rank/ranked> <> <s><SeasonID>
        /cb
            <cb>
            <cb> <>
        /oper
            <oper/operation>
            <oper/operation> <>
        /ship [shipname]
            <ship> <ShipName>
            <ship> <> <ShipName>
        /ships [filters]
            <ships> <Filters>
            <ships> <> <Filters>
        /clan
            <clan> 
            <clan> <>
        /clan [season]
            <clan> <s><SeasonID>
            <clan> <> <s><SeasonID>
        /clan history
            <clan> <history>
            <clan> <> <history>
        /recent [RecentType] [DateNumber/DateRange]
            <recent> [RecentType] [DateNumber/DateRange]
            <recent> <> [RecentType] [DateNumber/DateRange]
        /recent ship <ShipName> [DateNumber/DateRange]
        /recents [DateNumber/DateRange]

        '''
        # 以下为不需要用户绑定的指令
        if message_list[0] == 'test':
            callback_func = test.main
            extra_kwargs = {}
            return cls.return_data(callback_func, extra_kwargs)
        if (
            len(message_list) == 3 and
            message_list[0] == 'link'
        ):
            region_id = Utils.get_region_id_from_input(message_list[1])
            if not region_id:
                return JSONResponse.API_9007_InvaildParams
            callback_func = bind.post_bind
            extra_kwargs = {
                'region_id': region_id,
                'nickname': message_list[2]
            }
            return cls.return_data(callback_func, extra_kwargs)
        if not user_binding_status:
            return JSONResponse.API_9001_UserNotLinked
        # 以下为需要用户绑定的指令
        if (
            len(message_list) == 1 and
            message_list[0] == 'me'
        ):
            callback_func = overall.main
            extra_kwargs = {}
            return cls.return_data(callback_func, extra_kwargs)
        if (
            len(message_list) == 2 and
            message_list[0] == 'me' and
            message_list[1] == 'leader'
        ):
            callback_func = rank_page.main
            extra_kwargs = {}
            return cls.return_data(callback_func, extra_kwargs)
        if (
            len(message_list) == 2 and
            message_list[0] == 'me' and
            message_list[1] == 'leader2'
        ):
            callback_func = rank_user.main
            extra_kwargs = {}
            return cls.return_data(callback_func, extra_kwargs)
        if (
            len(message_list) == 1 and
            message_list[0] == 'sign'
        ):
            callback_func = signature.main
            extra_kwargs = {}
            return cls.return_data(callback_func, extra_kwargs)
        if (
            len(message_list) == 3 and
            message_list[0] == 'set' and
            message_list[1] == 'language'
        ):
            language = Utils.get_language_from_input(message_list[2])
            if not language:
                return JSONResponse.API_9007_InvaildParams
            callback_func = bind.update_language
            extra_kwargs = {
                'language': language
            }
            return cls.return_data(callback_func, extra_kwargs)
        if (
            len(message_list) == 3 and
            message_list[0] == 'set' and
            message_list[1] == 'rating' and
            message_list[2] in ['show','hide']
        ):
            if message_list[2] == 'show':
                algorithm = 'pr'
            else:
                algorithm = ''
            callback_func = bind.update_algorithm
            extra_kwargs = {
                'algorithm': algorithm
            }
            return cls.return_data(callback_func, extra_kwargs)
        return JSONResponse.API_9002_FuncNotFound