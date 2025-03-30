# Bot 图片渲染逻辑

> 此处仅讨论图片生成逻辑，有关指令匹配的逻辑不在本文的讨论范围内

## 主要架构

带 ⚠️ 为涉及图片渲染的重要文件

```txt
├── app/
│   ├── assets/        # 静态图片资源 ⚠️
│   │   └── ...
│   ├── data/          # 本地数据库
│   │   └── ...
│   ├── mock/          # 测试用json数据
│   │   └── ...
│   ├── scripts/       # 用于生成图片的脚本
│   │   ├── api/           # 用于调用api接口
│   │   ├── command/       # 指令解析
│   │   ├── common/        # 工具函数 ⚠️
│   │   ├── config/        # 配置
│   │   ├── db/            # 本地数据读取函数
│   │   ├── image/         # 图片处理模块 ⚠️
│   │   │   ├── fonts.py       # 字体管理
│   │   │   ├── generation.py  # 对相关文字渲染和图片叠加函数的封装 ⚠️⚠️⚠️
│   │   │   └── ...
│   │   ├── language/      # 多语言支持
│   │   ├── logs/          # bot日志模块
│   │   ├── resources/     # 图片渲染脚本 ⚠️⚠️⚠️
│   │   ├── schemas/       # 类型提示及参数效验
│   │   └── ...
│   ├── __init__.py
│   ├── main.py        # bot入口文件
│   ├── permission.py  # 用户权限
│   ├── config.yaml    # 配置文件
│   └── package.json   # 版本标识
```

## 图片大致渲染流程

1. 首先，图片通过 PS 完成设计，确定好图层渲染优先级，将图片的主体部分或者组件部分保存到 bot 的 assets 静态资源文件夹，一般是带 alpha 通道的 png 图片

```txt
渲染逻辑从左到右，其中[]表示不一定有该图层

背景 -> [图片主题] -> 图片主体 -> [组件] -> 文字或者图形
```

2. 用户输入指令，通过 `app\scripts\command` 下的指令解析代码，将指令解析为对应的 `图片渲染脚本` 和 `渲染参数`

```txt
用户id(例如123456789) => 获取用户的账号 => /basic指令的图片渲染参数

用户msg(例如wws me) => 匹配到/basic指令 => /basic指令的图片渲染脚本
```

3. 并由主函数调用，如下代码所示

```python
# app\main.py
generate_func = select_result['data']['callback_func']
...
generate_result = await generate_func(
    user = kokomi_user,
    **select_result['data']['extra_kwargs']
)
```

4. 所有的图片渲染脚本都位于 `app\scripts\resources` 文件夹下，每个脚本文件都由如下结构构成

```python
# 导入资源

# 主函数，主要用来请求获取页面渲染的数据
@ExceptionLogger.handle_program_exception_async    # 异常捕获
async def main(user: KokomiUser, extra_kwargs: str) -> dict:
    # 请求接口
    ...
    # 接口返回值的效验
    ...
    # 效验通过后，调用图片渲染函数，获取图片
    result = get_png(
        user=user,
        result=result
    )
    return result  # 返回渲染结果

# 图片渲染函数，只用于实现通过数据渲染图片
@TimeFormat.cost_time_sync(message='Image generation completed')   # debug用
def get_png(user: KokomiUser, result: dict) -> dict:
    # 设定画布宽度和高度
    width, height = 150, 75
    # 创建画布并叠加图片主题
    ...
    # 获取相关语言或者文字的信息
    ...
    # 开始图片渲染流程
    with ImageDrawManager(res_img) as image_manager:
        # 提交图片操作，例如在图片上写上文字或者形状
        ...
        # 在图片上叠加需要的图片
        ...
        image_manager.execute_operations()       # 提交并处理操作
        res_img = image_manager.get_image()      # 获取处理好的图片
        result = ImageHandler.save_image(res_img)   # 图片保存
        return result
```

接下来将对每个涉及到图片渲模块的文件或者代码进行解析

## 渲染脚本参数

从上面的渲染脚本文件接口可以看出，每个渲染脚本都包括两个参数 `kokomi_user` 和 `extra_kwargs`

### kokomi_user 参数

> ⚠️ 该参数是固定参数，不管是否需要都必须写

kokomi_user 参数类型为实例化后 KokomiUser 类的**引用**，你可以在 `app\scripts\schemas\user_base.py` 文件内找到它的定义和数据结构，实例化在 `app\main.py` 主函数内

该参数的主要用处就是保存当前请求的用户的基本信息，比如用户 id 和绑定数据，以及后续图片渲染需要的相关参数

