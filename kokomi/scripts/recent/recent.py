import gzip
import json
import os
import httpx
import threading
import asyncio
import time
from datetime import date, timedelta
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import platform
import datetime
import gc
import yaml

isWin = True if platform.system().lower() == 'windows' else False
file_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
png_path = os.path.dirname(__file__)

f = open(os.path.join(file_path, 'config.yaml'))
config_data = yaml.load(f.read(), Loader=yaml.FullLoader)
DATABASE_PATH = config_data['DatabaseConfig']['Database_path']
f.close()


class personal_rating:
    '''返回pr数据'''

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
            return {'value_battles_count': 0, 'personal_rating': -1, 'n_damage_dealt': -1, 'n_frags': -1}
        if str(ship_id) not in self.number_data['data'] and str(ship_id) in ss_server:
            server_damage_dealt = ss_server[str(
                ship_id)]['average_damage_dealt']
            server_frags = ss_server[str(ship_id)]['average_frags']
            server_wins = ss_server[str(ship_id)]['win_rate']
        else:
            if self.number_data['data'][str(ship_id)] == []:
                return {'value_battles_count': 0, 'personal_rating': -1, 'n_damage_dealt': -1, 'n_frags': -1}
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
        n_damage_dealt = average_damage_dealt/server_damage_dealt
        n_frags = average_kd/server_frags
        return {'value_battles_count': battles_count, 'personal_rating': round(pr*battles_count, 6), 'n_damage_dealt': round(n_damage_dealt*battles_count, 6), 'n_frags': round(n_frags*battles_count, 6)}


