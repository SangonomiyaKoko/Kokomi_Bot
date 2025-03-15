# 此处是用于更新用户徽章的工具，需要配合解压工具使用

import os
import shutil
import json
file_path = os.path.dirname(__file__)
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
# E:\a_wws_unpack\as_unpack\gui\dogTags\big
default_list = ['PCNA001', 'PCNA002', 'PCNA003', 'PCNA004', 'PCNA005', 'PCNA006', 'PCNA007', 'PCNA008', 'PCNA009', 'default_PCNA.png', 'default_PCNB.png']
all_list = ['PCNA001', 'PCNA002', 'PCNA003', 'PCNA004', 'PCNA005', 'PCNA006', 'PCNA007', 'PCNA008', 'PCNA009', 'PCNT001', 'PCNT002', 'PCNT003', 'PCNT004']

wg_file = os.path.join(file_path,'as_unpack','gui','dogTags','big')
wg_list = os.listdir(wg_file)
wg_list = [item for item in wg_list if item not in default_list]
wg_file_list = []
for index in wg_list:
    if '.png' in index:
        index = index.replace('.png','')
    all_list.append(index)
result = {}
wg_data = json.load(
    open(
        os.path.join(file_path, 'as_unpack', 'GameParams-0.json'), 
        "r", 
        encoding="utf-8"
    )
)
for index in all_list:
    dogtag_id = wg_data[index]['id']
    result[dogtag_id] = index

with open(os.path.join(file_path, 'dog_tags_wg.json'), 'w', encoding='utf-8') as f:
    f.write(json.dumps(result, ensure_ascii=False))
f.close()




default_list = ['PCNA001', 'PCNA002', 'PCNA003', 'PCNA004', 'PCNA005', 'PCNA006', 'PCNA007', 'PCNA008', 'PCNA009', 'default_PCNA.png', 'default_PCNB.png']
all_list = ['PCNA001', 'PCNA002', 'PCNA003', 'PCNA004', 'PCNA005', 'PCNA006', 'PCNA007', 'PCNA008', 'PCNA009', 'PCNT001', 'PCNT002', 'PCNT003', 'PCNT004']

ru_file = os.path.join(file_path,'ru_unpack','gui','dogTags','big')
ru_list = os.listdir(ru_file)
ru_list = [item for item in ru_list if item not in default_list]
ru_file_list = []
for index in ru_list:
    if '.png' in index:
        index = index.replace('.png','')
    all_list.append(index)
result = {}
ru_data = json.load(
    open(
        os.path.join(file_path, 'ru_unpack', 'GameParams-0.json'), 
        "r", 
        encoding="utf-8"
    )
)
for index in all_list:
    dogtag_id = ru_data[index]['id']
    result[dogtag_id] = index

with open(os.path.join(file_path, 'dog_tags_lesta.json'), 'w', encoding='utf-8') as f:
    f.write(json.dumps(result, ensure_ascii=False))
f.close()