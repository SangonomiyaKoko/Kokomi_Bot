from .common import JSONResponse, Utils
from .resources import (
    overall,
    bind
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
    def main(cls, message_list: list):
        if (
            len(message_list) == 1 and
            message_list[0] == 'me'
        ):
            callback_func = overall.main
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