class DataLoader:
    # 存储单例实例
    _instance = None

    # 用于模拟加载的数据（例如从文件、数据库、外部API等加载）
    data = {}

    def __new__(cls, *args, **kwargs):
        # 如果实例还不存在，创建实例
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # 避免重复加载数据
        if not hasattr(self, 'initialized'):
            self.load_data()
            self.initialized = True

    def load_data(self):
        """模拟加载数据的过程"""
        print("Loading data...")
        self.data = {
            'user_1': {'name': 'Alice', 'age': 30},
            'user_2': {'name': 'Bob', 'age': 25},
            'user_3': {'name': 'Charlie', 'age': 35}
        }

    def get_data(self, key: str):
        """通过key获取数据"""
        return self.data.get(key, 'Data not found')

    def get_all_data(self):
        """返回所有数据"""
        return self.data


# 测试单例模式加载数据
data_loader1 = DataLoader()
data_loader2 = DataLoader()

# 验证两个对象是同一个实例
print(data_loader1 is data_loader2)  # 输出：True

# 获取特定用户的数据
print(data_loader1.get_data('user_1'))  # 输出：{'name': 'Alice', 'age': 30}
print(data_loader2.get_data('user_2'))  # 输出：{'name': 'Bob', 'age': 25}

# 获取所有数据
print(data_loader1.get_all_data())
# 输出：{'user_1': {'name': 'Alice', 'age': 30}, 'user_2': {'name': 'Bob', 'age': 25}, 'user_3': {'name': 'Charlie', 'age': 35}}
