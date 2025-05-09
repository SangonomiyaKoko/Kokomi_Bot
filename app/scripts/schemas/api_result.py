from typing_extensions import Optional, TypedDict, Union, Dict


class DogTagDict(TypedDict):
    texture_id: int
    symbol_id: int
    border_color_id: int
    background_color_id: int
    background_id: int

class UserBasicDict(TypedDict):
    id: int
    region: int
    name: str
    karma: int
    created_at: int
    actived_at: int
    dog_tag: Union[Dict, None]

class UserClanDict(TypedDict):
    id: int
    tag: str
    league: int

class UserSignatureDict(TypedDict):
    battles_count: str
    win_rate: str
    avg_damage: str
    avg_frags: str
    rating: str
    win_rate_class: str
    avg_damage_class: str
    avg_frags_class: str
    rating_class: int

class UserOverallDict(TypedDict):
    battles_count: str
    win_rate: str
    avg_damage: str
    avg_frags: str
    avg_exp: str
    rating: str
    rating_next: int
    win_rate_class: str
    avg_damage_class: str
    avg_frags_class: str
    rating_class: int

class ResultBattleTypeDict:
    pvp_solo: Optional[UserOverallDict]
    pvp_dvi2: Optional[UserOverallDict]
    pvp_div3: Optional[UserOverallDict]
    rank_solo: Optional[UserOverallDict]

class BasicBattleTypeDict:
    solo: Optional[UserOverallDict]
    dvi2: Optional[UserOverallDict]
    div3: Optional[UserOverallDict]

class ResultShipTypeDict:
    AirCarrier: UserOverallDict
    Battleship: UserOverallDict
    Cruiser: UserOverallDict
    Destroyer: UserOverallDict
    Submarine: UserOverallDict