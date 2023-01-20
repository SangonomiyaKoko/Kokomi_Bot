import os
from PIL import Image, ImageDraw, ImageFont
import json
import platform
import time
import gc


file_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
isWin = True if platform.system().lower() == 'windows' else False


class seach_name():
    def __init__(self) -> None:
        # 读取json数据
        temp_data = open(os.path.join(
            file_path, 'data', 'ship_name.json'), "r", encoding="utf-8")
        self.ship_name_data = json.load(temp_data)
        temp_data.close()

    def get_type(self, info_message: str):
        info_message = info_message.split()
        info_tier = []
        info_type = []
        info_nation = []
        tier_dict = {
            'T11': 11,
            'T10': 10,
            'T9': 9,
            'T8': 8,
            'T7': 7,
            'T6': 6,
            'T5': 5,
            'T4': 4,
            'T3': 3,
            'T2': 2,
            'T1': 1,
            '11': 11,
            '10': 10,
            '9': 9,
            '8': 8,
            '7': 7,
            '6': 6,
            '5': 5,
            '4': 4,
            '3': 3,
            '2': 2,
            '1': 1,
            'XI': 11,
            'X': 10,
            'IX': 9,
            'VIII': 8,
            'VII': 7,
            'VI': 6,
            'V': 5,
            'IV': 4,
            'III': 3,
            'II': 2,
            'I': 1
        }
        type_dict = {
            'CV': 'AirCarrier',
            'BB': 'Battleship',
            'CA': 'Cruiser',
            'CL': 'Cruiser',
            'DD': 'Destroyer',
            'SS': 'Submarine',
            '航母': 'AirCarrier',
            '战列': 'Battleship',
            '巡洋': 'Cruiser',
            '驱逐': 'Destroyer',
            '潜艇': 'Submarine'
        }
        nation_dict = {
            'USA': 'usa',
            'M': 'usa',
            '美国': 'usa',
            '美系': 'usa',
            'M系': 'usa',
            'JAPAN': 'japan',
            'R': 'japan',
            '日本': 'japan',
            'R系': 'japan',
            '日系': 'japan',
            'EUROPE': 'europe',
            'E': 'europe',
            '欧洲': 'europe',
            'E系': 'europe',
            'FRANCE': 'france',
            'F': 'france',
            'F系': 'france',
            '法国': 'france',
            'GERMANY': 'germany',
            'D': 'germany',
            'D系': 'germany',
            '德国': 'germany',
            'UK': 'uk',
            'Y': 'uk',
            'Y系': 'uk',
            '英国': 'uk',
            'PANASIA': 'pan_asia',
            'C': 'pan_asia',
            'C系': 'pan_asia',
            '泛亚': 'pan_asia',
            '亚州': 'pan_asia',
            'USSR': 'ussr',
            'S': 'ussr',
            'S系': 'ussr',
            '苏联': 'ussr',
            'ITALY': 'italy',
            'I': 'italy',
            'I系': 'italy',
            '意大利': 'italy',
            'NETHERLANDS': 'netherlands',
            'HL': 'netherlands',
            'HL系': 'netherlands',
            '荷兰': 'netherlands',
            'PANAMERICA': 'pan_america',
            'FM': 'pan_america',
            'FM系': 'pan_america',
            '泛美': 'pan_america',
            'COMMONWEALTH': 'commonwealth',
            'CW': 'commonwealth',
            'CW系': 'commonwealth',
            '泛英': 'commonwealth',
            '英联邦': 'commonwealth',
            '联邦': 'commonwealth',
            'SPAIN': 'spain',
            'X': 'spain',
            'X系': 'spain',
            '西班牙': 'spain'
        }
        for index in info_message:
            index = index.upper()
            # 依次判断输入的参数是否属于tier type nation中
            if index in tier_dict:
                info_tier.append(tier_dict[index])
                continue
            if index in type_dict:
                info_type.append(type_dict[index])
                continue
            if index in nation_dict:
                info_nation.append(nation_dict[index])
                continue
            # 参数均不属于tier type nation中，则判定非法参数，return error
            return {'status': 'error', 'message': 'Invalid Parameter', 'data': index}
        return {'status': 'ok', 'message': 'SUCCESS', 'data': (info_tier, info_type, info_nation)}

    def get_ship_id(self, info_type):
        ship_id_dict = {}   # 用于后续按等级排序
        ship_num = 0  # 统计一共有多少符条件船只
        for ship_id, ship_data in self.ship_name_data.items():
            # 遍历每一艘船只，提取数据判断是否符合条件，例如先判断船只等级是否在info_type[0]中（info_type[0]为[]表示无限制）
            if info_type[0] == [] or ship_data['tier'] in info_type[0]:
                if info_type[1] == [] or ship_data['type'] in info_type[1]:
                    if info_type[2] == [] or ship_data['nation'] in info_type[2]:
                        # 当船只等级，类型，国家均符合条件则写数据
                        if '[' in self.ship_name_data[ship_id]['ship_name']['en'] and ']' in self.ship_name_data[ship_id]['ship_name']['en']:
                            # 删除cw用船，例如[大和]
                            continue
                        ship_id_dict[ship_id] = ship_data['tier']
                        ship_num += 1
        # 用来按等级进行排序，通过dict的value来对key进行排序，例如{'a':1,'b':2,'c':3}
        ship_id_dict = sorted(ship_id_dict.items(),
                              key=lambda x: x[1], reverse=True)
        return (ship_id_dict, ship_num)

    def main(self, info_message):
        type_data = self.get_type(info_message)
        if type_data['status'] != 'ok':
            return type_data
        shipid_dict, shipid_num = self.get_ship_id(type_data['data'])
        if shipid_num > 199:
            return {'status': 'error', 'message': 'Too Much Ship'}
        if shipid_num == 0:
            return {'status': 'error', 'message': 'No Data'}
        img = Image.open(os.path.join(os.path.dirname(__file__), 'name.png'))
        draw = ImageDraw.Draw(img)
        font_path = os.path.join(file_path, 'data', 'SourceHanSansCN-Bold.TTF') if isWin else os.path.join(
            '/usr/share/fonts', 'SourceHanSansCN-Bold.TTF')
        font = ImageFont.truetype(font_path, 20)
        i = 1
        for ship_id, ship_tier in shipid_dict:

            xcoord = self.x_coord(str(i), font=font)
            draw.text((52-xcoord, 4+28*i), str(i), (0, 0, 0), font=font)
            xcoord = self.x_coord(
                str(self.ship_name_data[ship_id]['tier']), font=font)
            draw.text((167-xcoord, 4+28*i),
                      str(self.ship_name_data[ship_id]['tier']), (0, 0, 0), font=font)
            xcoord = self.x_coord(
                self.ship_name_data[ship_id]['type'], font=font)
            draw.text((292-xcoord, 4+28*i),
                      self.ship_name_data[ship_id]['type'], (0, 0, 0), font=font)
            xcoord = self.x_coord(
                self.ship_name_data[ship_id]['nation'], font=font)
            draw.text((417-xcoord, 4+28*i),
                      self.ship_name_data[ship_id]['nation'], (0, 0, 0), font=font)
            xcoord = self.x_coord(
                self.ship_name_data[ship_id]['ship_name']['zh_sg'], font=font)
            draw.text((584-xcoord, 4+28*i),
                      self.ship_name_data[ship_id]['ship_name']['zh_sg'], (0, 0, 0), font=font)
            xcoord = self.x_coord(
                self.ship_name_data[ship_id]['ship_name']['en'], font=font)
            draw.text((792-xcoord, 4+28*i),
                      self.ship_name_data[ship_id]['ship_name']['en'], (0, 0, 0), font=font)
            j = 0
            if self.ship_name_data[ship_id]['ship_name']['nick'] != []:
                for nickname in self.ship_name_data[ship_id]['ship_name']['nick']:
                    if j == 4:
                        break
                    xcoord = self.x_coord(nickname, font=font)
                    draw.text((996-xcoord+200*j, 4+28*i),
                              nickname, (0, 0, 0), font=font)
                    j += 1
            i += 1
        if i <= 10:
            y_coord = 308
        else:
            y_coord = 28*(i+1)
        img = img.crop((0, 0, 1696, y_coord))
        pic_path = os.path.join(file_path, 'temp', '5-{}.png'.format(
            png_name().generate_name(str(int(time.time()*100000)))))
        img.save(pic_path)
        img.close()
        del draw
        gc.collect()
        return {'status': 'ok', 'message': 'SUCCESS', 'img': pic_path}

    def x_coord(self, in_str: str, font: ImageFont.FreeTypeFont):
        x, y = font.getsize(in_str)
        out_coord = x/2
        return out_coord


