from PIL import Image
import os

def create_custom_gif(image_folder, overlay_image_path, output_gif_path, frame_count, canvas_size, background_color, resize_factor, fps):
    """
    按要求处理图片并生成 GIF 动画
    :param image_folder: 主图片的文件夹路径
    :param overlay_image_path: 叠加图片的路径
    :param output_gif_path: 输出 GIF 文件路径
    :param frame_count: 总帧数
    :param canvas_size: 背景画布的大小 (width, height)
    :param background_color: 背景颜色，例如 "#F8F9FB"
    :param resize_factor: 最终缩放比例（例如 0.5 表示缩小一半）
    :param fps: 每秒帧数
    """
    # 初始化参数
    width, height = canvas_size
    frame_duration = int(1000 / fps)  # 每帧持续时间（毫秒）

    # 获取所有帧图片路径
    frame_files = [os.path.join(image_folder, f"image_{str(i).zfill(3)}.png") for i in range(frame_count)]

    # 检查路径是否存在
    if not os.path.exists(overlay_image_path):
        raise FileNotFoundError(f"叠加图片 {overlay_image_path} 不存在")
    for frame_file in frame_files:
        if not os.path.exists(frame_file):
            raise FileNotFoundError(f"帧图片 {frame_file} 不存在")

    # 打开叠加图片
    overlay_image = Image.open(overlay_image_path).convert("RGBA")
    overlay_image = overlay_image.resize((1214,1675), Image.LANCZOS)

    # 存储处理好的帧
    frames = []
    i = 0
    for frame_file in frame_files:
        # 创建背景画布
        canvas = Image.new("RGBA", (width, height), background_color)

        # 打开并裁剪帧图片
        frame_image = Image.open(frame_file).convert("RGBA")
        frame_image = frame_image.resize((1294, 1785), Image.LANCZOS)
        frame_image = frame_image.crop((40, 55, 40+1214, 55+1675))


        # 叠加帧图片到画布
        canvas.alpha_composite(frame_image, (0, 0))

        # 叠加叠加图片
        canvas.alpha_composite(overlay_image, (0, 0))

        # 缩小画布尺寸
        resized_canvas = canvas.resize((int(width * resize_factor), int(height * resize_factor)), Image.LANCZOS)

        # 添加到帧列表
        frames.append(resized_canvas)
        print(f"处理第 {i} 帧")
        i += 1

    # 保存为 GIF
    frames[0].save(
        output_gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=frame_duration,
        loop=0
    )
    print(f"GIF 动画已成功生成: {output_gif_path}")
    

# 参数设置
create_custom_gif(
    image_folder=r"C:\Users\MaoYu\Desktop\fire",  # 主图片路径
    overlay_image_path=r"C:\Users\MaoYu\Desktop\fire\image.png",  # 叠加图片路径
    output_gif_path=r"C:\Users\MaoYu\Desktop\output.gif",  # 输出 GIF 路径
    frame_count=168,  # 总帧数
    canvas_size=(1214, 1675),  # 背景画布大小
    background_color="#F8F9FB",  # 背景颜色
    resize_factor=0.5,  # 缩小比例
    fps=15  # 每秒播放帧数
)
