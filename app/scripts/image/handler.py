import os
import time
import numpy as np
from typing import Tuple, Optional

from PIL import Image

from ..config import OUTPUT_DIR, bot_settings
from ..schemas import JSONResponse


class ImageHandler:
    """
    图像处理类，封装了常用的图像操作方法，涵盖了图像处理的基本操作

    主要方法:
        - new_image: 创建一张新的空白图片，支持 RGB 或 RGBA 模式
        - open_image: 打开指定路径的图片
        - resize_image: 调整图片大小，可以选择插值方法来控制缩放质量
        - save_image: 保存图片到指定目录，并返回保存的文件路径
        - composite_paste: 使用 paste 方法将前景图叠加到背景图上（适用于不带透明通道的图片）
        - composite_alpha: 使用 alpha_composite 方法将前景图叠加到背景图上（适用于带透明通道的图片）
        - composite_numpy: 使用 NumPy 进行加速叠加，支持带或不带透明通道的图片
    """

    @staticmethod
    def new_image(
        size: Tuple[int, int], 
        color: Tuple[int, int, int, int] = (255, 255, 255, 255)
    ) -> Image.Image:
        """创建新的空白图片，支持 RGB 或 RGBA 模式

        参数:
            size (Tuple[int, int]): 图片尺寸 (宽, 高)
            color (Tuple[int, int, int, int]): 背景颜色 (R, G, B) 或 (R, G, B, A)，默认为白色不透明

        返回:
            Image.Image: 创建的图片对象
        """
        mode = "RGBA" if len(color) == 4 else "RGB"
        return Image.new(mode, size, color)


    @staticmethod
    def open_image(path: str) -> Image.Image | dict:
        """打开图片文件

        注意，如果没有文件会抛出异常，请根据实际功能自行判断是否需要捕获

        参数:
            path (str): 图片文件路径

        返回:
            Image.Image: 加载的图片对象
        """
        return Image.open(path)

    @staticmethod
    def resize_image(
        img: Image.Image, 
        size: Tuple[int, int], 
        resample: Optional[Image.Resampling] = None
    ) -> Image.Image:
        """调整图片大小。

        ressample如果没有指定，默认插值是根据图片模式决定

        如果是 BGR; 模式，使用 NEAREST，否则，使用 BICUBIC 
        
        注: BGR 模式一般用于 OpenCV 兼容格式

        参数:
            img (Image.Image): 需要调整的图片对象
            size (Tuple[int, int]): 目标尺寸 (宽, 高)
            resample (int): 插值方法，决定缩放质量

                可选插值方法：
                - Image.NEAREST  ：最近邻插值，速度最快，质量最低，适用于像素风格图片
                - Image.BOX      ：盒滤波，适用于缩小图像，效果较平滑
                - Image.BILINEAR ：双线性插值，计算4个相邻像素的加权平均，质量适中，适用于一般缩放
                - Image.BICUBIC  ：双三次插值，计算16个相邻像素，质量较好，适用于放大图像。
                - Image.LANCZOS  ：Lanczos滤波，适用于缩小图像，边缘锐利，细节保留较好（推荐）
                - Image.HAMMING  ：Hamming滤波，适用于小比例缩放，较少使用

        返回:
            Image.Image: 调整大小后的图片对象。
        """
        return img.resize(size=size, resample=resample)
    
    @staticmethod
    def save_image(img: Image.Image) -> dict:
        """保存图片到指定目录，并返回保存的文件路径

        参数:
            img (Image.Image): 要保存的图片对象

        返回:
            dict: 包含状态信息和图片路径的字典
        """
        try:
            file_name = os.path.join(OUTPUT_DIR, f"{int(time.time() * 1000)}." + bot_settings.RETURN_PIC_TYPE)
            img.save(file_name)
            return {
                'status': 'ok',
                'code': 1000,
                'message': 'Success',
                'data': {
                    'img': file_name
                }
            }
        except Image.DecompressionBombError:
            return JSONResponse.API_10009_ImageTooLarge  # 返回图片过大错误
        except Exception:
            return JSONResponse.API_10007_SaveImageFailed  # 其他异常返回通用保存失败错误
        finally:
            img.close()

    @staticmethod
    def composite_paste(
        bg: Image.Image, 
        fg: Image.Image, 
        position: Tuple[int, int] = (0, 0)
    ) -> Image.Image:
        """使用 paste 方法叠加图片（适用于不带透明通道的图片）

        不带有alpha通道图片叠加，如有会丢失alpha通道的信息
        
        参数:
            bg (Image.Image): 背景图片
            fg (Image.Image): 需要叠加的前景图片
            position (tuple): 叠加的位置，默认为 (0, 0)

        返回:
            Image.Image: 叠加后的图片。
        """
        # 叠加图片
        bg.paste(fg, position)
        return bg

    @staticmethod
    def composite_alpha(
        bg: Image.Image, 
        fg: Image.Image, 
        position: Tuple[int, int] = (0, 0)
    ) -> Image.Image:
        """使用 alpha_composite 方法叠加两张图片（适用于带透明通道的图片）
        
        参数:
            bg (Image.Image): 背景图片
            fg (Image.Image): 需要叠加的前景图片
            position (tuple): 前景图片放置的位置，默认为 (0, 0)

        返回:
            Image.Image: 叠加后的图片
        """
        if fg.mode != 'RGBA':
            # 检查顶图是否有 alpha 通道
            fg.convert("RGBA")
        # 叠加图片
        bg.alpha_composite(fg, position)
        return bg

    @staticmethod
    def composite_numpy(
        bg: Image.Image, 
        fg: Image.Image, 
        position: Tuple[int, int] = (0, 0)
    ) -> Image.Image:
        """使用 NumPy 进行加速叠加（支持带或不带透明通道的图片）

        该方法虽然可以快速完成叠加，但是效果较差，一般只用大图片叠加或者其他对精度需求不大的任务
    
        参数:
            bg (Image.Image): 背景图片
            fg (Image.Image): 需要叠加的前景图片
            position (tuple): 叠加的位置，默认为 (0, 0)

        返回:
            Image.Image: 叠加后的图片
        """
        # 确保图片为 RGBA
        bg = bg.convert("RGBA")
        fg = fg.convert("RGBA")

        # 转换为 NumPy 数组
        bg_arr = np.array(bg, dtype=np.uint8)
        fg_arr = np.array(fg, dtype=np.uint8)

        # 获取叠加区域
        x, y = position
        bh, bw = bg.size
        fh, fw = fg.size

        # 限制叠加范围，防止越界
        if x + fw > bw:
            fw = bw - x
        if y + fh > bh:
            fh = bh - y

        # 提取 RGBA 通道
        fg_rgb = fg_arr[:fh, :fw, :3]
        fg_alpha = fg_arr[:fh, :fw, 3] / 255.0  # 归一化 alpha

        bg_rgb = bg_arr[y:y+fh, x:x+fw, :3]
        bg_alpha = bg_arr[y:y+fh, x:x+fw, 3] / 255.0

        # 计算新的 alpha 通道
        out_alpha = fg_alpha + bg_alpha * (1 - fg_alpha)
        out_rgb = (fg_rgb * fg_alpha[:, :, None] + bg_rgb * bg_alpha[:, :, None] * (1 - fg_alpha[:, :, None])) / out_alpha[:, :, None]

        # 组合结果
        bg_arr[y:y+fh, x:x+fw, :3] = np.clip(out_rgb, 0, 255).astype(np.uint8)
        bg_arr[y:y+fh, x:x+fw, 3] = np.clip(out_alpha * 255, 0, 255).astype(np.uint8)

        return Image.fromarray(bg_arr, "RGBA")
