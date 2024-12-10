class ContentLanguage:
    UserClan = 'クラン'
    Createdat = '登録日'
    DataType = ''
    RatingText_0 = '水平未知'
    RatingText_1 = '良くない'
    RatingText_2 = '並以下'
    RatingText_3 = '並'
    RatingText_4 = '良い'
    RatingText_5 = 'とても良い'
    RatingText_6 = '素晴らしい'
    RatingText_7 = 'Unicum'
    RatingText_8 = 'Super Unicum'
    RatingNextText_1 = '次の段階'
    RatingNextText_2 = '最高評価の外'
    
    def get_rating_text(rating_class: int, return_len: bool = False) -> str | tuple:
        rating_text_list = [
            '水平未知','良くない','並以下','並',
            '良い','とても良い','素晴らしい','Unicum',
            'Super Unicum','Super Ultra Unicum'
        ]
        rating_len_list = [
            430,440,360,210,
            286,516,516,410,
            630,825
        ]
        if return_len:
            return rating_text_list[rating_class], rating_len_list[rating_class]
        else:
            return rating_text_list[rating_class]