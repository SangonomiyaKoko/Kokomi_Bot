from typing_extensions import Optional, TypedDict, Union, Dict


class DogTagDict(TypedDict):
    texture_id: int
    symbol_id: int
    border_color_id: int
    background_color_id: int
    background_id: int

class UserBasicDict(TypedDict):
    id: int
    name: str
    karma: int
    crated_at: int
    actived_at: int
    dog_tag: Union[Dict, None]

class UserClanDict(TypedDict):
    id: int
    tag: str
    league: int

class UserOverallDict(TypedDict):
    battles_count: str
    win_rate: str
    avg_damage: str
    avg_frags: str
    avg_exp: str
    rating: str
    rating_class: int
    rating_next: int
    win_rate_color: str
    avg_damage_color: str
    avg_frags_color: str
    rating_color: str

class ResultBattleTypeDict:
    pvp_solo: Optional[UserOverallDict]
    pvp_dvi2: Optional[UserOverallDict]
    pvp_div3: Optional[UserOverallDict]
    rank_solo: Optional[UserOverallDict]

class ResultShipTypeDict:
    AirCarrier: UserOverallDict
    Battleship: UserOverallDict
    Cruiser: UserOverallDict
    Destroyer: UserOverallDict
    Submarine: UserOverallDict