from .base import ContentLanguageBase

class ContentLanguage(ContentLanguageBase):
    Test = 'テスト'
    UserClan = 'クラン'
    Createdat = '登録日'
    Activedat = '最終アクティブ'
    DataType = ''
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

    def get_rank_text(season_rank: int) -> str:
        rank_text_dict = {
            1: 'Gold',
            2: 'Silver',
            3: 'Bronze'
        }
        return rank_text_dict.get(season_rank)
    
    def get_basic_type_text(filte_type: str) -> str:
        filter_type_dict = {
            'pvp': 'ランダム戦全体', 'rank': 'ランク戦全体', 'pvp_solo': 'ランダム戦 (ソロ)', 
            'pvp_div2': 'ランダム戦 (二人分隊)', 'pvp_div3': 'ランダム戦 (三人分隊)','AirCarrier': 'ランダム戦 (空母)',
            'Battleship': 'ランダム戦 (戦艦)','Cruiser': 'ランダム戦 (巡洋艦)','Destroyer': 'ランダム戦 (駆逐艦)',
            'Submarine': 'ランダム戦 (潜水艦)','SurfaceShips': 'ランダム戦 (水上艦)'
        }
        return filter_type_dict.get(filte_type)