class add_name():
    # 未完成
    def __init__(self) -> None:
        temp_data = open(os.path.join(
            file_path, 'data', 'ship_name.json'), "r", encoding="utf-8")
        self.ship_name_data = json.load(temp_data)
        temp_data.close()

    def name_format(self, in_str: str):
        in_str_list = in_str.split()
        in_str = None
        in_str = ''.join(in_str_list)
        en_list = {
            'a': ['à', 'á', 'â', 'ã', 'ä', 'å'],
            'e': ['è', 'é', 'ê', 'ë'],
            'i': ['ì', 'í', 'î', 'ï'],
            'o': ['ó', 'ö', 'ô', 'õ', 'ò', 'ō'],
            'u': ['ü', 'û', 'ú', 'ù', 'ū'],
            'y': ['ÿ', 'ý']
        }
        for en, lar in en_list.items():
            for index in lar:
                if index in in_str:
                    in_str = in_str.replace(index, en)
                if index.upper() in in_str:
                    in_str = in_str.replace(index.upper(), en.upper())
        re_str = ['_', '-', '·', '.', '\'']
        for index in re_str:
            if index in in_str:
                in_str = in_str.replace(index, '')
        in_str = in_str.lower()
        return in_str

    def seach_name(self, info):
        info = self.name_format(info)
        return_dict = {
            'status': 'ok',
            'ship_id': None
        }
        for ship_id, ship_data in self.ship_name_data.items():
            if info in ship_data['ship_name']['other']:
                return_dict['ship_id'] = ship_id
        return return_dict

    def main(self, standardname, nickname):
        ship_id_data = self.seach_name(standardname)
        if ship_id_data['ship_id'] == None:
            return {'status': 'error', 'message': 'Invalid Standardname'}
        ship_id = ship_id_data['ship_id']
        self.ship_name_data[ship_id]['ship_name']['nick'].append(nickname)
        self.ship_name_data[ship_id]['ship_name']['other'].append(
            self.name_format(nickname))
        with open(os.path.join(file_path, 'data', 'ship_name.json'), 'w', encoding='utf-8') as f:
            f.write(json.dumps(
                self.ship_name_data, ensure_ascii=False))
        f.close()
        gc.collect()
        return {'status': 'ok', 'message': 'SUCCESS'}


