import datetime
import os
import gzip
import json
import httpx
import threading
import asyncio
import time
from datetime import date
#import psutil
from PIL import Image, ImageDraw, ImageFont
import platform
import gc
import sys
import matplotlib.pyplot as plt
import yaml

isWin = True if platform.system().lower() == 'windows' else False
file_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
f = open(os.path.join(file_path, 'config.yaml'))
config_data = yaml.load(f.read(), Loader=yaml.FullLoader)
DATABASE_PATH = config_data['DatabaseConfig']['Database_path']
f.close()


class update:
    '''Update user data'''

    def __init__(self, data) -> None:
        self.account_id = data[0]
        self.server = data[1]

    def server_url(self, server: str) -> str:
        '''Return the domain name of the server's website'''
        url_list = {
            'asia': 'http://vortex.worldofwarships.asia',
            'eu': 'http://vortex.worldofwarships.eu',
            'na': 'http://vortex.worldofwarships.com',
            'ru': 'http://vortex.korabli.su',
            'cn': 'http://vortex.wowsgame.cn'
        }
        return url_list[server]

    def error_msg(self, msg: list) -> None:
        ship_data['status'] = msg[0]
        ship_data['message'] = msg[1]
        ship_data['error'] = msg[2]
        ship_data['params'] = msg[3]

    async def user_info(self) -> dict:
        try:
            global ship_data
            ship_data = {
                'status': 'ok',
                'message': 'SUCCESS',
                'data': {
                    'user': {
                        'hidden': False,
                        'value': True,
                        'nickname': None
                    },
                    'info': {},
                    'ship': {
                        'pvp': {},
                        'pvp_solo': {},
                        'pvp_div2': {},
                        'pvp_div3': {},
                        'rank_solo': {}
                    },
                    'achievements': {},
                    'clans': {}
                }
            }
            # 写入user和info数据，并判断数据是否存在或者是否隐藏战绩
            user_data = await self.request_user_data()
            if user_data['status'] == 'error' and user_data['message'] == 'Network Error':
                ship_data['data']['user']['value'] = False
                ship_data['status'] = 'error'
                ship_data['message'] = 'Network Error'
            elif user_data['status'] != 'ok':
                ship_data['data']['user']['value'] = False
                ship_data['status'] = 'error'
                ship_data['error'] = user_data['error']
                ship_data['message'] = 'NOT FOUND'
                return ship_data
            ship_data['data']['user']['nickname'] = user_data['data'][str(
                self.account_id)]['name']
            if 'hidden_profile' in user_data['data'][str(self.account_id)]:
                ship_data['data']['user']['hidden'] = True

                return ship_data
            if user_data['data'][str(self.account_id)]['statistics'] == {}:
                return ship_data

            ship_data['data']['info'] = user_data['data'][str(
                self.account_id)]['statistics']['basic']

            # 写入其他数据
            thread = []
            for index in range(0, 7):
                thread.append(threading.Thread(
                    target=self.user2, args=(index,)))
            for t in thread:
                t.start()
            for t in thread:
                t.join()
            ship_data['data']['ship'] = self.data(ship_data['data']['ship'])
            ship_data['data']['achievements'] = self.achieve(
                ship_data['data']['achievements'])
            return ship_data
        except Exception as e:
            return {
                'status': 'error',
                'message': 'UNEXPECTED ERROR',
                'error': str(e),
                'data': {
                    'user': {
                        'hidden': False,
                        'nickname': None,
                    },
                    'info': {},
                    'ship': {},
                    'achievements': {},
                    'clans': {}
                }
            }

    def user2(self, request_number) -> None:
        asyncio.run(self.request_data(request_number))

    async def request_user_data(self) -> dict:
        url = self.server_url(self.server) + \
            '/api/accounts/{}/'.format(self.account_id)
        async with httpx.AsyncClient() as client:
            res = await client.get(url, timeout=3)
            if res.status_code != 200 and res.status_code != 404:
                return {'status': 'error', 'message': 'Network Error'}
            result = res.json()
            return result

    async def request_data(self, request_number) -> dict:
        '''Resquest and get original statistics data'''
        url_list = [
            '/api/accounts/{}/ships/pvp/',
            '/api/accounts/{}/ships/pvp_solo/',
            '/api/accounts/{}/ships/pvp_div2/',
            '/api/accounts/{}/ships/pvp_div3/',
            '/api/accounts/{}/ships/rank_solo/',
            '/api/accounts/{}/clans/',
            '/api/accounts/{}/achievements/'
        ]
        async with httpx.AsyncClient() as client:
            try:
                url = self.server_url(self.server) + \
                    url_list[request_number].format(self.account_id)

                res = await client.get(url, timeout=3)
                result = res.json()

                if res.status_code != 200:
                    self.error_msg(['error', 'NETWORK ERROR',
                                    'Status Code:'+str(res.status_code), url])
                    return None
            except:
                self.error_msg(
                    ['error', 'NETWORK ERROR', 'httpx connect error', url])
            if request_number == 5 and 'data' not in result:
                ship_data['data']['clans'] = {'clan': {}}
                return None
            if 'data' not in result:
                self.error_msg(['error', 'NETWORK ERROR',
                               'httpx connect error', url])
                return None
            battles_type_list = ['pvp', 'pvp_solo',
                                 'pvp_div2', 'pvp_div3', 'rank_solo']
            original_data = result['data']
            if request_number <= 4:
                ship_data['data']['ship'][battles_type_list[request_number]] = original_data[str(
                    self.account_id)]['statistics']
            elif request_number == 5:
                ship_data['data']['clans'] = original_data
            else:
                ship_data['data']['achievements'] = original_data[str(
                    self.account_id)]['statistics']['achievements']

    def data(self, ships: dict):
        res_data = {}
        if ships['pvp'] != {} or ships['rank_solo'] != {}:
            for types in ['pvp', 'pvp_solo', 'pvp_div2', 'pvp_div3', 'rank_solo']:
                for ship_id, datas in ships[types].items():
                    if types == 'pvp':
                        res_data[ship_id] = {
                            'pvp': {},
                            'pvp_solo': {},
                            'pvp_div2': {},
                            'pvp_div3': {},
                            'rank_solo': {}
                        }
                    del_list = [
                        'battles_count_512',
                        'battles_count_510',
                        'premium_exp',
                        'dropped_capture_points',
                        'damage_dealt_to_buildings',
                        'battles_count_0711',
                        'capture_points',
                        'max_suppressions_count',
                        'suppressions_count',
                        'max_damage_dealt_to_buildings',
                        'max_premium_exp',
                        'battles_count_078',
                        'battles_count_0910'
                    ]
                    if datas[types] != {}:
                        for del_index in del_list:
                            del datas[types][del_index]
                    res_data[ship_id][types] = datas[types]
        for ship_id, data in res_data.items():
            if data == {'pvp': {}, 'pvp_solo': {}, 'pvp_div2': {}, 'pvp_div3': {}, 'rank_solo': {}}:
                res_data[ship_id] = {}
        return res_data

    def achieve(self, ships: dict):
        res_data = {}
        if ships != {}:
            achievement_dict = {
                4277330864: 'PCH016_FirstBlood',
                4289913776: 'PCH004_Dreadnought',
                4282573744: 'PCH011_InstantKill',
                4290962352: 'PCH003_MainCaliber',
                4287816624: 'PCH006_Withering',
                4288865200: 'PCH005_Support',
                4269990832: 'PCH023_Warrior',
                4283622320: 'PCH010_Retribution',
                4276282288: 'PCH017_Fireproof',
                4281525168: 'PCH012_Arsonist',
                4273136560: 'PCH020_ATBACaliber',
                4293059504: 'PCH001_DoubleKill',
                4111655856: 'PCH174_AirDefenseExpert',
                4274185136: 'PCH019_Detonated',
                4279428016: 'PCH014_Headbutt',
                4292010928: 'PCH002_OneSoldierInTheField',
                4275233712: 'PCH018_Unsinkable',
                3879920560: 'PCH395_CombatRecon',

                3910329264: 'PCH366_Warrior_Squad',
                3909280688: 'PCH367_Support_Squad',
                3908232112: 'PCH368_Frag_Squad',
                3912426416: 'PCH364_MainCaliber_Squad',
                3911377840: 'PCH365_ClassDestroy_Squad'
            }
            ''',

                4004701104: 'PCH276_JollyRogerBronze',
                4003652528: 'PCH277_JollyRogerSilver',
                4050838448: 'PCH232_JollyRoger',
                3910329264: 'PCH366_Warrior_Squad',
                3909280688: 'PCH367_Support_Squad',
                3908232112: 'PCH368_Frag_Squad',
                3912426416: 'PCH364_MainCaliber_Squad',
                3911377840: 'PCH365_ClassDestroy_Squad'
                4125287344:'PCH161_CLAN_LEAGUE_4',
                4126335920:'PCH160_CLAN_LEAGUE_3',
                4127384496:'PCH159_CLAN_LEAGUE_2',
                4128433072:'PCH158_CLAN_LEAGUE_1',
            '''
            for id, name in achievement_dict.items():
                if str(id) in ships:
                    res_data[name] = ships[str(
                        id)]['count']
            return res_data