class recent:
    '''计算recent数据'''

    def __init__(self, data) -> None:
        self.account_id = data[0]
        self.server = data[1]
        self.date = data[2]
        self.path = os.path.join(
            DATABASE_PATH, '{}'.format(data[1]), '{}'.format(data[0]))
        self.index_list = [
            # base data
            "battles_count",
            "wins",
            "losses",
            "damage_dealt",
            "planes_killed",
            "art_agro",
            "tpd_agro",
            "survived",
            "ships_spotted",
            "win_and_survived",
            "original_exp",
            "scouting_damage",
            # frags data
            "frags",
            "frags_by_main",
            "frags_by_atba",
            "frags_by_tpd",
            "frags_by_dbomb",
            "frags_by_ram",
            "frags_by_planes",
            # hits data
            "hits_by_skip",
            "hits_by_atba",
            "hits_by_rocket",
            "hits_by_bomb",
            "hits_by_tpd",
            "hits_by_main",
            "hits_by_tbomb",
            # shots data
            "shots_by_main",
            "shots_by_tbomb",
            "shots_by_tpd",
            "shots_by_bomb",
            "shots_by_rocket",
            "shots_by_skip",
            "shots_by_atba",
            # points data
            "control_dropped_points",
            "control_captured_points",
            "team_control_captured_points",
            "team_control_dropped_points"
        ]
        self.zero_data = {}
        self.all_data = {}
        for index in self.index_list:
            self.zero_data[index] = 0
            self.all_data[index] = 0
        for index in ["value_battles_count", "personal_rating", "n_damage_dealt", "n_frags"]:
            self.all_data[index] = 0
        self.recent_dict = {
            'nickname': None,
            'clan': {},
            'battles': {
                'pvp': {'all': {}, 'type': {'pvp_solo': {}, 'pvp_div2': {}, 'pvp_div3': {}},  'ships': {}},
                'rank': {'all': {}, 'type': {'rank_solo': {}}, 'ships': {}}
            },
            'achievements': {}
        }

    def get_list(self, date):
        return datetime.datetime.strptime(date, "%Y-%m-%d").timestamp()

    async def recent_data(self):
        data = await self.recentdata()
        if data['status'] == 'ok' and data['message'] == 'SUCCESS':
            data['data'] = self.recent_dict
            return data
        else:
            return data

    def new_dict(self, battles_type: str, dict_type: str, data_type: str) -> None:
        if data_type == 'ships':
            if dict_type not in self.recent_dict['battles'][battles_type][data_type]:
                self.recent_dict['battles'][battles_type][data_type][dict_type] = {
                }
        else:
            for index in self.index_list:
                self.recent_dict['battles'][battles_type][data_type][index] = 0

    async def update_data(self) -> dict:
        '''Update user data before clculating recent data'''
        res = await update((self.account_id, self.server)).user_info()
        if res['status'] != 'ok':
            return {'status': res['status'], 'message': res['message']}
        if os.path.exists(self.path) == False:
            today = date.today().strftime("%Y-%m-%d")
            yesterday = (date.today() + timedelta(days=-1)
                         ).strftime("%Y-%m-%d")
            os.mkdir(os.path.join(self.path))
            gzip_data = gzip.compress(
                bytes(str(res['data']), encoding='utf-8'))
            with open(os.path.join(os.path.join(self.path, (today+'.txt'))), "wb") as fp:
                fp.write(gzip_data)
            fp.close()
            with open(os.path.join(os.path.join(self.path, (yesterday+'.txt'))), "wb") as fp:
                fp.write(gzip_data)
            fp.close()
            return {'status': 'error', 'message': 'New User'}
        else:
            today = date.today().strftime("%Y-%m-%d")
            gzip_data = gzip.compress(
                bytes(str(res['data']), encoding='utf-8'))
            with open(os.path.join(os.path.join(self.path, (today+'.txt'))), "wb") as fp:
                fp.write(gzip_data)
            fp.close()
        gc.collect()
        return {'status': 'ok', 'message': 'SUCCESS', 'data': res['data']}

    async def recentdata(self):
        '''Calculating recent data'''
        user_data = await self.update_data()
        if user_data['status'] != 'ok':
            return {'status': 'error', 'message': user_data['message']}
        else:
            if datetime.datetime.now().hour >= 0 and datetime.datetime.now().hour <= 4:
                date_add = True
            else:
                date_add = False
            db_data = user_data['data']
            today = date.today().strftime("%Y-%m-%d")
            dby = (date.today() + timedelta(days=-2)).strftime("%Y-%m-%d")
            if os.path.exists(os.path.join(self.path, (dby+'.txt'))) == False:
                day = (date.today() + timedelta(days=-(self.date))
                       ).strftime("%Y-%m-%d")
                date_add = False
            else:
                day = (date.today() + timedelta(days=-(self.date +
                       ((1 if date_add else 0))))).strftime("%Y-%m-%d")
            self.recent_dict['nickname'] = db_data['user']['nickname']
            self.recent_dict['clan'] = db_data['clans']
            self.recent_dict['start_date'] = day
            self.recent_dict['end_date'] = today
            if os.path.exists(os.path.join(self.path, (day+'.txt'))) == False:
                file_name_list = os.listdir(self.path)
                file_date_list = []
                for i_date in file_name_list:
                    file_date_list.append(i_date.replace('.txt', ''))
                # for i_date, i_data in db_data.items():
                #     file_date_list.append(i_date)
                file_date_list = sorted(
                    file_date_list, key=lambda date: self.get_list(date))
                bind_date = file_date_list[0]
                date_len = len(file_date_list) - (0 if date_add else 1)
                return {'status': 'ok', 'message': 'Date too long', 'bind_num': date_len, 'bind_date': bind_date}
            else:
                today_data = db_data
                day_data = eval(str(gzip.decompress(
                    open(os.path.join(self.path, (day+'.txt')), 'rb').read()), encoding="utf-8"))
                # with open(os.path.join(self.path, (day+'.json')), 'w', encoding='utf-8') as f:
                #     f.write(json.dumps(day_data, ensure_ascii=False))
                if today_data['user']['value'] == False:
                    return {'status': 'ok', 'message': 'ID not found'}
                if today_data['user']['hidden'] or day_data['user']['hidden']:
                    return {'status': 'ok', 'message': 'Hidden profile'}
                if today_data['ship'] == {}:
                    return {'status': 'ok', 'message': 'Data is none'}
                for ship_id, ship_info in today_data['ship'].items():
                    self.rank_data(ship_id, ship_info, day_data)
                    self.pvp_data(ship_id, ship_info, day_data)

                self.rank_pr()
                self.pvp_pr()
                self.ach(today_data['achievements'],
                         day_data['achievements'])
                return {'status': 'ok', 'message': 'SUCCESS', 'data': {}}

    def pvp_data(self, ship_id, ship_info, day_data):
        if ship_info == {}:
            ship_info = {
                'pvp': {},
                'pvp_solo': {},
                'pvp_div2': {},
                'pvp_div3': {},
                'rank_solo': {}
            }
        if ship_info['pvp'] == {}:
            pass
        else:
            new_battles_count = ship_info['pvp']['battles_count']
            if ship_id not in day_data['ship']:
                old_battles_count = 0
            elif day_data['ship'][ship_id] == {} or day_data['ship'][ship_id]['pvp'] == {}:
                old_battles_count = 0
            else:
                old_battles_count = day_data['ship'][ship_id]['pvp']['battles_count']

            if new_battles_count <= old_battles_count:
                pass
            else:
                self.recent_dict['battles']['pvp']['ships'][ship_id] = {
                    'pvp': {}, 'pvp_solo': {}, 'pvp_div2': {}, 'pvp_div3': {}}
                for battles_type in ['pvp', 'pvp_solo', 'pvp_div2', 'pvp_div3']:
                    self.data(ship_info[battles_type], dict(self.zero_data) if old_battles_count ==
                              0 else day_data['ship'][ship_id][battles_type], battles_type, ship_id)

    def rank_data(self, ship_id, ship_info, day_data):
        if ship_info == {}:
            ship_info = {
                'pvp': {},
                'pvp_solo': {},
                'pvp_div2': {},
                'pvp_div3': {},
                'rank_solo': {}
            }
        if ship_info['rank_solo'] == {}:
            pass
        else:
            new_battles_count = ship_info['rank_solo']['battles_count']
            if ship_id not in day_data['ship']:
                old_battles_count = 0
            elif day_data['ship'][ship_id] == {} or day_data['ship'][ship_id]['rank_solo'] == {}:
                old_battles_count = 0
            else:
                old_battles_count = day_data['ship'][ship_id]['rank_solo']['battles_count']

            if new_battles_count <= old_battles_count:
                pass
            else:
                self.recent_dict['battles']['rank']['ships'][ship_id] = {
                    'rank': {}}
                self.data(ship_info['rank_solo'], dict(self.zero_data) if old_battles_count ==
                          0 else day_data['ship'][ship_id]['rank_solo'], 'rank', ship_id)

    def pvp_pr(self):
        if self.recent_dict['battles']['pvp']['ships'] != {}:
            for ship_id, pvp_data in self.recent_dict['battles']['pvp']['ships'].items():
                for battles_type in ['pvp', 'pvp_solo', 'pvp_div2', 'pvp_div3']:
                    if pvp_data[battles_type] != {}:
                        pr_data = personal_rating().number_pr(
                            ship_id, pvp_data[battles_type])
                        if pr_data['personal_rating'] != -1:
                            self.recent_dict['battles']['pvp']['ships'][ship_id][battles_type][
                                'value_battles_count'] = pr_data['value_battles_count']
                            self.recent_dict['battles']['pvp']['ships'][ship_id][battles_type][
                                'personal_rating'] = pr_data['personal_rating']
                            self.recent_dict['battles']['pvp']['ships'][ship_id][
                                battles_type]['n_damage_dealt'] = pr_data['n_damage_dealt']
                            self.recent_dict['battles']['pvp']['ships'][ship_id][battles_type]['n_frags'] = pr_data['n_frags']
                            if battles_type == 'pvp':
                                self.recent_dict['battles']['pvp']['all']['value_battles_count'] += pr_data['value_battles_count']
                                self.recent_dict['battles']['pvp']['all']['personal_rating'] += pr_data['personal_rating']
                                self.recent_dict['battles']['pvp']['all']['n_damage_dealt'] += pr_data['n_damage_dealt']
                                self.recent_dict['battles']['pvp']['all']['n_frags'] += pr_data['n_frags']
                            else:
                                self.recent_dict['battles']['pvp']['type'][battles_type][
                                    'value_battles_count'] += pr_data['value_battles_count']
                                self.recent_dict['battles']['pvp']['type'][battles_type]['personal_rating'] += pr_data['personal_rating']
                                self.recent_dict['battles']['pvp']['type'][battles_type]['n_damage_dealt'] += pr_data['n_damage_dealt']
                                self.recent_dict['battles']['pvp']['type'][battles_type]['n_frags'] += pr_data['n_frags']
                        else:
                            self.recent_dict['battles']['pvp']['ships'][ship_id][battles_type]['value_battles_count'] = 0
                            self.recent_dict['battles']['pvp']['ships'][ship_id][battles_type]['personal_rating'] = 0
                            self.recent_dict['battles']['pvp']['ships'][ship_id][battles_type]['n_damage_dealt'] = 0
                            self.recent_dict['battles']['pvp']['ships'][ship_id][battles_type]['n_frags'] = 0
                    else:
                        pass

    def rank_pr(self):
        if self.recent_dict['battles']['rank']['ships'] != {}:
            for ship_id, rank_data in self.recent_dict['battles']['rank']['ships'].items():
                for battles_type in ['rank']:
                    if rank_data[battles_type] != {}:
                        pr_data = personal_rating().number_pr(
                            ship_id, rank_data[battles_type])
                        if pr_data['personal_rating'] != -1:
                            self.recent_dict['battles']['rank']['ships'][ship_id][battles_type][
                                'value_battles_count'] = pr_data['value_battles_count']
                            self.recent_dict['battles']['rank']['ships'][ship_id][battles_type][
                                'personal_rating'] = pr_data['personal_rating']
                            self.recent_dict['battles']['rank']['ships'][ship_id][
                                battles_type]['n_damage_dealt'] = pr_data['n_damage_dealt']
                            self.recent_dict['battles']['rank']['ships'][ship_id][battles_type]['n_frags'] = pr_data['n_frags']
                            self.recent_dict['battles']['rank']['type']['rank_solo'][
                                'value_battles_count'] += pr_data['value_battles_count']
                            self.recent_dict['battles']['rank']['type']['rank_solo']['personal_rating'] += pr_data['personal_rating']
                            self.recent_dict['battles']['rank']['type']['rank_solo']['n_damage_dealt'] += pr_data['n_damage_dealt']
                            self.recent_dict['battles']['rank']['type']['rank_solo']['n_frags'] += pr_data['n_frags']
                            self.recent_dict['battles']['rank']['all']['value_battles_count'] += pr_data['value_battles_count']
                            self.recent_dict['battles']['rank']['all']['personal_rating'] += pr_data['personal_rating']
                            self.recent_dict['battles']['rank']['all']['n_damage_dealt'] += pr_data['n_damage_dealt']
                            self.recent_dict['battles']['rank']['all']['n_frags'] += pr_data['n_frags']
                        else:
                            self.recent_dict['battles']['rank']['ships'][ship_id][battles_type]['value_battles_count'] = 0
                            self.recent_dict['battles']['rank']['ships'][ship_id][battles_type]['personal_rating'] = 0
                            self.recent_dict['battles']['rank']['ships'][ship_id][battles_type]['n_damage_dealt'] = 0
                            self.recent_dict['battles']['rank']['ships'][ship_id][battles_type]['n_frags'] = 0
                    else:
                        pass

    def ach(self, new_data: dict, old_data: dict) -> None:
        if old_data == None:
            pass
        if new_data == {}:
            pass
        else:
            if old_data == {}:
                old_data = dict(self.zero_data)
            for name, num in new_data.items():
                if name not in old_data:
                    self.recent_dict['achievements'][name] = num
                else:
                    if num - old_data[name] > 0:
                        self.recent_dict['achievements'][name] = num - \
                            old_data[name]

    def data(self, new_data: dict, old_data: dict, battle_type: str, ship_id: str) -> None:
        if new_data == {}:
            return None
        if old_data == {}:
            old_data = dict(self.zero_data)

        if battle_type == 'pvp':
            if self.recent_dict['battles']['pvp']['all'] == {}:
                self.recent_dict['battles']['pvp']['all'] = dict(self.all_data)
            for index in self.index_list:
                self.recent_dict['battles']['pvp']['all'][index] += new_data[index] - \
                    old_data[index]
                self.recent_dict['battles']['pvp']['ships'][ship_id]['pvp'][index] = new_data[index] - old_data[index]
        elif battle_type == 'rank':
            for index in self.index_list:
                if self.recent_dict['battles']['rank']['all'] == {}:
                    self.recent_dict['battles']['rank']['all'] = dict(
                        self.all_data)
                self.recent_dict['battles']['rank']['all'][index] += new_data[index] - \
                    old_data[index]
                if self.recent_dict['battles']['rank']['type']['rank_solo'] == {}:
                    self.recent_dict['battles']['rank']['type']['rank_solo'] = dict(
                        self.all_data)
                self.recent_dict['battles']['rank']['type']['rank_solo'][index] += new_data[index] - old_data[index]
                self.recent_dict['battles']['rank']['ships'][ship_id]['rank'][index] = new_data[index] - old_data[index]
        else:
            if new_data['battles_count'] - old_data['battles_count'] <= 0:
                return None
            for index in self.index_list:
                if self.recent_dict['battles']['pvp']['type'][battle_type] == {}:
                    self.recent_dict['battles']['pvp']['type'][battle_type] = dict(
                        self.all_data)
                self.recent_dict['battles']['pvp']['type'][battle_type][index] += new_data[index] - old_data[index]
                self.recent_dict['battles']['pvp']['ships'][ship_id][battle_type][index] = new_data[index] - old_data[index]


