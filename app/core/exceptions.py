class AppInitError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class I18nRegisterError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)