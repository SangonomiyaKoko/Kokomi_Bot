from .message import Message
from .content.cn import ContentLanguage as ContentText_CN
from .content.en import ContentLanguage as ContentText_EN
from .content.ja import ContentLanguage as ContentText_JA

__all__ = [
    'Message',
    'ContentText_CN',
    'ContentText_EN',
    'ContentText_JA'
]