class personal_rating:
    '''Return pr'''

    def __init__(self) -> None:
        server_file_path = os.path.join(file_path, 'data', 'server.json')
        ship_server_data = open(
            server_file_path, "r", encoding="utf-8")
        result = json.load(ship_server_data)
        ship_server_data.close()

        self.number_data = result

    def number_pr(self, ship_id, data) -> dict:
        battles_count = data['battles_count']
        average_damage_dealt = data['damage_dealt']/battles_count
        average_wins = data['wins']/battles_count*100
        average_kd = data['frags']/battles_count
        ss_server = {
            '3751196368': {'win_rate': 49.58, 'average_damage_dealt': 28475.514944, 'average_frags': 0.625831},
            '4074157872': {'win_rate': 49.64, 'average_damage_dealt': 41468.532263, 'average_frags': 0.577373},
            '4076255024': {'win_rate': 50.36, 'average_damage_dealt': 26760.805256, 'average_frags': 0.498884},
            '4078352176': {'win_rate': 50.44, 'average_damage_dealt': 23485.309381, 'average_frags': 0.585853},
            '3761681872': {'win_rate': 49.96, 'average_damage_dealt': 25481.529185, 'average_frags': 0.444348},
            '4074158064': {'win_rate': 51.65, 'average_damage_dealt': 42011.532957, 'average_frags': 0.704729},
            '4076255216': {'win_rate': 51.54, 'average_damage_dealt': 28279.428878, 'average_frags': 0.561205},
            '4078352368': {'win_rate': 49.75, 'average_damage_dealt': 20297.190654, 'average_frags': 0.531933}
        }
        if str(ship_id) not in self.number_data['data'] and str(ship_id) not in ss_server:
            return (0, 0)
        if str(ship_id) not in self.number_data['data'] and str(ship_id) in ss_server:
            server_damage_dealt = ss_server[str(
                ship_id)]['average_damage_dealt']
            server_frags = ss_server[str(ship_id)]['average_frags']
            server_wins = ss_server[str(ship_id)]['win_rate']
        else:
            if self.number_data['data'][str(ship_id)] == []:
                return (0, 0)
            server_damage_dealt = self.number_data['data'][str(
                ship_id)]['average_damage_dealt']
            server_frags = self.number_data['data'][str(
                ship_id)]['average_frags']
            server_wins = self.number_data['data'][str(ship_id)]['win_rate']
        if average_damage_dealt > server_damage_dealt*0.4:
            n_damage = (average_damage_dealt-server_damage_dealt *
                        0.4)/(server_damage_dealt*0.6)
        else:
            n_damage = 0
        if average_wins > server_wins*0.7:
            n_win_rate = (average_wins-server_wins*0.7) / \
                (server_wins*0.3)
        else:
            n_win_rate = 0
        if average_kd > server_frags*0.1:
            n_kd = (average_kd-server_frags*0.1)/(server_frags*0.9)
        else:
            n_kd = 0
        pr = 700*n_damage+300*n_kd+150*n_win_rate
        return (battles_count, round(pr*battles_count, 6))


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


