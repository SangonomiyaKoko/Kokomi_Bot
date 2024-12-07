from scripts.common import ResponseDict
from .cn import LANGUAGE as LANGUAGE_CN
from .en import LANGUAGE as LANGUAGE_EN
from .ja import LANGUAGE as LANGUAGE_JA

class Message:
    def return_message(language: str, result: ResponseDict) -> str:
        "通过code值返回对应的返回值"
        language_dict = {
            'cn': LANGUAGE_CN,
            'en': LANGUAGE_EN,
            'ja': LANGUAGE_JA
        }
        language_data = language_dict[language]
        if language_data.get(result['code']):
            return language_data.get(result['code'])
        else:
            return result['message']