class png_name:
    def __init__(self) -> None:
        base = [
            0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x4A,
            0x4B, 0x4C, 0x4D, 0x4E, 0x4F, 0x50, 0x51, 0x52, 0x53, 0x54,
            0x55, 0x56, 0x57, 0x58, 0x59, 0x5A, 0x61, 0x62, 0x63, 0x64,
            0x65, 0x66, 0x67, 0x68, 0x69, 0x6A, 0x6B, 0x6C, 0x6D, 0x6E,
            0x6F, 0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78,
            0x79, 0x7A, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37,
            0x38, 0x39, 0x2B, 0x2F]
        self.base_changed = ''.join(chr(i) for i in base)

    def generate_name(self, inputs):
        # 图片名称
        bin_str = []
        for i in inputs:
            x = str(bin(ord(i))).replace('0b', '')
            bin_str.append('{:0>8}'.format(x))
        outputs = ""
        nums = 0
        while bin_str:
            temp_list = bin_str[:3]
            if (len(temp_list) != 3):
                nums = 3 - len(temp_list)
                while len(temp_list) < 3:
                    temp_list += ['0' * 8]
            temp_str = "".join(temp_list)
            temp_str_list = []
            for i in range(0, 4):
                temp_str_list.append(int(temp_str[i * 6:(i + 1) * 6], 2))
            if nums:
                temp_str_list = temp_str_list[0:4 - nums]
            for i in temp_str_list:
                outputs += self.base_changed[i]
            bin_str = bin_str[3:]
        outputs += nums * '='
        return outputs

    def get_png(self, inputs):
        bin_str = []
        for i in inputs:
            if i != '=':
                x = str(bin(self.base_changed.index(i))).replace('0b', '')
                bin_str.append('{:0>6}'.format(x))
        outputs = ""
        nums = inputs.count('=')
        while bin_str:
            temp_list = bin_str[:4]
            temp_str = "".join(temp_list)
            if (len(temp_str) % 8 != 0):
                temp_str = temp_str[0:-1 * nums * 2]
            for i in range(0, int(len(temp_str) / 8)):
                outputs += chr(int(temp_str[i * 8:(i + 1) * 8], 2))
            bin_str = bin_str[4:]
        return outputs


#print(seach_name().main('ss t10'))
