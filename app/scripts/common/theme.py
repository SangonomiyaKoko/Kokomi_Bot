from typing import Literal


class ThemeTextColor:
    def __init__(self, theme: Literal['dark', 'light']):
        if theme.lower() == "dark":
            self.TextThemeColor1 = (255, 255, 255)
            self.TextThemeColor2 = (225, 225, 225)
            self.TextThemeColor3 = (180, 180, 180)
            self.TextThemeColor4 = (130, 130, 130)
            self.TextThemeColor5 = (80, 80, 80)
        elif theme.lower() == "light":
            self.TextThemeColor1 = (0, 0, 0)
            self.TextThemeColor2 = (20, 20, 20)
            self.TextThemeColor3 = (75, 75, 75)
            self.TextThemeColor4 = (125, 125, 125)
            self.TextThemeColor5 = (175, 175, 175)
        else:
            raise ValueError("Invalid theme. Please choose 'dark' or 'light'.")
        
class ThemeRatingColor:
    def __init__(self, theme: Literal['dark', 'light']):
        if theme.lower() == "dark":
            self.RatingThemeColor = [
                (127, 127, 127),
                (205, 51, 51),
                (254, 121, 3),
                (255, 193, 7),
                (78, 206, 0),
                (10, 145, 0),
                (52, 186, 211),
                (200, 45, 200),
                (147, 50, 212)
            ]
        elif theme.lower() == "light":
            self.RatingThemeColor = [
                (127, 127, 127),
                (205, 51, 51),
                (254, 121, 3),
                (255, 193, 7),
                (68, 179, 0),
                (49, 128, 0),
                (52, 186, 211),
                (121, 61, 182),
                (88, 43, 128)
            ]
        else:
            raise ValueError("Invalid theme. Please choose 'dark' or 'light'.")
    
    def get_class_color(self, content_class: int) -> tuple:
        '''获取评分等级对应的颜色'''
        if type(content_class) == str:
            content_class = int(content_class)
        return self.RatingThemeColor[content_class]
        
class ThemeClanColor:
    def __init__(self, theme: Literal['dark', 'light']):
        if theme.lower() == "dark":
            self.RatingThemeColor = [
                (121, 61, 182),
                (144, 223, 143),
                (234, 197, 0),
                (147, 147, 147),
                (184, 115, 51)
            ]
        elif theme.lower() == "light":
            self.RatingThemeColor = [
                (121, 61, 182),
                (144, 223, 143),
                (234, 197, 0),
                (147, 147, 147),
                (184, 115, 51)
            ]
        else:
            raise ValueError("Invalid theme. Please choose 'dark' or 'light'.")
    
    def get_color(self, content_class: int) -> tuple:
        '''获取评分等级对应的颜色'''
        if type(content_class) == str:
            content_class = int(content_class)
        return self.RatingThemeColor[content_class]
        
class ThemeRegionColor:
    def __init__(self, theme: Literal['dark', 'light']):
        if theme.lower() == "dark":
            self.RatingThemeColor = [
                (234, 104, 162),
                (0, 183, 238),
                (50, 177, 108),
                (248, 181, 81),
                (137, 87, 161)
            ]
        elif theme.lower() == "light":
            self.RatingThemeColor = [
                (234, 104, 162),
                (0, 183, 238),
                (50, 177, 108),
                (248, 181, 81),
                (137, 87, 161)
            ]
        else:
            raise ValueError("Invalid theme. Please choose 'dark' or 'light'.")
    
    def get_color(self, content_class: int) -> tuple:
        '''获取评分等级对应的颜色'''
        if type(content_class) == str:
            content_class = int(content_class)
        return self.RatingThemeColor[content_class]