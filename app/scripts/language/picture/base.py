class ContentLanguageBase:
    '''
    基类
    '''
    Test = ''
    UserClan = ''
    Createdat = ''
    Activedat = ''
    DataType = ''
    RatingNextText_1 = ''
    RatingNextText_2 = ''
    
    def get_rating_text():
        raise NotImplementedError("Subclasses should implement this method")

    def get_rank_text():
        raise NotImplementedError("Subclasses should implement this method")
    
    def get_basic_type_text():
        raise NotImplementedError("Subclasses should implement this method")