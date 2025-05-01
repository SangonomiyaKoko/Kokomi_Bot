from .base import ContentLanguageBase

class ContentLanguage(ContentLanguageBase):
    Test = 'Test'
    UserClan = 'User\'s Clan'
    Createdat = 'Created at'
    Activedat = 'Last Active at'
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
    
    def get_basic_type_text(filte_type: str) -> str:
        filter_type_dict = {
            'pvp': 'Random All', 'rank': 'Ranked All', 'pvp_solo': 'Solo Random', 
            'pvp_div2': 'Div2 Random', 'pvp_div3': 'Div3 Random','AirCarrier': 'AirCarrier Random',
            'Battleship': 'Battleship Random','Cruiser': 'Cruiser Random','Destroyer': 'Destroyer Random',
            'Submarine': 'Submarine Random','SurfaceShips': 'SurfaceShips Random'
        }
        return filter_type_dict.get(filte_type)