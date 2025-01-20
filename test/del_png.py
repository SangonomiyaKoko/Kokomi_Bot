import os
import glob

def delete_images(folder_path):
    # 查找文件夹下所有 .png 和 .webp 文件
    png_files = glob.glob(os.path.join(folder_path, "*.png"))
    webp_files = glob.glob(os.path.join(folder_path, "*.webp"))
    
    # 合并文件列表
    all_files = png_files + webp_files

    # 删除文件
    for file in all_files:
        try:
            os.remove(file)
            print(f"删除文件: {file}")
        except Exception as e:
            print(f"删除文件 {file} 失败: {e}")

# 调用函数
folder_path = r"F:\Kokomi_PJ_Bot\output"
delete_images(folder_path)
