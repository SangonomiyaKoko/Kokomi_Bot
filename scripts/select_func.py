from .common import JSONResponse
from .resources import *

class SelectFunc:
    def main(message_list: list):
        if (
            len(message_list) == 1 and
            message_list[0] == 'message'
        ):
            return {
                'callback_func': None,
                'extra_kwargs': {}
            }
        return None