### extra_kwargs 参数

> ⚠️ 该参数为非必须参数，且数量不固定

该参数的主要用处是通过解析指令获取到的额外参数，例如指令 `wws me recent 10` 中的参数 10

## 渲染数据获取

在图片渲染脚本的 main 文件，实现读取接口获取数据的功能，例如如下代码

```python
@ExceptionLogger.handle_program_exception_async
async def main(
    user: KokomiUser
) -> dict:
    # api配置，调用该接口获取数据
    path = '/api/v1/robot/user/account/'
    params = {
        'region': Utils.get_region_by_id(user.bind.region_id),
        'account_id': user.bind.account_id,
        'game_type': 'overall',
        'language': Utils.get_language(user.local.language)
    }
    if user.local.algorithm:
        params['algo_type'] = user.local.algorithm

    # 在debug测试阶段可以使用mock跳过网络请求来测试图片渲染
    if bot_settings.USE_MOCK:
        result = Mock.read_data('basic.json')
        logging.debug('Using MOCK, skip network requests')
    else:
        # 实际的api请求
        result = await BaseAPI.get(
            path=path,
            params=params
        )

    # 数据效验
    if 2000 <= result['code'] <= 9999:
        logging.error(f"API Error, Error: {result['message']}")
        return result
    if result['code'] != 1000:
        return result

    # 效验通过后，调用图片渲染函数，获取图片
    result = get_png(
        user=user,
        result=result
    )
    return result  # 返回渲染结果
```

## 图片渲染前准备

在进入图片渲染脚本的 get_png 函数后，开始图片渲染开始前，还有几件事需要准备好。

其中 kokomi_user 的 local 包括以下数据

```python
class UserLocal:
    "用户本地信息类"
    def __init__(self, platform: Platform):
        "先按默认值初始化类"
        self.language = self.__get_default_language(platform)
        self.algorithm = self.__get_default_algorithm()
        self.background = self.__get_default_picture('background')
        self.content = self.__get_default_picture('content')
        self.theme = self.__get_default_picture('theme')
```

- `background`: 用来表示图片背景颜色，一般和主题绑定

- `content`：用来表示图片主题，只有两种深色和亮色

- `theme`：用来表示定制水表主题，一般为某个二次元角色

- `language`：用户使用的语言

以上四个参数会影响图片的最终效果

### 背景图片准备

1. 通过设置的图片 size 和 `background` 值新建一个 RGBA 格式的背景图片

2. 通过 `theme` 判断是否有特殊图片需要叠加在背景图片上

3. 通过用户的 `language` 和 `content` 将合适的图片主体叠加

4. 通过以上步骤才能合成我们需要的背景，然后进一步渲染数据

```python
# 画布宽度和高度
width, height = 150, 75
# 背景颜色（RGBA）
background_color = Utils.hex_to_rgb(user.local.background, 255)
# 创建画布
res_img = ImageHandler.new_image([width, height], background_color)
```

### 数据准备

因为不同用户的 `language` 和 `content` 不相同，所以需要获取到对应的数据

```python
# 获取语言对应的文本文字
content_text = Content.get_content_language(user.local.language)
# 获取不同主题的文字颜色
theme_text_color = ThemeTextColor(user.local.content)
# 获取不同主题的评分颜色
theme_rating_color = ThemeRatingColor(user.local.content)
```

比如深色主题下的用户评分颜色和亮色主题下不一样

```python
# app\scripts\common\theme.py

class ThemeRatingColor:
    def __init__(self, theme: Literal['dark', 'light']):
        if theme.lower() == "dark":
            self.RatingThemeColor = [
                (105, 105, 105),
                (125, 0, 0),
                (168, 66, 0),
                (183, 170, 0),
                (99, 140, 11),
                (0, 113, 48),
                (0, 117, 169),
                (234, 63, 224),
                (151, 38, 176)
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
                (211, 33, 213),
                (115, 13, 189)
            ]
        else:
            raise ValueError("Invalid theme. Please choose 'dark' or 'light'.")
```

## 图片渲染开始

在图片渲染脚本的 get_png 函数中，下面这行代码通常标志的开始进入图片渲染流程

```python
with ImageDrawManager(res_img) as image_manager:
```

其中，我们主要需要关注 `app\scripts\image\generation.py` 中以下四个模块

```python
from ..image import (
    ImageDrawManager, ImageHandler, TextOperation as Text, RectangleOperation as Rectangle
)
```

### ImageHandler 类

