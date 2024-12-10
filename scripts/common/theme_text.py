from typing import Literal


class ThemeTextColor:
    def __init__(self, theme: Literal['dark', 'light']):
        if theme.lower() == "dark":
            self.TextThemeColor1 = (255, 255, 255)  # 主标题颜色（白色）
            self.TextThemeColor2 = (225, 225, 225)  # 副标题颜色
            self.TextThemeColor3 = (180, 180, 180)  # 正文颜色
            self.TextThemeColor4 = (130, 130, 130)  # 次要信息颜色
            self.TextThemeColor5 = (80, 80, 80)  # 次要信息颜色
        elif theme.lower() == "light":
            self.TextThemeColor1 = (0, 0, 0)  # 主标题颜色（黑色）
            self.TextThemeColor2 = (20, 20, 20)  # 副标题颜色
            self.TextThemeColor3 = (75, 75, 75)  # 正文颜色
            self.TextThemeColor4 = (125, 125, 125)  # 次要信息颜色
            self.TextThemeColor5 = (175, 175, 175)  # 次要信息颜色
        else:
            raise ValueError("Invalid theme. Please choose 'dark' or 'light'.")