class calendar:
    def __init__(self, data):
        self.account_id = data[0]
        self.server = data[1]
        self.date_list = []
        self.res_data = {}
        ship_name_data = open(os.path.join(
            file_path, 'data', 'ship_name.json'), "r", encoding="utf-8")
        self.ship_info = json.load(ship_name_data)
        ship_name_data.close()

    def get_list(self, date):
        return datetime.datetime.strptime(date, "%Y-%m-%d").timestamp()

    def calerdar_data(self):
        file_name_list = os.listdir(os.path.join(
            DATABASE_PATH, self.server, str(self.account_id)))
        file_date_list = []
        for i in file_name_list:
            file_date_list.append(i.replace('.txt', ''))
        file_date_list = sorted(
            file_date_list, key=lambda date: self.get_list(date))
        limit_len = 70
        if len(file_date_list) > limit_len:
            file_date_list = file_date_list[len(file_date_list)-limit_len:]
        self.date_list = file_date_list
        for date_name in file_date_list:
            self.res_data[date_name] = {}
        thread = []
        for index in range(0, 7):
            thread.append(threading.Thread(
                target=self.read_file, args=(index,)))
        for t in thread:
            t.start()
        for t in thread:
            t.join()
        return self.res_data

    def read_file(self, index_num):
        i = 0
        while True:
            file_index_num = i * 7 + index_num
            if len(self.date_list) <= file_index_num:
                break
            byte_data = open(os.path.join(DATABASE_PATH, self.server, str(
                self.account_id), (self.date_list[file_index_num]+'.txt')), 'rb')
            db_data = eval(
                str(gzip.decompress(byte_data.read()), encoding="utf-8"))
            byte_data.close()
            self.res_data[self.date_list[file_index_num]
                          ] = self.data(db_data['ship'])
            i += 1
            del db_data

    def data(self, user_data):
        temp_dict = {
            'value': True,
            'battles': {
                'pvp': 0,
                'pvp_solo': 0,
                'pvp_div2': 0,
                'pvp_div3': 0,
                'rank_solo': 0,

                'AirCarrier': 0,
                'Battleship': 0,
                'Cruiser': 0,
                'Destroyer': 0,
                'Submarine': 0
            },
            'data': {
                'win_rate': 0,
                'damage_dealt': 0,
                'frags': 0,
                'xp': 0,
                'planes_kill': 0,
                'personal_rate': 0,
                'value_battles_count': 0
            }
        }
        if user_data == {}:
            temp_dict['value'] = False
            return temp_dict
        for ship_id, ship_data in user_data.items():
            if ship_data == {}:
                continue
            for type_index in ['pvp', 'pvp_solo', 'pvp_div2', 'pvp_div3', 'rank_solo']:
                if ship_data[type_index] == {}:
                    continue
                temp_dict['battles'][type_index] += ship_data[type_index]['battles_count']
                if type_index == 'pvp':
                    temp_dict['data']['win_rate'] += ship_data[type_index]['wins']
                    temp_dict['data']['damage_dealt'] += ship_data[type_index]['damage_dealt']
                    temp_dict['data']['frags'] += ship_data[type_index]['frags']
                    temp_dict['data']['xp'] += ship_data[type_index]['original_exp']
                    temp_dict['data']['planes_kill'] += ship_data[type_index]['planes_killed']
                    pr_data = personal_rating().number_pr(
                        ship_id, ship_data[type_index])
                    temp_dict['data']['personal_rate'] += pr_data[1]
                    temp_dict['data']['value_battles_count'] += pr_data[0]
        return temp_dict


