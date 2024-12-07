class Utils:
    def get_default_language(platform: dict) -> str:
        if platform['type'] in ['qq_bot', 'qq_group', 'qq_guild']:
            return 'cn'
        else:
            return 'en'
        
    def get_default_picture() -> int:
        return 1