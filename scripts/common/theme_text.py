from typing import Literal


class ThemeTextColor:
    def __init__(self, theme: Literal['dark', 'light']):
        if theme.lower() == "dark":
            self.TextThemeColor1 = "#FFFFFF"  # 主标题颜色（白色）
            self.TextThemeColor2 = "#CCCCCC"  # 副标题颜色
            self.TextThemeColor3 = "#999999"  # 正文颜色
            self.TextThemeColor4 = "#666666"  # 次要信息颜色
            self.TextThemeColor5 = "#333333"  # 暗灰色信息
        elif theme.lower() == "light":
            self.TextThemeColor1 = "#000000"  # 主标题颜色（黑色）
            self.TextThemeColor2 = "#333333"  # 副标题颜色
            self.TextThemeColor3 = "#666666"  # 正文颜色
            self.TextThemeColor4 = "#999999"  # 次要信息颜色
            self.TextThemeColor5 = "#CCCCCC"  # 浅灰色信息
        else:
            raise ValueError("Invalid theme. Please choose 'dark' or 'light'.")