class update:
    '''更新数据'''

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


class pic:
    '''图片生成'''

    def __init__(self) -> None:
        font2_path = os.path.join(file_path, 'data', 'SourceHanSansCN-Bold.ttf') if isWin else os.path.join(
            '/usr/share/fonts', 'SourceHanSansCN-Bold.ttf')
        self.font = {
            1: {
                50: ImageFont.truetype(font2_path, 50, encoding="utf-8"),
                60: ImageFont.truetype(font2_path, 60, encoding="utf-8"),
                65: ImageFont.truetype(font2_path, 65, encoding="utf-8"),
                70: ImageFont.truetype(font2_path, 70, encoding="utf-8"),
                100: ImageFont.truetype(font2_path, 100, encoding="utf-8"),
                120: ImageFont.truetype(font2_path, 120, encoding="utf-8")

            }
        }
        self.text_list = []

    def add_alpha_channel(self, img):
        '''给图片添加alpha通道'''
        b_channel, g_channel, r_channel = cv2.split(img)
        alpha_channel = np.ones(
            b_channel.shape, dtype=b_channel.dtype) * 255

        img_new = cv2.merge(
            (b_channel, g_channel, r_channel, alpha_channel))
        return img_new

    def merge_img(self, jpg_img, png_img, y1, y2, x1, x2):
        '''图片叠加'''
        if jpg_img.shape[2] == 3:
            jpg_img = self.add_alpha_channel(jpg_img)
        yy1 = 0
        yy2 = png_img.shape[0]
        xx1 = 0
        xx2 = png_img.shape[1]

        if x1 < 0:
            xx1 = -x1
            x1 = 0
        if y1 < 0:
            yy1 = - y1
            y1 = 0
        if x2 > jpg_img.shape[1]:
            xx2 = png_img.shape[1] - (x2 - jpg_img.shape[1])
            x2 = jpg_img.shape[1]
        if y2 > jpg_img.shape[0]:
            yy2 = png_img.shape[0] - (y2 - jpg_img.shape[0])
            y2 = jpg_img.shape[0]

        alpha_png = png_img[yy1:yy2, xx1:xx2, 3] / 255.0
        alpha_jpg = 1 - alpha_png

        for c in range(0, 3):
            jpg_img[y1:y2, x1:x2, c] = (
                (alpha_jpg*jpg_img[y1:y2, x1:x2, c]) + (alpha_png*png_img[yy1:yy2, xx1:xx2, c]))

        return jpg_img

    def x_coord(self, in_str: str, font: ImageFont.FreeTypeFont):
        '''获取文字的像素长度'''
        x = font.getsize(in_str)[0]
        out_coord = x
        return out_coord

    def main(self, type, recent_data):
        '''主函数'''
        if recent_data['status'] != 'ok' or recent_data['message'] != 'SUCCESS':
            return recent_data
        elif recent_data['data']['battles'][type]['all'] == {}:
            return {'status': 'ok', 'message': 'Recent data is None'}
        else:
            # user & clan
            self.text_list.append(
                [(142, 181), recent_data['data']['nickname'], (0, 0, 0), 1, 120])
            if recent_data['data']['clan'] != {}:
                role_dict = {
                    'commander': '指挥官',
                    'executive_officer': '副指挥官',
                    'recruitment_officer': '征募官',
                    'commissioned_officer': '现役军官',
                    'officer': '前线军官',
                    'private': '军校见习生'
                }
                if recent_data['data']['clan']['clan'] == {}:
                    clan_info = 'None'
                else:
                    clan_info = '['+recent_data['data']['clan']['clan']['tag']+']' + \
                        recent_data['data']['clan']['clan']['name']+'\n  ' + \
                        role_dict[recent_data['data']['clan']['role']]
                self.text_list.append(
                    [(194, 335), clan_info, (0, 0, 0), 1, 70])
            # main pr
            if recent_data['data']['battles'][type]['all']['value_battles_count'] == 0:
                avg_pr = -1
                avg_n_damage = -1
                avg_n_frag = -1
            else:
                avg_n_damage = recent_data['data']['battles'][type]['all']['n_damage_dealt'] / \
                    recent_data['data']['battles'][type]['all']['value_battles_count']
                avg_n_frag = recent_data['data']['battles'][type]['all']['n_frags'] / \
                    recent_data['data']['battles'][type]['all']['value_battles_count']
                avg_pr = int(recent_data['data']['battles'][type]['all']['personal_rating'] /
                             recent_data['data']['battles'][type]['all']['value_battles_count']) + 1
            pr_data = self.pr_info(avg_pr)
            if type == 'rank':
                background_path = os.path.join(png_path, 'background_rank.jpg')
            else:
                background_path = os.path.join(png_path, 'background_pvp.jpg')
            pr_png_path = os.path.join(
                png_path, 'pr', '{}.png'.format(pr_data[0]))
            res_img = cv2.imread(background_path, cv2.IMREAD_UNCHANGED)
            pr_png = cv2.imread(pr_png_path, cv2.IMREAD_UNCHANGED)
            x1 = 136
            y1 = 684
            x2 = x1 + pr_png.shape[1]
            y2 = y1 + pr_png.shape[0]
            res_img = self.merge_img(res_img, pr_png, y1, y2, x1, x2)
            self.text_list.append(
                [(643+100*pr_data[3], 755), pr_data[2]+str(pr_data[4]), (255, 255, 255), 1, 60])
            str_pr = '{:,}'.format(int(avg_pr))
            fontStyle = self.font[1][100]
            w = self.x_coord(str_pr, fontStyle)
            self.text_list.append(
                [(2862-w, 708), str_pr, (255, 255, 255), 1, 100])
            # all avg
            battles_count = '{:,}'.format(
                recent_data['data']['battles'][type]['all']['battles_count'])
            avg_win = '{:.2f}%'.format(recent_data['data']['battles'][type]['all']
                                       ['wins']/recent_data['data']['battles'][type]['all']['battles_count']*100)
            avg_wins = recent_data['data']['battles'][type]['all']['wins'] / \
                recent_data['data']['battles'][type]['all']['battles_count']*100
            avg_damage = '{:,}'.format(int(recent_data['data']['battles'][type]['all']
                                       ['damage_dealt']/recent_data['data']['battles'][type]['all']['battles_count'])).replace(',', ' ')
            avg_frag = '{:.2f}'.format(recent_data['data']['battles'][type]['all']
                                       ['frags']/recent_data['data']['battles'][type]['all']['battles_count'])
            avg_xp = '{:,}'.format(int(recent_data['data']['battles'][type]['all']['original_exp'] /
                                   recent_data['data']['battles'][type]['all']['battles_count'])).replace(',', ' ')

            fontStyle = self.font[1][100]
            w = self.x_coord(battles_count, fontStyle)
            self.text_list.append(
                [(405-w/2, 970), battles_count, (0, 0, 0), 1, 100])
            w = self.x_coord(avg_win, fontStyle)
            self.text_list.append(
                [(405-w/2+557, 970), avg_win, self.color_box(0, avg_wins)[1], 1, 100])
            w = self.x_coord(avg_damage, fontStyle)
            self.text_list.append(
                [(405-w/2+557*2, 970), avg_damage, self.color_box(1, avg_n_damage)[1], 1, 100])
            w = self.x_coord(avg_frag, fontStyle)
            self.text_list.append(
                [(405-w/2+557*3, 970), avg_frag, self.color_box(2, avg_n_frag)[1], 1, 100])
            w = self.x_coord(avg_xp, fontStyle)
            self.text_list.append(
                [(405-w/2+557*4, 970), avg_xp, (0, 0, 0), 1, 100])
            fontStyle = self.font[1][50]
            w = self.x_coord(
                '数据统计区间：{} —— {}'.format(recent_data['data']['start_date'], recent_data['data']['end_date']), fontStyle)
            self.text_list.append([(1523-w/2, 1100), '数据统计区间：{} —— {}'.format(
                recent_data['data']['start_date'], recent_data['data']['end_date']), (71, 71, 71), 1, 50])
            # type
            if type == 'pvp':
                type_list = ['pvp_solo', 'pvp_div2', 'pvp_div3']
            else:
                type_list = ['rank_solo']
            for battles_type in type_list:
                if recent_data['data']['battles'][type]['type'][battles_type] != {}:
                    battles_count = '{:,}'.format(
                        recent_data['data']['battles'][type]['type'][battles_type]['battles_count'])
                    avg_win = '{:.2f}%'.format(recent_data['data']['battles'][type]['type'][battles_type]
                                               ['wins']/recent_data['data']['battles'][type]['type'][battles_type]['battles_count']*100)
                    avg_wins = recent_data['data']['battles'][type]['type'][battles_type]['wins'] / \
                        recent_data['data']['battles'][type]['type'][battles_type]['battles_count']*100
                    avg_damage = '{:,}'.format(int(recent_data['data']['battles'][type]['type'][battles_type]
                                               ['damage_dealt']/recent_data['data']['battles'][type]['type'][battles_type]['battles_count'])).replace(',', ' ')
                    avg_frag = '{:.2f}'.format(recent_data['data']['battles'][type]['type'][battles_type]
                                               ['frags']/recent_data['data']['battles'][type]['type'][battles_type]['battles_count'])
                    avg_xp = '{:,}'.format(int(recent_data['data']['battles'][type]['type'][battles_type]['original_exp'] /
                                           recent_data['data']['battles'][type]['type'][battles_type]['battles_count'])).replace(',', ' ')
                    avg_plane = '{:.2f}'.format(recent_data['data']['battles'][type]['type'][battles_type]
                                                ['planes_killed']/recent_data['data']['battles'][type]['type'][battles_type]['battles_count'])

                    if recent_data['data']['battles'][type]['type'][battles_type]['value_battles_count'] == 0:
                        avg_pr = -1
                        avg_n_damage = -1
                        avg_n_frag = -1
                    else:
                        avg_n_damage = recent_data['data']['battles'][type]['type'][battles_type]['n_damage_dealt'] / \
                            recent_data['data']['battles'][type]['type'][battles_type]['value_battles_count']
                        avg_n_frag = recent_data['data']['battles'][type]['type'][battles_type]['n_frags'] / \
                            recent_data['data']['battles'][type]['type'][battles_type]['value_battles_count']
                        avg_pr = recent_data['data']['battles'][type]['type'][battles_type]['personal_rating'] / \
                            recent_data['data']['battles'][type]['type'][battles_type]['battles_count']
                    str_pr = self.pr_info(
                        avg_pr)[5] + '(+'+str(self.pr_info(avg_pr)[4])+')'
                else:
                    battles_count = '--'
                    avg_win = '--'
                    avg_wins = -1
                    avg_damage = '--'
                    avg_frag = '--'
                    avg_xp = '--'
                    avg_plane = '--'
                    avg_n_damage = -1
                    avg_n_frag = -1
                    str_pr = '--'
                    avg_pr = -1
                if battles_type == 'pvp_div2':
                    i = 1
                elif battles_type == 'pvp_div3':
                    i = 2
                else:
                    i = 0
                fontStyle = self.font[1][65]
                w = self.x_coord(battles_count, fontStyle)
                self.text_list.append(
                    [(748-w/2, 1388+127*i), battles_count, (0, 0, 0), 1, 65])
                w = self.x_coord(str_pr, fontStyle)
                self.text_list.append(
                    [(1149-w/2, 1388+127*i), str_pr, self.pr_info(avg_pr)[1], 1, 65])
                w = self.x_coord(avg_win, fontStyle)
                self.text_list.append(
                    [(1562-w/2, 1388+127*i), avg_win, self.color_box(0, avg_wins)[1], 1, 65])
                w = self.x_coord(avg_damage, fontStyle)
                self.text_list.append(
                    [(1898-w/2, 1388+127*i), avg_damage, self.color_box(1, avg_n_damage)[1], 1, 65])
                w = self.x_coord(avg_frag, fontStyle)
                self.text_list.append(
                    [(2200-w/2, 1388+127*i), avg_frag, self.color_box(2, avg_n_frag)[1], 1, 65])
                w = self.x_coord(avg_xp, fontStyle)
                self.text_list.append(
                    [(2468-w/2, 1388+127*i), avg_xp, (0, 0, 0), 1, 65])
                w = self.x_coord(avg_plane, fontStyle)
                self.text_list.append(
                    [(2748-w/2, 1388+127*i), avg_plane, (0, 0, 0), 1, 65])
            # achievement
            achievement_list = recent_data['data']['achievements']
            if achievement_list != {}:
                achievement_list = sorted(
                    achievement_list.items(), key=lambda x: x[1], reverse=True)
                i = 0
                for ach_list in achievement_list:
                    index = ach_list[0]
                    num = ach_list[1]
                    if i == 10:
                        self.text_list.append(
                            [(312+239*i, 1930), '······'.format(num), (0, 0, 0), 1, 65])
                        break
                    ach_png_path = os.path.join(
                        png_path, 'achievement', '{}.png'.format(index))
                    ach_png = cv2.imread(ach_png_path, cv2.IMREAD_UNCHANGED)
                    ach_png = cv2.resize(ach_png, None, fx=2, fy=2)
                    x1 = 166 + 239*i
                    y1 = 1863
                    x2 = x1 + ach_png.shape[1]
                    y2 = y1 + ach_png.shape[0]
                    res_img = self.merge_img(res_img, ach_png, y1, y2, x1, x2)
                    self.text_list.append(
                        [(312+239*i, 1977), 'x{}'.format(num), (0, 0, 0), 1, 50])
                    i += 1
            # ship
            if (isinstance(res_img, np.ndarray)):
                res_img = Image.fromarray(
                    cv2.cvtColor(res_img, cv2.COLOR_BGR2RGB))
            all_png_path = os.path.join(png_path, 'all.jpg')
            all_png = Image.open(all_png_path)
            all_dict = json.load(
                open(os.path.join(png_path, 'all.json'), "r", encoding="utf-8"))
            #xier = all_png[0:115, 0:517]
            i = 0
            for ship_id, ship_data in recent_data['data']['battles'][type]['ships'].items():
                if ship_id in all_dict:
                    pic_code = all_dict[ship_id]
                    x = (pic_code % 10)
                    y = int(pic_code / 10)
                    ship_png = all_png.crop(
                        ((0+517*x), (0+115*y), (517+517*x), (115+115*y)))
                    res_img.paste(ship_png, (106, 2251+126*i))
                else:
                    pic_code = 0
                    x = (pic_code % 10)
                    y = int(pic_code / 10)
                    ship_png = all_png.crop(
                        ((0+517*x), (0+115*y), (517+517*x), (115+115*y)))
                    res_img.paste(ship_png, (106, 2251+126*i))
                battles_count = '{:,}'.format(ship_data[type]['battles_count'])
                avg_win = '{:.2f}%'.format(
                    ship_data[type]['wins']/ship_data[type]['battles_count']*100)
                avg_wins = ship_data[type]['wins'] / \
                    ship_data[type]['battles_count']*100
                avg_damage = '{:,}'.format(int(
                    ship_data[type]['damage_dealt']/ship_data[type]['battles_count'])).replace(',', ' ')
                avg_frag = '{:.2f}'.format(
                    ship_data[type]['frags']/ship_data[type]['battles_count'])
                avg_xp = '{:,}'.format(int(
                    ship_data[type]['original_exp']/ship_data[type]['battles_count'])).replace(',', ' ')
                avg_survived = '{:.1f}%'.format(
                    ship_data[type]['survived']/ship_data[type]['battles_count']*100)
                avg_hit = '{:.1f}%'.format(0.0 if ship_data[type]['shots_by_main'] ==
                                           0 else ship_data[type]['hits_by_main']/ship_data[type]['shots_by_main']*100)
                if ship_data[type]['value_battles_count'] == 0:
                    avg_pr = -1
                    avg_n_damage = -1
                    avg_n_frag = -1
                else:
                    avg_n_damage = ship_data[type]['n_damage_dealt'] / \
                        ship_data[type]['battles_count']
                    avg_n_frag = ship_data[type]['n_frags'] / \
                        ship_data[type]['battles_count']
                    avg_pr = ship_data[type]['personal_rating'] / \
                        ship_data[type]['battles_count']
                str_pr = self.pr_info(
                    avg_pr)[5] + '(+'+str(self.pr_info(avg_pr)[4])+')'

                fontStyle = self.font[1][65]
                w = self.x_coord(battles_count, fontStyle)
                self.text_list.append(
                    [(749-w/2, 2280+126*i), battles_count, (0, 0, 0), 1, 65])
                w = self.x_coord(str_pr, fontStyle)
                self.text_list.append(
                    [(1105-w/2, 2280+126*i), str_pr, self.pr_info(avg_pr)[1], 1, 65])
                w = self.x_coord(avg_win, fontStyle)
                self.text_list.append(
                    [(1507-w/2, 2280+126*i), avg_win, self.color_box(0, avg_wins)[1], 1, 65])
                w = self.x_coord(avg_damage, fontStyle)
                self.text_list.append(
                    [(1806-w/2, 2280+126*i), avg_damage, self.color_box(1, avg_n_damage)[1], 1, 65])
                w = self.x_coord(avg_frag, fontStyle)
                self.text_list.append(
                    [(2056-w/2, 2280+126*i), avg_frag, self.color_box(2, avg_n_frag)[1], 1, 65])
                w = self.x_coord(avg_xp, fontStyle)
                self.text_list.append(
                    [(2277-w/2, 2280+126*i), avg_xp, (0, 0, 0), 1, 65])
                w = self.x_coord(avg_survived, fontStyle)
                self.text_list.append(
                    [(2517-w/2, 2280+126*i), avg_survived, (0, 0, 0), 1, 65])
                w = self.x_coord(avg_hit, fontStyle)
                self.text_list.append(
                    [(2789-w/2, 2280+126*i), avg_hit, (0, 0, 0), 1, 65])
                i += 1
            self.text_list.append(
                [(1313, 2280+126*(i+1)), 'KokomiBot v3.0.1', (75, 75, 75), 1, 60])
            res_img = self.add_text(res_img)
            res_img = res_img[0:2251+126*(i+2), 0:3046]
            res_img = cv2.resize(res_img, None, fx=0.7, fy=0.7)
            png_out_path = os.path.join(file_path, 'temp', '2-{}.png'.format(
                png_name().generate_name(str(int(time.time()*100000)))))
            cv2.imwrite(png_out_path, res_img)
            all_png.close()
            del res_img
            gc.collect()
            return {'status': 'ok', 'message': 'SUCCESS', 'img': png_out_path}

    def pr_info(self, pr: int):
        '''pr info'''
        if pr == -1:
            # [pic_num ,color_box, 描述, 字数差（add_text用），pr差值，评级]
            return [0, (128, 128, 128), '水平未知：', 0, -1, '水平未知']
        elif pr >= 0 and pr < 750:
            return [1, (205, 51, 51), '距离下一评级：+', 0, int(750-pr), '还需努力']
        elif pr >= 750 and pr < 1100:
            return [2, (254, 121, 3), '距离下一评级：+', 0, int(1100-pr), '低于平均']
        elif pr >= 1100 and pr < 1350:
            return [3, (255, 193, 7), '距离下一评级：+', 0, int(1350-pr), '平均水平']
        elif pr >= 1350 and pr < 1550:
            return [4, (68, 179, 0), '距离下一评级：+', -3, int(1550-pr), '好']
        elif pr >= 1550 and pr < 1750:
            return [5, (49, 128, 0), '距离下一评级：+', -2, int(1750-pr), '很好']
        elif pr >= 1750 and pr < 2100:
            return [6, (52, 186, 211), '距离下一评级：+', -1, int(2100-pr), '非常好']
        elif pr >= 2100 and pr < 2450:
            return [7, (121, 61, 182), '距离下一评级：+', 0, int(2450-pr), '大佬平均']
        elif pr >= 2450:
            return [8, (88, 43, 128), '已超过最高评级：+', 0, int(pr-2450), '神佬平均']

    def color_box(self, index: int, num: float):
        '''avg/server 自上向下为 win dmg frag xp plane_kill'''
        index_list = [
            [70, 60, 55, 52.5, 51, 49, 45],
            [1.7, 1.4, 1.2, 1.1, 1.0, 0.95, 0.8],
            [2, 1.5, 1.3, 1.0, 0.6, 0.3, 0.2],
            [1.7, 1.5, 1.3, 1.1, 0.9, 0.7, 0.5],
            [2.0, 1.7, 1.5, 1.3, 1.0, 0.9, 0.7]
        ]
        data = index_list[index]
        if num == -1:
            return [0, (128, 128, 128)]
        elif num >= data[0]:
            return [8, (88, 43, 128)]
        elif num >= data[1] and num < data[0]:
            return [7, (121, 61, 182)]
        elif num >= data[2] and num < data[1]:
            return [6, (52, 186, 211)]
        elif num >= data[3] and num < data[2]:
            return [5, (49, 128, 0)]
        elif num >= data[4] and num < data[3]:
            return [4, (68, 179, 0)]
        elif num >= data[5] and num < data[4]:
            return [3, (255, 193, 7)]
        elif num >= data[6] and num < data[5]:
            return [2, (254, 121, 3)]
        elif num < data[6]:
            return [1, (205, 51, 51)]

    def add_text(self, res_img):
        draw = ImageDraw.Draw(res_img)
        for index in self.text_list:
            fontStyle = self.font[index[3]][index[4]]
            draw.text(index[0], index[1], index[2], font=fontStyle)
        res_img = cv2.cvtColor(np.asarray(res_img), cv2.COLOR_RGB2BGR)
        return res_img


# print(pic().main('pvp', asyncio.run(recent((2023619512, 'asia', 1)).recent_data())))
