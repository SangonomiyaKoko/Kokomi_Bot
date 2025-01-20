from .picture.cn import ContentLanguage as ContentText_CN
from .picture.en import ContentLanguage as ContentText_EN
from .picture.ja import ContentLanguage as ContentText_JA
from .picture.base import ContentLanguageBase


class Content:
    def get_content_language(language) -> ContentLanguageBase:
        language_dict = {
            'cn': ContentText_CN,
            'en': ContentText_EN,
            'ja': ContentText_JA
        }
        if language not in language_dict:
            raise ValueError("Invaild language.")
        return language_dict[language]