该类封装了 Pillow（PIL）库的常用图片处理方法，包括 创建、打开、调整大小、保存和合成 图片，部分功能使用了 NumPy 加速。主要是完成一些简单的图片操作，尤其是对涉及 IO 操作的封装

| 方法              | 功能                            | 关键点                     |
| ----------------- | ------------------------------- | -------------------------- |
| `new_image`       | 创建新图片                      | 支持 `RGB` 和 `RGBA`       |
| `open_image`      | 打开图片                        | 处理 **文件不存在** 的情况 |
| `resize_image`    | 调整图片大小                    | 调用 `resize` 方法         |
| `save_image`      | 保存图片                        | 处理保存失败的异常         |
| `composite_paste` | 直接 `paste` 叠加图片           | **不支持透明通道**         |
| `composite_alpha` | 使用 `alpha_composite` 叠加图片 | **支持透明通道**           |
| `composite_numpy` | 用 NumPy 计算图片叠加           | **性能优化，支持透明通道** |

> **在图片渲染脚本中主要使用前四个函数**，后三个图片叠加函数是暴露给其他函数使用，不要在图片渲染脚本中使用！

> ⚠️ 使用`open_image`函数时必须检查返回值的类型是否为 Image.Image 而不是 dict，原因可以看代码实现

```python
@staticmethod
def open_image(path: str) -> Image.Image:
    """打开图片文件，如果文件不存在，则返回占位图片。

    参数:
        path (str): 图片文件路径。

    返回:
        Image.Image: 加载的图片对象，如果文件不存在则返回占位图片。
    """
    try:
        return Image.open(path)
    except (FileNotFoundError, OSError):
        # 在这里捕获了file not found错误
        # 所以遇到返回值为dict时直接return返回结果
        return JSONResponse.API_10008_ImageResourceMissing
```

### ImageDrawManager 类

该类是一个用于处理图像绘制的管理器，继承自 ContextDecorator，使用上下文管理处理资源释放。主要实现以下功能：

- 支持文本和矩形绘制，按照优先级绘制顺序

- 支持图像叠加

类使用示例

```python
with ImageDrawManager(res_img) as image_manager:
    # 在这里进行图片操作
    ...
    image_manager.execute_operations()
    res_img = image_manager.get_image()  # 获取到渲染完成的图片
    result = ImageHandler.save_image(res_img)  # 图片保存
    return result
```

#### 1. 文本和矩形绘制

主要通过以下两个函数实现。

> ⚠️ 注意：从代码中可以看出，对图片的操作并不是立即实现的，而是先 append 到 list 中直到 `execute_operations` 函数被执行

```python
def add_text(self, operation: TextOperation):
    """写入文字到图片"""
    self.operations.append(operation)

def add_rectangle(self, operation: RectangleOperation):
    """绘制矩形到图片"""
    self.operations.append(operation)

...

def execute_operations(self):
    """统一执行所有记录的操作，按照优先级顺序绘制。

    该方法会根据操作的优先级（priority）从低到高排序，
    先绘制矩形，再绘制文字，确保优先级高的操作先完成。
    """
    self.draw = ImageDraw.Draw(self.image)
    # 按照优先级对操作进行排序，优先级小的操作先执行
    sorted_operations = sorted(self.operations, key=lambda x: x.priority)

    # 先绘制矩形
    for operation in sorted_operations:
        if isinstance(operation, RectangleOperation):
            self._draw_rectangle(operation)

    # 再绘制文字
    for operation in sorted_operations:
        if isinstance(operation, TextOperation):
            self._draw_text(operation)

    self.operations = None
```

传入进行图片操作的数据类结构

```python
class TextOperation:
    """封装写入文字的操作，支持指定字体、大小、颜色和优先级"""

    def __init__(
        self,
        text: str,
        position: Tuple[int, int],
        font_index: int,
        font_size: int,
        color: Tuple[int, int, int],
        align: Literal["left", "center", "right"] = "left",
        priority: int = 10
    ):
        """
        文字绘制操作

        参数:
            text (str): 要绘制的文字内容
            position (Tuple[int, int]): 文字的基准位置 (x, y)，其含义取决于对齐模式：
                - "left"（默认）: x 为文字的左边界
                - "center": x 为文字的中心
                - "right": x 为文字的右边界
            font_index (int): 字体索引，用于选择不同字体
            font_size (int): 字体大小
            color (Tuple[int, int, int]): 文字颜色 (R, G, B)
            align (Literal["left", "center", "right"], optional): 文字对齐方式，默认 "left"
            priority (int, optional): 操作优先级，数值越小优先级越高。默认 10
        """
        self.text = text
        self.position = position
        self.font_index = font_index
        self.font_size = font_size
        self.color = color
        self.priority = priority
        self.align = align  # 文字对齐方式

class RectangleOperation:
    """封装绘制矩形的操作，支持圆角矩形"""

    def __init__(self, position: tuple, size: tuple, color: tuple, corner_radius: int = 0, priority: int = 10):
        """
        初始化矩形操作

        参数:
            position (tuple): 矩形的位置 (x, y)
            size (tuple): 矩形的尺寸 (宽, 高)
            color (tuple): 矩形的填充颜色 (R, G, B)
            corner_radius (int, optional): 圆角半径，默认值为 0，即不绘制圆角
            priority (int, optional): 操作的优先级，数字越小优先级越高。默认值为 10
        """
        self.position = position
        self.size = size
        self.color = color
        self.corner_radius = corner_radius
        self.priority = priority
```

