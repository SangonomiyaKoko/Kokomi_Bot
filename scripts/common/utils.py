class Utils:
    def get_language(language: str) -> str:
        "获取接口语言的参数内容"
        language_dict = {
            'cn': 'chinese',
            'en': 'english',
            'ja': 'japanese'
        }
        return language_dict.get(language)
    
    def get_operator_by_id(region_id: int) -> str:
        "获取服务器id对应的运营商，不同运营商对应的素材会有不同"
        if region_id == 4:
            return 'LestaGame'
        else:
            return 'WarGaming'

    def get_region_by_id(region_id: int) -> str:
        "获取region"
        region_dict = {
            1: 'asia',
            2: 'eu',
            3: 'na',
            4: 'ru',
            5: 'cn'
        }
        return region_dict.get(region_id)

    def get_default_language(platform: dict) -> str:
        "获取平台默认的语言"
        if platform['type'] in ['qq_bot', 'qq_group', 'qq_guild']:
            return 'cn'
        else:
            return 'en'
        
    def get_default_picture() -> dict:
        "获取默认的图片格式"
        return {
            'background': '#F8F9FB',
            'content': 'light',
            'theme': 'default'
        }