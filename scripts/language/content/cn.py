class ContentLanguage:
    UserClan = '所属工会'
    Createdat = '注册时间'
    DataType = ''
    RatingNextText_1 = '距离下一评级'
    RatingNextText_2 = '超出最高评级'

    def get_rating_text(rating_class: int, return_len: bool = False) -> str | tuple:
        rating_text_list = [
            '水平未知','还需努力','低于平均',
            '平均水平','好','很好','非常好',
            '大佬平均','神佬平均'
        ]
        rating_len_list = [
            425, 910
        ]