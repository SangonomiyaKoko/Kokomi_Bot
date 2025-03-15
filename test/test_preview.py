import time
import lmdb
import random
import os
from PIL import Image
from io import BytesIO

# 方法1：从大图中裁剪出100个小图片，并合并
def crop_and_merge_from_large_image(input_image_path, output_image_path):
    image = Image.open(input_image_path)
    width, height = image.size

    # 小图片的宽度和高度
    small_width = 360
    small_height = 80

    # 随机选择100个裁剪区域
    indices = random.sample(range(0, 900), 100)  # 选择100个索引

    # 合并裁剪出的图片
    small_images = []
    for idx in indices:
        row = idx // 10  # 获取行
        col = idx % 10  # 获取列

        left = col * small_width
        upper = row * small_height
        right = left + small_width
        lower = upper + small_height

        cropped_image = image.crop((left, upper, right, lower))
        small_images.append(cropped_image)

    # 计算合并后的新图片的尺寸
    merged_width = small_width * 10
    merged_height = small_height * 10

    # 创建一个新图片用于合并
    merged_image = Image.new("RGBA", (merged_width, merged_height))

    # 将小图片按行和列粘贴到新图上
    for i in range(10):
        for j in range(10):
            index = i * 10 + j
            merged_image.alpha_composite(small_images[index], (j * small_width, i * small_height))

    # 保存合并后的图片
    merged_image.save(output_image_path)

# 方法2：从文件夹读取100个小文件并合并
def read_and_merge_from_files(input_folder, output_image_path):
    # 随机选择100个文件
    files = os.listdir(input_folder)
    indices = random.sample(range(0, 900), 100)  # 随机选择100个索引

    # 合并图片
    small_images = []
    for idx in indices:
        file_name = f"index_{idx}.png"  # 根据文件名格式生成文件名
        file_path = os.path.join(input_folder, file_name)
        cropped_image = Image.open(file_path)
        small_images.append(cropped_image)

    # 计算合并后的新图片的尺寸
    small_width, small_height = small_images[0].size
    merged_width = small_width * 10
    merged_height = small_height * 10

    # 创建一个新图片用于合并
    merged_image = Image.new("RGBA", (merged_width, merged_height))

    # 将小图片按行和列粘贴到新图上
    for i in range(10):
        for j in range(10):
            index = i * 10 + j
            merged_image.alpha_composite(small_images[index], (j * small_width, i * small_height))

    # 保存合并后的图片
    merged_image.save(output_image_path)

# 方法3：使用LMDB批量加载文件并合并
def load_files_to_lmdb(input_folder, lmdb_path, batch_size):
    # 创建LMDB环境
    env = lmdb.open(lmdb_path, map_size=10**9)  # 设置适当的map_size以容纳所有数据
    with env.begin(write=True) as txn:
        # 将小文件加载到LMDB中
        for idx in range(900):  # 假设有900个小文件
            file_name = f"index_{idx}.png"
            file_path = os.path.join(input_folder, file_name)
            with open(file_path, 'rb') as f:
                txn.put(f"index_{idx}".encode(), f.read())  # 使用文件名作为key

    env.close()
    print(f"All files have been loaded into LMDB at {lmdb_path}")

# 从LMDB中批量读取文件并合并
def read_and_merge_from_lmdb(lmdb_path, output_image_path, batch_size):
    env = lmdb.open(lmdb_path)
    with env.begin() as txn:
        # 随机选择100个索引
        indices = random.sample(range(0, 900), 100)  # 随机选择100个索引

        small_images = []
        for idx in indices:
            key = f"index_{idx}".encode()
            image_data = txn.get(key)
            if image_data:
                # 将字节数据转换为图片
                img = Image.open(BytesIO(image_data))
                small_images.append(img)

        # 计算合并后的新图片的尺寸
        small_width, small_height = small_images[0].size
        merged_width = small_width * batch_size
        merged_height = small_height * batch_size

        # 创建一个新图片用于合并
        merged_image = Image.new("RGBA", (merged_width, merged_height))

        # 将小图片按行和列粘贴到新图上
        for i in range(10):
            for j in range(10):
                index = i * 10 + j
                merged_image.alpha_composite(small_images[index], (j * small_width, i * small_height))

        # 保存合并后的图片
        merged_image.save(output_image_path)

    env.close()

# 测试三种方法的时间
def compare_methods(input_image_path, input_folder, lmdb_path, output_image_path1, output_image_path2, output_image_path3, batch_size):
    # 测量方法1时间
    start_time = time.time()
    crop_and_merge_from_large_image(input_image_path, output_image_path1)
    method1_time = time.time() - start_time
    print(f"Method 1 (Crop from large image) took {method1_time:.4f} seconds")

    # 测量方法2时间
    start_time = time.time()
    read_and_merge_from_files(input_folder, output_image_path2)
    method2_time = time.time() - start_time
    print(f"Method 2 (Read from files) took {method2_time:.4f} seconds")

    # 测量方法3时间（LMDB）
    start_time = time.time()
    read_and_merge_from_lmdb(lmdb_path, output_image_path3, batch_size)
    method3_time = time.time() - start_time
    print(f"Method 3 (Read from LMDB) took {method3_time:.4f} seconds")

# 执行对比
input_image_path = r"F:\Kokomi_PJ_Bot\app\assets\components\ships\preview\ship_preview_cn.png"  # 大图的路径
input_folder = r"F:\Kokomi_PJ_Bot\temp\preview"  # 小文件存放的文件夹路径
lmdb_path = "file_data.lmdb"  # LMDB存储路径
output_image_path1 = "merged_from_large_image.png"  # 合并后的图片路径（方法1）
output_image_path2 = "merged_from_files.png"  # 合并后的图片路径（方法2）
output_image_path3 = "merged_from_lmdb.png"  # 合并后的图片路径（方法3）
batch_size = 400  # 设置批量读取的大小

# 加载文件到LMDB
load_files_to_lmdb(input_folder, lmdb_path, batch_size)

# 对比性能
compare_methods(input_image_path, input_folder, lmdb_path, output_image_path1, output_image_path2, output_image_path3, batch_size)


