class AppContext:
    InitStatus = False
    SupportedLangCode = []
    SupportedTheme = None

    @classmethod
    def set_init_status(cls):
        cls.InitStatus = True

    @classmethod
    def set_languages(cls, lang_code: str):
        cls.SupportedLangCode.append(lang_code)
