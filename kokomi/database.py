import gzip
import json
import os
import httpx
import json
import threading
import asyncio
import time
import sqlite3
from datetime import date, timedelta
import platform
import datetime
import psutil
import gc
import sys
from memory_profiler import profile
import yaml


isWin = True if platform.system().lower() == 'windows' else False
file_path = os.path.dirname(__file__)

f = open(os.path.join(file_path, 'config.yaml'))
config_data = yaml.load(f.read(), Loader=yaml.FullLoader)
f.close()
db_path = config_data['DatabaseConfig']['Database_path']
acc_path = os.path.join(file_path, 'data', 'accountid.db')


debug = False
cyc = True
server = True


def server_url(server: str) -> str:
    '''Return the domain name of the server's website'''
    url_list = {
        'asia': 'http://vortex.worldofwarships.asia',
        'eu': 'http://vortex.worldofwarships.eu',
        'na': 'http://vortex.worldofwarships.com',
        'ru': 'http://vortex.korabli.su',
        'cn': 'http://vortex.wowsgame.cn'
    }
    return url_list[server]


class update_user_data:
    '''Get user data'''

    def __init__(self, data) -> None:
        self.account_id = data[0]
        self.server = data[1]

    def error_msg(self, msg: list) -> None:
        ship_data['status'] = msg[0]
        ship_data['message'] = msg[1]
        ship_data['error'] = msg[2]
        ship_data['params'] = msg[3]

    def user_info(self) -> dict:
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
            user_data = asyncio.run(self.request_user_data())
            if user_data['status'] != 'ok':
                ship_data['data']['user']['value'] = False
                ship_data['status'] = 'error'
                ship_data['error'] = user_data['error']
                ship_data['message'] = 'NOT FOUND'
                temp_data = ship_data
                del ship_data
                return temp_data
            ship_data['data']['user']['nickname'] = user_data['data'][str(
                self.account_id)]['name']
            if 'hidden_profile' in user_data['data'][str(self.account_id)]:
                ship_data['data']['user']['hidden'] = True

                temp_data = ship_data
                del ship_data
                return temp_data
            if user_data['data'][str(self.account_id)]['statistics'] == {}:
                temp_data = ship_data
                del ship_data
                return temp_data

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
            ship_data['data']['ship'] = self.data(
                ship_data['data']['ship'])
            ship_data['data']['achievements'] = self.achieve(
                ship_data['data']['achievements'])
            temp_data = ship_data
            del ship_data
            return temp_data
        except Exception as e:
            return {
                'status': 'error',
                'message': 'UNEXPECTED ERROR',
                'error': str(e),
                'data': {
                    'user': {
                        'hidden': False,
                        'value': True,
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
        url = server_url(self.server) + \
            '/api/accounts/{}/'.format(self.account_id)
        async with httpx.AsyncClient() as client:
            res = await client.get(url, timeout=10)
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
                url = server_url(self.server) + \
                    url_list[request_number].format(self.account_id)

                res = await client.get(url, timeout=10)
                result = res.json()

                if res.status_code != 200 and res.status_code != 404:
                    self.error_msg(
                        ['error', 'NETWORK ERROR', 'Status Code:'+str(res.status_code), url])
                    return None
            except:
                self.error_msg(['error', 'NETWORK ERROR',
                                'httpx connect error', url])
                return None

            battles_type_list = ['pvp', 'pvp_solo',
                                 'pvp_div2', 'pvp_div3', 'rank_solo']
            if request_number == 5 and 'data' not in result:
                ship_data['data']['clans'] = {'clan': {}}
                return None
            if 'data' not in result:
                self.error_msg(['error', 'NETWORK ERROR',
                               'httpx connect error', url])
                return None
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
                4288865200: 'PCH005_Support',
                4287816624: 'PCH006_Withering',
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

    def main(self, id, server):
        user_db_path = os.path.join(db_path, server, str(id))
        if os.path.exists(user_db_path):
            res = update_user_data((id, server)).user_info()
            today = date.today().strftime("%Y-%m-%d")
            # Update user data
            gzip_data = gzip.compress(
                bytes(str(res['data']), encoding='utf-8'))
            with open(os.path.join(db_path, server, str(id), (today+'.txt')), "wb") as fp:
                fp.write(gzip_data)
            fp.close()
            # if res['status'] == 'error':
            #     db_data[today] = res['data']
            #     new_data = True
            # else:
            #     if today not in db_data:
            #         db_data[today] = res['data']
            #         new_data = True
            #     elif db_data[today]['info'] == {} or res['data']['info'] == {}:
            #         db_data[today] = res['data']
            #         new_data = True
            #     elif db_data[today]['info']['last_battle_time'] == res['data']['info']['last_battle_time']:
            #         new_data = False
            #         pass
            #     else:
            #         db_data[today] = res['data']
            #         new_data = True
            # # Compress and save data
            # if new_data:
            #     gzip_data = gzip.compress(
            #         bytes(str(db_data), encoding='utf-8'))
            #     with open(user_db_path, "wb") as fp:
            #         fp.write(gzip_data)
            #     fp.close()
            # debug

            del res
        else:
            today = date.today().strftime("%Y-%m-%d")
            yesterday = (date.today() + timedelta(days=-1)
                         ).strftime("%Y-%m-%d")
            res = update_user_data((id, server)).user_info()
            os.mkdir(os.path.join(db_path, server, str(id)))
            gzip_data = gzip.compress(
                bytes(str(res['data']), encoding='utf-8'))
            with open(os.path.join(db_path, server, str(id), (today+'.txt')), "wb") as fp:
                fp.write(gzip_data)
            fp.close()
            with open(os.path.join(db_path, server, str(id), (yesterday+'.txt')), "wb") as fp:
                fp.write(gzip_data)
            fp.close()
            if debug:
                with open(os.path.join(db_path, server, str(id), (today+'.json')), 'w') as f:
                    f.write(json.dumps(res['data']))
                f.close()
            # today = date.today().strftime("%Y-%m-%d")
            # yesterday = (date.today() + timedelta(days=-1)
            #              ).strftime("%Y-%m-%d")
            # if res['status'] == 'error':
            #     db_data[yesterday] = res['data']
            #     db_data[today] = res['data']
            # else:
            #     db_data[yesterday] = res['data']
            #     db_data[today] = res['data']
            # gzip_data = gzip.compress(bytes(str(db_data), encoding='utf-8'))
            # with open(user_db_path, "wb") as fp:
            #     fp.write(gzip_data)
            # fp.close()
            del res


def db_main(user_list):
    user_num = 1
    start_time = time.time()
    for id, server in user_list:

        print("\r", end="")
        white_num = int(user_num/all_user*50)
        white = '▓'*white_num + '-'*(50-white_num)
        sys_mem = psutil.virtual_memory()
        mem = '%.2f MB' % (psutil.Process(
            os.getpid()).memory_info().rss / 1024 / 1024)
        print("  进度:{:.2f}% |{}| {}/{}  {}|{}  已耗时: {:.2f}s  程序占用:{}  总占用:{}%  可用:{:.2f}M ".format(user_num/all_user *
              100, white, user_num, all_user, server, id, time.time()-start_time, mem, sys_mem[2], sys_mem[1]/1024/1024))
        sys.stdout.flush()
        try:
            update_user_data((id, server)).main(id, server)
            gc.collect()
        except:
            print('{} 错误'.format(id))
        user_num += 1


if __name__ == '__main__':
    while cyc:
        if server != True:
            cyc = False
        print('================================================================================================================================================================')
        conn = sqlite3.connect(acc_path)
        c = conn.cursor()
        cursor = c.execute("SELECT ACCID,TIME,SERVER  from accid")
        user_list = list(cursor)
        all_user = len(user_list)
        conn.close()

        db_list = []
        for user in user_list:
            temp = (user[0], user[2])
            db_list.append(temp)
        user_list = db_list
        db_main(user_list)
        # all_user = 1
        # user_list = [(2023619512, 'asia')]
        gc.collect()
        print('================================================================================================================================================================')
        if datetime.datetime.now().hour == 23 or datetime.datetime.now().hour == 0:
            print('[休眠0s]')
        else:
            time.sleep(1800)
            print('[休眠1800s]')
