from .base import ContentLanguageBase

class ContentLanguage(ContentLanguageBase):
    Test = '测试'
    UserClan = '所属工会'
    Createdat = '注册时间'
    DataType = ''
    RatingNextText_1 = '距离下一评级'
    RatingNextText_2 = '超出最高评级'

    def get_rating_text(rating_class: int, return_len: bool = False) -> str | tuple:
        rating_text_list = [
            '水平未知','还需努力','低于平均',
            '平均水平','好','很好','非常好',
            '大佬平均','神佬平均','战舰仙人'
        ]
        rating_len_list = [
            430, 430, 430, 430,
            210, 280, 355, 430,
            430, 430
        ]
        if return_len:
            return rating_text_list[rating_class], rating_len_list[rating_class]
        else:
            return rating_text_list[rating_class]

    def get_rank_text(season_rank: int) -> str:
        rank_text_dict = {
            1: '黄金联盟',
            2: '白银联盟',
            3: '青铜联盟'
        }
        return rank_text_dict.get(season_rank)