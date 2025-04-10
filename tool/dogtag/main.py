# 此处是用于更新用户徽章的工具，需要配合解压工具使用

import os
import shutil
import json
'''
接口返回值
"dog_tag": {
    "texture_id": 0,                # 背景纹理
    "symbol_id": 4079963056,        # 符号
    "border_color_id": 0,           # 镶边颜色
    "background_color_id": 0,       # 背景颜色
    "background_id": 4240427952     # 背景
    }

id -> color
"border_color":{
    "4293348272": "0x282828",
    "4292299696": "0x23325d",
    "4291251120": "0x15668c",
    "4290202544": "0x213f47",
    "4289153968": "0x3a4a23",
    "4288105392": "0x553b16",
    "4287056816": "0x6d4f29",
    "4286008240": "0x8a763a",
    "4284959664": "0xd9d9d9",
    "4283911088": "0xf3c612",
    "4282862512": "0xcb7208",
    "4281813936": "0xa73a1c",
    "4280765360": "0xa32323",
    "4279716784": "0x7f1919",
    "4278668208": "0x382c4f"
}

"background_color":{
    "4293577648": "0x252525",
    "4292529072": "0x25355d",
    "4291480496": "0x2b6e91",
    "4290431920": "0x22454a",
    "4289383344": "0x3f4d2c",
    "4288334768": "0x8f7e44",
    "4287286192": "0x8b6932",

    "4286237616": "0xc9c9c9",
    "4285189040": "0xcfa40f",
    "4284140464": "0xd98815",
    "4283091888": "0xb74522",
    "4282043312": "0xad1d1d",
    "4280994736": "0x771d27",
    "4279946160": "0x3b2f4e"
}

'''

default_list = ['PCNA001', 'PCNA002', 'PCNA003', 'PCNA004', 'PCNA005', 'PCNA006', 'PCNA007', 'PCNA008', 'PCNA009', 'default_PCNA.png', 'default_PCNB.png']
all_list = ['PCNA001', 'PCNA002', 'PCNA003', 'PCNA004', 'PCNA005', 'PCNA006', 'PCNA007', 'PCNA008', 'PCNA009', 'PCNT001', 'PCNT002', 'PCNT003', 'PCNT004']

# 指定服务器及解包数据地址
server = 'lesta'

bot_file_path = r'F:\Kokomi_PJ_Bot'
if server == 'wg':
    unpack_file_path = r'E:\a_wws_unpack\as_unpack'
    op = 'WarGaming'
else:
    unpack_file_path = r'E:\a_wws_unpack\ru_unpack'
    op = 'LestaGame'


def find_new_keys(old_data, new_data):
    new_items = {
        key: new_data[key]
        for key in new_data
        if key not in old_data
    }
    for k, v in new_items.items():
        print(f'新增 "{k}": "{v}"')
        src = os.path.join(dog_tag_dir, f'{v}.png')
        dst = os.path.join(bot_file_path, r'app\assets\components\insignias\symbol', op, f'{v}.png')
        shutil.copy(src, dst)

if __name__ == '__main__':
    # wg数据处理，获取所有的图片
    dog_tag_dir = os.path.join(unpack_file_path, 'gui', 'dogTags', 'big')
    dog_tag_list = os.listdir(dog_tag_dir)
    dog_tag_list = [item for item in dog_tag_list if item not in default_list]
    for index in dog_tag_list:
        if '.png' in index:
            index = index.replace('.png','')
        all_list.append(index)
    # 从游戏解包数据中读取数据
    new_josn_data = {}
    wg_data = json.load(
        open(
            os.path.join(unpack_file_path, 'GameParams-0.json'), 
            "r", 
            encoding="utf-8"
        )
    )
    for index in all_list:
        dogtag_id = wg_data[index]['id']
        new_josn_data[str(dogtag_id)] = index
    
    json_file_path = os.path.join(bot_file_path, r'app\assets\json', op, 'dog_tags.json')

    with open(json_file_path, 'r', encoding='utf-8') as f:
        old_json_data = json.load(f)

    find_new_keys(old_json_data, new_josn_data)

    with open(json_file_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(new_josn_data, ensure_ascii=False))
    f.close()