使用示例

```python
with ImageDrawManager(res_img) as image_manager:
    image_manager.add_text(
        Text(
            text=content_text.Test,
            position=(0,0),
            font_index=1,
            font_size=50,
            color=theme_text_color.TextThemeColor2,
            align='left',
            priority=10
        )
    )
    ... # 其他操作
    image_manager.execute_operations() # 只有在这一步才会被真正渲染到图片
```

#### 2. 图像叠加

主要通过以下两个函数实现。

> ⚠️ 注意：图片叠加函数对图片的操作是立即实现的，需要注意叠加顺序

```python
def composite_paste(
    self,
    fg: Image.Image,
    position: tuple = (0, 0)
) -> Image.Image:
    """使用 paste 方法叠加图片（适用于不带透明通道的图片）。

    该方法适用于不带 alpha 通道的前景图叠加到背景图上，
    如果前景图含有 alpha 通道，则会丢失 alpha 通道的信息。

    参数:
        fg (Image.Image): 需要叠加的前景图片。
        position (tuple): 前景图片放置的位置，默认为 (0, 0)。

    返回:
        Image.Image: 叠加后的图片对象。
    """
    # 叠加前景图到背景图
    self.image.paste(fg, position)
    return self.image  # 返回叠加后的图片

def composite_alpha(
    self,
    fg: Image.Image,
    position: tuple = (0, 0)
) -> Image.Image:
    """使用 alpha_composite 方法叠加两张图片（适用于带透明通道的图片）。

    该方法适用于带有 alpha 通道的图片，能够保留前景图的透明度效果。
    如果前景图不包含 alpha 通道，会先转换为 RGBA 格式。

    参数:
        fg (Image.Image): 需要叠加的前景图片。
        position (tuple): 前景图片放置的位置，默认为 (0, 0)。

    返回:
        Image.Image: 叠加后的图片对象，包含透明度效果。
    """
    # 如果前景图没有 alpha 通道，先转换为 RGBA
    if fg.mode != 'RGBA':
        fg = fg.convert("RGBA")

    # 叠加前景图到背景图，并保留透明度效果
    self.image = self.image.alpha_composite(fg, position)
    return self.image  # 返回叠加后的图片
```

## 最小 Dome

一个简单的 test 功能

```python
# app\scripts\resources\test.py

@ExceptionLogger.handle_program_exception_async
async def main(user: KokomiUser, test_msg: str) -> dict:
    result = get_png(
        user=user,
        test_msg=test_msg
    )
    return result

@TimeFormat.cost_time_sync(message='Image generation completed')
def get_png(user: KokomiUser, test_msg: str) -> str:
    # 画布宽度和高度
    width, height = 150, 75
    # 背景颜色（RGBA）
    background_color = Utils.hex_to_rgb(user.local.background, 255)
    # 创建画布
    res_img = ImageHandler.new_image([width, height], background_color)
    # 获取语言对应的文本文字
    content_text = Content.get_content_language(user.local.language)
    # 获取不同主题的文字颜色
    theme_text_color = ThemeTextColor(user.local.content)
    # 需要叠加的 文字/矩形
    with ImageDrawManager(res_img) as image_manager:
        image_manager.add_text(
            Text(
                text=content_text.Test,
                position=(0,0),
                font_index=1,
                font_size=50,
                color=theme_text_color.TextThemeColor2,
                align='left',
                priority=10
            )
        )
        image_manager.add_text(
            Text(
                text=test_msg,
                position=(0,50),
                font_index=1,
                font_size=25,
                color=theme_text_color.TextThemeColor3,
                align='left',
                priority=10
            )
        )
        image_manager.execute_operations()
        res_img = image_manager.get_image()
        result = ImageHandler.save_image(res_img)
        return result
```
