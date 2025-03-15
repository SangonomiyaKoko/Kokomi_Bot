import os
import lmdb
from PIL import Image
import io
from ..config import DATA_DIR, ASSETS_DIR

class ImageDB:
    def __init__(self):
        """
        初始化函数，从给定的文件夹读取文件，将文件存储到 LMDB 数据库中
        """
        self.folder_path = os.path.join(ASSETS_DIR)
        self.db_path = os.path.join(DATA_DIR, 'image.lmab')
        # 创建或打开一个 LMDB 数据库
        self.env = lmdb.open(self.db_path, map_size=100 * 1024 * 1024)  # 1GB 的最大数据库大小
        self._load_existing_data()

    def _load_existing_data(self):
        """
        从文件夹读取文件并加载到 LMDB 数据库中
        """
        with self.env.begin(write=True) as txn:
            for filename in os.listdir(self.folder_path):
                file_path = os.path.join(self.folder_path, filename)
                if os.path.isfile(file_path):
                    # 读取图片并转换为二进制数据
                    with open(file_path, 'rb') as f:
                        img_data = f.read()
                    # 存储到 LMDB 数据库，使用文件名作为键
                    txn.put(filename.encode('utf-8'), img_data)

    def refresh(self):
        """
        刷新函数，检查文件夹是否有新增文件，有则写入
        """
        existing_files = set(self._get_existing_files())
        current_files = set(os.listdir(self.folder_path))
        new_files = current_files - existing_files

        if new_files:
            with self.env.begin(write=True) as txn:
                for filename in new_files:
                    file_path = os.path.join(self.folder_path, filename)
                    if os.path.isfile(file_path):
                        # 读取新的图片并转换为二进制数据
                        with open(file_path, 'rb') as f:
                            img_data = f.read()
                        # 存储到 LMDB 数据库，使用文件名作为键
                        txn.put(filename.encode('utf-8'), img_data)

    def _get_existing_files(self):
        """
        获取数据库中已存在的文件列表
        """
        with self.env.begin() as txn:
            return [key.decode('utf-8') for key, _ in txn.cursor()]

    def read_images(self, image_names: list):
        """
        根据给定的文件名列表，返回相应的图片
        """
        images = {}
        with self.env.begin() as txn:
            for image_name in image_names:
                image_data = txn.get(image_name.encode('utf-8'))
                if image_data:
                    images[image_name] = Image.open(io.BytesIO(image_data))
                else:
                    images[image_name] = None
        return images
