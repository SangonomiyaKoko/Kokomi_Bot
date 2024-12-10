from .common import JSONResponse
from .resources import (
    overall
)

class SelectFunc:
    def main(message_list: list):
        if (
            len(message_list) == 1 and
            message_list[0] == 'me'
        ):
            return {
                'callback_func': overall.main,
                'extra_kwargs': {}
            }
        return None