class pic:
    def __init__(self, data) -> None:
        self.account_id = data[0]
        self.server = data[1]

    async def update_data(self) -> dict:
        if os.path.exists(os.path.join(DATABASE_PATH, self.server, str(self.account_id))) != True or len(os.listdir(os.path.join(DATABASE_PATH, self.server, str(self.account_id)))) < 8:
            return {'status': 'error', 'message': 'New User'}
        res = await update((self.account_id, self.server)).user_info()
        if res['status'] != 'ok':
            return {'status': res['status'], 'message': res['message']}
        today = date.today().strftime("%Y-%m-%d")
        gzip_data = gzip.compress(
            bytes(str(res['data']), encoding='utf-8'))
        with open(os.path.join(os.path.join(DATABASE_PATH, self.server, str(self.account_id), (today+'.txt'))), "wb") as fp:
            fp.write(gzip_data)
        fp.close()
        return {'status': 'ok', 'message': 'SUCCESS', 'data': {'user': res['data']['user'], 'clan': res['data']['clans']}}

    def get_color(self, battle_num: int):
        if battle_num == 'x':
            return(153, 151, 151)
        elif battle_num == 0:
            return(153, 151, 151)
        elif battle_num > 0 and battle_num <= 10:
            return(134, 198, 252)
        elif battle_num > 10 and battle_num <= 20:
            return(54, 146, 241)
        elif battle_num > 20 and battle_num < 30:
            return(19, 90, 208)
        else:
            return(19, 90, 208)

    # @profile(precision=4, stream=open('memory_profiler.log', 'w+'))
    async def main(self):
        info_data = await self.update_data()
        if info_data['status'] == 'ok' and info_data['message'] == 'SUCCESS':
            info_data = info_data['data']
        else:
            return info_data
        user_data = calendar((self.account_id, self.server)).calerdar_data()

        imageFile = os.path.join(os.path.dirname(__file__), 'bg.png')
        font_path = os.path.join(file_path, 'data', 'ARLRDBD.TTF') if isWin else os.path.join(
            '/usr/share/fonts', 'ARLRDBD.TTF')
        font = ImageFont.truetype(font_path, 55)
        font2 = ImageFont.truetype(font_path, 73)
        font3 = ImageFont.truetype(font_path, 100)
        img = Image.open(imageFile)
        draw = ImageDraw.Draw(img)

        data = []
        date_list = []
        for n_date, n_data in user_data.items():
            date_list.append(n_date)
            if n_data['value'] == False:
                continue
            wins = round(n_data['data']['win_rate'] /
                         n_data['battles']['pvp']*100, 2)
            damage = int(n_data['data']['damage_dealt'] /
                         n_data['battles']['pvp'])
            frag = round(n_data['data']['frags']/n_data['battles']['pvp'], 2)
            xp = round(n_data['data']['xp']/n_data['battles']['pvp'], 2)
            plane = round(n_data['data']['planes_kill'] /
                          n_data['battles']['pvp'], 2)
            pr = 0 if n_data['data']['value_battles_count'] == 0 else round(
                n_data['data']['personal_rate']/n_data['data']['value_battles_count'], 2)
            data.append([n_date, wins, damage, frag, xp, plane, pr])
        clc_num = 1
        plt.style.use('ggplot')
        plt.figure(figsize=(30, 17.5))
        while clc_num <= 6:
            plt.subplot(3, 2, clc_num)
            x_ticks = []
            num = []
            for i in data:
                num.append(i[clc_num])
                x_ticks.append(i[0][5:])
            x = x_ticks
            y1 = num
            #
            x_ = range(len(x))
            y_ = range(len(y1))
            if len(data) <= 7:
                x_limit = 0
            elif len(data) > 7 and len(data) <= 10:
                x_limit = 1
            elif len(data) > 10 and len(data) <= 20:
                x_limit = 2
            elif len(data) > 20 and len(data) <= 35:
                x_limit = 3
            elif len(data) > 35 and len(data) <= 50:
                x_limit = 4
            elif len(data) > 50:
                x_limit = 5
            if x_limit == 0:
                plt.xticks(list(x_), x, rotation=45)
            else:
                plt.xticks(list(x_)[::x_limit], x[::x_limit], rotation=45)
            color_list = ['#CB4B4B', '#4DA74D', '#134F90',
                          '#BD9B33', '#9440ED', '#2B591F']
            plt.plot(x, y1, color=color_list[clc_num-1],
                     label='label1', linewidth=2.0)
            plt.tick_params(labelsize=20)
            name_list = ['Win Rate', 'Average Damage', 'Average Frags',
                         'Average Experience(XP)', 'Average Planes Killed', 'Personsl Rating(PR)']
            plt.title(name_list[clc_num-1], fontsize=28)

            clc_num += 1
        plt.tight_layout(pad=0.60)
        pic_name = str(time.time())
        pic_path = os.path.join(file_path, 'temp', f'{pic_name}.jpg')
        plt.savefig(pic_path, format='jpg')
        achieve_img = Image.open(pic_path)
        img.paste(achieve_img, (80, 1687))
        os.remove(pic_path)
        achieve_img.close()
        plt.close()
        all_date = []
        all_battlse_count = 0
        value_date = 0
        active_date = 0
        max_battles_date = ('1970-01-01', 0)
        j = 0
        while j < (len(date_list) - 1):
            date1 = date_list[j]
            date2 = date_list[j+1]

            if user_data[date1]['value'] != True or user_data[date2]['value'] != True:
                all_date.append('x')
                continue
            add_date = (user_data[date2]['battles']['pvp'] - user_data[date1]['battles']['pvp']) + (
                user_data[date2]['battles']['rank_solo'] - user_data[date1]['battles']['rank_solo'])
            all_date.append(add_date)
            value_date += 1
            if add_date > 0:
                active_date += 1
                all_battlse_count += add_date
                if add_date > max_battles_date[1]:
                    max_battles_date = (date2, add_date)

            j += 1
        all_date.reverse()
        local_time = time.localtime(time.time())
        week_index = local_time.tm_wday
        x_ = 3307-1765
        y_ = 3840-3257
        x_1 = 3346-1765
        y_1 = 3877-3257
        i = 0
        while i < len(all_date):
            x_as, y_as = self.get_coord(len(all_date), i, week_index)
            if x_as >= 10:
                break
            x = x_ - x_as*(61+79)
            y = y_ + y_as*(50+79)
            color = self.get_color(all_date[i])
            w = 79
            h = 79
            r = 10
            draw.ellipse((x, y, x+r, y+r), fill=color)
            draw.ellipse((x+w-r, y, x+w, y+r), fill=color)
            draw.ellipse((x, y+h-r, x+r, y+h), fill=color)
            draw.ellipse((x+w-r, y+h-r, x+w, y+h), fill=color)
            draw.rectangle((x+r/2, y, x+w-(r/2), y+h), fill=color)
            draw.rectangle((x, y+r/2, x+w, y+h-(r/2)), fill=color)
            x, y = font.getsize(str(all_date[i]))
            x = x_1 - x/2 - x_as*(61+79)
            y = y_1 - y/2 + y_as*(50+79)
            draw.text((x, y), str(all_date[i]), (255, 255, 255), font=font)
            i += 1
        account_name = info_data['user']['nickname']
        clan_name = '' if info_data['clan']['clan'] == {
        } else info_data['clan']['clan']['tag']
        user_name = '['+clan_name+']'+account_name
        xcoord = self.x_coord(user_name, font=font3)
        draw.text((1596-xcoord, 40), user_name, (19, 90, 208), font=font3)
        draw.text((4175-1765, 3820-3257), str(len(date_list)),
                  (19, 90, 208), font=font2)
        draw.text((4100-1765, 3938-3257), str(active_date),
                  (19, 90, 208), font=font2)
        draw.text((4100-1765, 4054-3257), str(
            round(active_date/len(date_list)*100, 2))+'%', (19, 90, 208), font=font2)
        draw.text((4227-1765, 4172-3257), str(all_battlse_count),
                  (19, 90, 208), font=font2)
        draw.text((4305-1765, 4289-3257), str(round(all_battlse_count/len(date_list), 1)),
                  (19, 90, 208), font=font2)
        draw.text((4020-1765, 4404-3257), max_battles_date[0],
                  (19, 90, 208), font=font2)
        draw.text((4092-1765, 4520-3257), str(max_battles_date[1]),
                  (19, 90, 208), font=font2)

        img = img.resize((1590, 1780))
        pic_path = os.path.join(file_path, 'temp', '3-{}.png'.format(
            png_name().generate_name(str(int(time.time()*100000)))))
        img.save(pic_path)
        img.close()
        del user_data
        del draw
        gc.collect()
        return {'status': 'ok', 'message': 'SUCCESS', 'img': pic_path}

    def x_coord(self, in_str: str, font: ImageFont.FreeTypeFont):
        x, y = font.getsize(in_str)
        out_coord = x/2
        return out_coord

    def get_coord(self, date_len: int, date_num: int, week: int):
        if date_len <= week + 1:
            return 0, (week - date_num + 1)
        else:
            if date_num <= week:
                return 0, (week - date_num)
            else:
                temp_num = date_num - week - 1
                x = temp_num / 7 + 1
                y = 7 - (temp_num % 7) - 1
                return int(x), int(y)


# def test():
#     i = 0
#     while i <= 50:
#         print(i)
#         sys_mem = psutil.virtual_memory()
#         mem = '%.2f MB' % (psutil.Process(
#             os.getpid()).memory_info().rss / 1024 / 1024)
#         print("程序占用:{}  总占用:{}%  可用:{:.2f}M ".format(
#             mem, sys_mem[2], sys_mem[1]/1024/1024))
#         i += 1
#         print(asyncio.run(pic((2023619512, 'asia')).main()))
#         gc.collect()


# test()
