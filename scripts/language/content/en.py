class ContentLanguage:
    UserClan = 'User\'s Clan'
    Createdat = 'Created at'
    DataType = ''
    RatingNextText_1 = 'Next level'
    RatingNextText_2 = 'Out of top rating'
    
    def get_rating_text(rating_class: int, return_len: bool = False) -> str | tuple:
        rating_text_list = [
            'Unknow','Improvement Needed','Below Average',
            'Average','Good','Very Good','Great','Unicum',
            'Super Unicum','Super Ultra Unicum'
        ]
        rating_len_list = [
            425,910,660,420,
            300,500,330,410,
            630,825
        ]
        if return_len:
            return rating_text_list[rating_class], rating_len_list[rating_class]
        else:
            return rating_text_list[rating_class]

    def get_rank_text(season_rank: int) -> str:
        rank_text_dict = {
            1: 'Gold',
            2: 'Silver',
            3: 'Bronze'
        }
        return rank_text_dict.get(season_rank)