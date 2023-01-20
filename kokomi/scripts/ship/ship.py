import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import json
import httpx
import json
import threading
import asyncio
import os
import platform
import time
import gc

isWin = True if platform.system().lower() == 'windows' else False
file_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
png_path = os.path.dirname(__file__)


def check_memory():
    '''检查是否有内存泄漏'''
    gc.set_debug(gc.DEBUG_SAVEALL)
    gc.collect()
    unreachableL = []
    for it in gc.garbage:
        unreachableL.append(it)
    print(str(unreachableL))
    return len(unreachableL)


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


class ship:
    '''Request to obtain the detailed data of the specified ship'''

    def __init__(self, data) -> None:
        self.ship_id = str(data['ship_id'])
        self.account_id = str(data['account_id'])
        self.server = data['server']

    async def request_data(self, request_number) -> dict:
        type_list = ['pvp', 'pvp_solo', 'pvp_div2', 'pvp_div3', 'rank_solo']
        async with httpx.AsyncClient() as client:
            try:
                url = server_url(self.server) + '/api/accounts/{}/ships/{}/{}/'.format(
                    self.account_id, self.ship_id, type_list[request_number])
                res = await client.get(url, timeout=3)
                if res.status_code != 200:
                    self.error_msg(['error', 'NETWORK ERROR',
                                   'Status Code:'+str(res.status_code)])
                    return None
                result = res.json()
            except:
                self.error_msg(
                    ['error', 'NETWORK ERROR', 'httpx connect error'])
                return None
            if ship_data['status'] == 'ok':
                ship_data['nickname'] = result['data'][self.account_id]['name']
                if 'hidden_profile' in result['data'][self.account_id]:
                    ship_data['hidden'] = True
                    ship_data['data'] = {}
                elif result['data'][self.account_id]['statistics'] == {}:
                    ship_data['data'] = {}
                else:
                    original_data = result['data'][self.account_id]['statistics'][self.ship_id][type_list[request_number]]
                    ship_data['data'][type_list[request_number]
                                      ] = self.shipdata(original_data)
            elif result == None:
                self.error_msg(
                    ['error', 'NETWORK ERROR', 'httpx connect error'])
            else:
                self.error_msg(['error', 'STATUS ERROR', result['error']])
            return None

    def ship_info(self) -> dict:
        global ship_data
        ship_data = {
            'status': 'ok',
            'message': 'SUCCESS',
            'hidden': False,
            'nickname': None,
            'data': {
                'pvp': {},
                'pvp_solo': {},
                'pvp_div2': {},
                'pvp_div3': {},
                'rank_solo': {}
            }
        }
        thread = []
        for index in range(0, 5):
            thread.append(threading.Thread(
                target=self.ship2, args=(index,)))
        for t in thread:
            t.start()
        for t in thread:
            t.join()
        gc.collect()
        return ship_data

    def error_msg(self, msg: list) -> None:
        ship_data['status'] = msg[0]
        ship_data['message'] = msg[1]
        ship_data['error'] = msg[2]

    def ship2(self, request_number) -> None:
        asyncio.run(self.request_data(request_number))

    def shipdata(self, data) -> dict:
        ship_dict = {
            'battles': 0,
            'avg': {},
            'max': {},
            'point': {},
            'frag': {},
            'hit_rate': {}
        }
        if 'battles_count' not in data or data['battles_count'] == 0:
            return {}
        battles = data['battles_count']
        wins = data['wins']
        damage_dealt = data['damage_dealt']
        frags = data['frags']
        average_xp = int(data['original_exp']/battles)
        average_survived = round(data['survived']/battles*100, 2)
        average_art_agro = int(data['art_agro']/battles)
        average_tpd_agro = int(data['tpd_agro']/battles)
        average_planes_killed = round(data['planes_killed']/battles, 2)
        average_scouting_damage = int(data['scouting_damage']/battles)
        average_wins = round(wins/battles*100, 2)
        average_damage_dealt = int(damage_dealt/battles)
        average_frags = round(frags/battles, 2)
        for frag_type in ['main', 'skip', 'tpd', 'tbomb', 'bomb', 'atba', 'rocket']:
            tag = 'hit_rate_of_'+frag_type
            hits = data['hits_by_'+frag_type]
            shots = data['shots_by_'+frag_type]
            if shots == 0:
                hit_rate = 0.0
            else:
                hit_rate = round(hits/shots*100, 2)
            ship_dict['hit_rate'][tag] = hit_rate
        ship_dict['battles'] = battles
        ship_dict['avg']['wins'] = average_wins
        ship_dict['avg']['frags'] = average_frags
        ship_dict['avg']['damage_dealt'] = average_damage_dealt
        ship_dict['avg']['scouting_damage'] = average_scouting_damage
        ship_dict['avg']['planes_killed'] = average_planes_killed
        ship_dict['avg']['art_agro'] = average_art_agro
        ship_dict['avg']['tpd_agro'] = average_tpd_agro
        ship_dict['avg']['survived'] = average_survived
        ship_dict['avg']['xp'] = average_xp
        ship_dict['point']['control_dropped_points'] = data['control_dropped_points']
        ship_dict['point']['team_control_dropped_points'] = data['team_control_dropped_points']
        ship_dict['point']['control_captured_points'] = data['control_captured_points']
        ship_dict['point']['team_control_captured_points'] = data['team_control_captured_points']
        ship_dict['max']['frags'] = data['max_frags']
        ship_dict['max']['xp'] = data['max_exp']
        ship_dict['max']['total_agro'] = data['max_total_agro']
        ship_dict['max']['damage_dealt'] = data['max_damage_dealt']
        ship_dict['max']['ship_spotted'] = data['max_ships_spotted']
        ship_dict['max']['planes_killed'] = data['max_planes_killed']
        ship_dict['max']['scouting_damage'] = data['max_scouting_damage']
        ship_dict['max']['frags_by_tpd'] = data['max_frags_by_tpd']
        ship_dict['max']['frags_by_atba'] = data['max_frags_by_atba']
        ship_dict['max']['frags_by_dbomb'] = data['max_frags_by_dbomb']
        ship_dict['max']['frags_by_main'] = data['max_frags_by_main']
        ship_dict['max']['frags_by_ram'] = data['max_frags_by_ram']
        ship_dict['max']['frags_by_planes'] = data['max_frags_by_planes']
        ship_dict['frag']['planes'] = data['frags_by_planes']
        ship_dict['frag']['ram'] = data['frags_by_ram']
        ship_dict['frag']['dbomb'] = data['frags_by_dbomb']
        ship_dict['frag']['atba'] = data['frags_by_atba']
        ship_dict['frag']['main'] = data['frags_by_main']
        return ship_dict


class data:
    '''返回clan,user,ship数据'''

    def __init__(self) -> None:
        pass

    def claninfo(self, server, account_id):
        ship_data['clan'] = asyncio.run(self.clan_info(server, account_id))

    async def clan_info(self, server: str, account_id: int):
        '''Return the information of the player'''
        async with httpx.AsyncClient() as client:
            try:
                url = server_url(server) + \
                    '/api/accounts/{}/clans/'.format(account_id)
                res = await client.get(url, timeout=3)
                if res.status_code != 200:
                    return {'status': 'error', 'message': 'NETWORK ERROR', 'error': 'Status Code:'+str(res.status_code)}
                result = res.json()
            except:
                return {'status': 'error', 'message': 'NETWORK ERROR', 'error': 'httpx connect error'}
            if result['status'] == 'ok':
                if result['data']['clan'] == {}:
                    res = {'status': 'ok', 'message': 'SUCCESS', 'data': {}}
                else:
                    res = {
                        'status': 'ok',
                        'message': 'SUCCESS',
                        'data': {
                            'tag': result['data']['clan']['tag'],
                            'name': result['data']['clan']['name'],
                            'clan_id': result['data']['clan_id'],
                            'clan_color': result['data']['clan']['color'],
                            'role': result['data']['role']
                        }
                    }
            else:
                res = {'status': 'error', 'message': 'STATUS ERROR',
                       'error': result['error']}
            return res

    def userinfo(self, server, account_id):
        ship_data['user'] = asyncio.run(self.user_info(server, account_id))

    async def user_info(self, server: str, account_id: int):
        async with httpx.AsyncClient() as client:
            try:
                url = server_url(server) + \
                    '/api/accounts/{}/'.format(account_id)
                res = await client.get(url, timeout=3)
                if res.status_code != 200:
                    return {'status': 'error', 'message': 'NETWORK ERROR', 'error': 'Status Code:'+str(res.status_code)}
                result = res.json()
            except:
                return {'status': 'error', 'message': 'NETWORK ERROR', 'error': 'httpx connect error'}
            if result['status'] == 'ok':
                if 'hidden_profile' in result['data'][str(account_id)]:
                    res = {'status': 'ok', 'hidden': True,
                           'message': 'SUCCESS', 'data': {}}
                elif result['data'][str(account_id)]['statistics'] == {}:
                    res = {'status': 'ok', 'hidden': False,
                           'message': 'NO DATA', 'data': {}}
                else:
                    res = {
                        'status': 'ok',
                        'hidden': False,
                        'message': 'SUCCESS',
                        'data': {
                            "name": result['data'][str(account_id)]['name'],
                            "basic": result['data'][str(account_id)]['statistics']['basic'],
                            "dog_tag": result['data'][str(account_id)]['dog_tag']
                        }
                    }
            else:
                res = {'status': 'error', 'message': 'STATUS ERROR',
                       'error': result['error']}
            return res

    def shipinfo(self, server, account_id, ship_id):
        ship_data['ship'] = asyncio.run(
            self.ship_info(server, account_id, ship_id))

    async def ship_info(self, server: str, account_id: int, ship_id: int):
        params = {'account_id': account_id,
                  'ship_id': ship_id, 'server': server}
        if server not in ['asia', 'na', 'eu', 'ru', 'cn']:
            return {'status': 'error', 'message': 'INVALID_SEARCH'}
        statistics_data = ship(params).ship_info()
        if statistics_data['status'] != 'ok':
            statistics_data['data'] = {}
            return statistics_data
        else:
            return statistics_data

    def info(self, server, account_id, ship_id) -> dict:
        global ship_data
        ship_data = {
            'clan': {},
            'ship': {},
            'user': {}
        }
        thread1 = threading.Thread(
            target=self.claninfo, args=(server, account_id))
        thread2 = threading.Thread(
            target=self.userinfo, args=(server, account_id))
        thread3 = threading.Thread(
            target=self.shipinfo, args=(server, account_id, ship_id))
        thread1.start()
        thread2.start()
        thread3.start()
        thread1.join()
        thread2.join()
        thread3.join()
        gc.collect()
        return ship_data


class pic:
    def __init__(self, info) -> None:
        '''导入计算所需数据'''
        shipdata = data().info(info[0], info[1], info[2])
        self.result_data = shipdata['ship']
        self.ship_info_data = json.load(
            open(os.path.join(file_path, 'data', 'ship_name.json'), "r", encoding="utf-8"))
        self.ship_server_data = json.load(
            open(os.path.join(file_path, 'data', 'server.json'), "r", encoding="utf-8"))
        # self.dog_tag_data = json.load(open(
        #     file_path + (r'\dog_tag.json' if isWin else r'/dog_tag.json'), "r", encoding="utf-8"))
        self.clan_data = shipdata['clan']
        self.user_data = shipdata['user']
        self.account_id = info[1]
        self.ship_id = info[2]
        self.server = info[0]
        font1_path = os.path.join(
            file_path, 'data', 'SourceHanSansCN-Bold.ttf') if isWin else os.path.join('/usr/share/fonts', 'NZBZ.ttf')
        font2_path = os.path.join(file_path, 'data', 'SourceHanSansCN-Bold.ttf') if isWin else os.path.join(
            '/usr/share/fonts', 'SourceHanSansCN-Bold.ttf')
        self.font = {
            1: {
                60: ImageFont.truetype(font1_path, 60, encoding="utf-8"),
                80: ImageFont.truetype(font1_path, 80, encoding="utf-8"),
                90: ImageFont.truetype(font1_path, 90, encoding="utf-8")
            },
            2: {
                48: ImageFont.truetype(font2_path, 48, encoding="utf-8"),
                60: ImageFont.truetype(font2_path, 60, encoding="utf-8"),
                70: ImageFont.truetype(font2_path, 70, encoding="utf-8"),
                72: ImageFont.truetype(font2_path, 72, encoding="utf-8"),
                80: ImageFont.truetype(font2_path, 80, encoding="utf-8"),
                90: ImageFont.truetype(font2_path, 90, encoding="utf-8"),
                100: ImageFont.truetype(font2_path, 100, encoding="utf-8"),
                140: ImageFont.truetype(font2_path, 120, encoding="utf-8"),
                160: ImageFont.truetype(font2_path, 160, encoding="utf-8")

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

    async def main(self) -> dict:
        '''主函数'''
        res = {
            'status': 'ok',
            'hidden': False,
            'message': 'SUCCESS'
        }
        # user info
        user_data = self.user_data
        if user_data['status'] == 'ok' and user_data['message'] == 'SUCCESS':
            if user_data['hidden'] or user_data['data'] == {}:
                res['hidden'] = True
                return res
            else:
                self.user_info(user_data)
        else:
            return user_data
        # clan info
        clan_data = self.clan_data
        if clan_data['status'] == 'ok' and clan_data['message'] == 'SUCCESS':
            self.clan_info(clan_data)
        else:
            return clan_data
        # ship info
        ship_info_data = self.ship_info_data
        if str(self.ship_id) in ship_info_data:
            img = self.ship_info(ship_info_data[str(self.ship_id)])
        else:
            return {'status': 'error', 'hidden': False, 'message': 'UNKNOW SHIP', 'error': 'ship id not found'}
        # 船只服务器数据
        ship_server_data = self.ship_server_data['data']
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
        if str(self.ship_id) not in ship_server_data and str(self.ship_id) not in ss_server:
            server_data = {
                'battles_count': 0,
                'avg_wins': 0,
                'avg_damage': 0,
                'avg_frags': 0,
                'avg_xp': 0,
                'avg_planes': 0,
                'avg_argo': 0,
                'avg_scout': 0,
                'avg_hit': 0,
                'avg_survived': 0
            }
        else:
            if str(self.ship_id) not in ss_server:
                ship_data = ship_server_data[str(self.ship_id)]
            else:
                ship_data = ss_server[str(self.ship_id)]
            server_data = {
                'battles_count': 1,
                'avg_wins': ship_data['win_rate']/100,
                'avg_damage': ship_data['average_damage_dealt'],
                'avg_frags': ship_data['average_frags'],
                'avg_xp': 1,
                'avg_planes': 1,
                'avg_argo': 1,
                'avg_scout': 1,
                'avg_hit': 1,
                'avg_survived': 1
            }
        result_data = self.result_data
        if result_data['data'] == {}:
            return {'status': 'ok', 'hidden': False, 'message': 'NO DATA'}
        img = self.pvp_info(img, server_data, result_data['data']['pvp'])
        img = self.type_info(
            img, server_data, result_data['data']['pvp_solo'], 0)
        img = self.type_info(
            img, server_data, result_data['data']['pvp_div2'], 1)
        img = self.type_info(
            img, server_data, result_data['data']['pvp_div3'], 2)
        img = self.rank_info(
            img, server_data, result_data['data']['rank_solo'])
        img = self.add_text(img)

        img = cv2.resize(img, None, fx=0.4, fy=0.4)
        png_out_path = os.path.join(file_path, 'temp', '1-{}.png'.format(
            png_name().generate_name(str(int(time.time()*100000)))))
        cv2.imwrite(png_out_path, img)
        res['img'] = png_out_path
        del img
        gc.collect()
        return res

    def user_info(self, user_data):
        # user info 数据
        # # dog_tag
        # dog_tag_data = self.dog_tag_data
        # doll_id = user_data['data']['dog_tag']['doll_id']
        # png_path = (png_path + r'\dogtag\{}.png' if isWin else r'/dogtag/{}.png').format(
        #     dog_tag_data[str(doll_id)]['index'])
        # img_jpg = cv2.imread(background_path, cv2.IMREAD_UNCHANGED)
        # img_png = cv2.imread(png_path, cv2.IMREAD_UNCHANGED)
        # img_png = cv2.resize(img_png, None, fx=2.58, fy=2.58)
        # x1 = 54
        # y1 = 53
        # x2 = x1 + img_png.shape[1]
        # y2 = y1 + img_png.shape[0]
        # res_img = self.merge_img(img_jpg, img_png, y1, y2, x1, x2)
        # if user_data['data']['dog_tag']['slots'] != {}:
        #     slots = user_data['data']['dog_tag']['slots']['1']
        #     png_path = (png_path + r'\dogtag\{}.png' if isWin else r'/dogtag/{}.png').format(
        #         dog_tag_data[str(slots)]['index'])
        #     img_jpg = cv2.imread(background_path, cv2.IMREAD_UNCHANGED)
        #     img_png = cv2.imread(png_path, cv2.IMREAD_UNCHANGED)
        #     img_png = cv2.resize(img_png, None, fx=2.58, fy=2.58)
        #     x1 = 54
        #     y1 = 53
        #     x2 = x1 + img_png.shape[1]
        #     y2 = y1 + img_png.shape[0]
        #     res_img = self.merge_img(img_jpg, img_png, y1, y2, x1, x2)

        nickname = user_data['data']['name']
        self.text_list.append([(329, 181), nickname, (255, 255, 255), 2, 140])
        # self.text_list.append([(601, 208), '{}    {}'.format(
        #     self.server.upper(), self.account_id), (255, 255, 255), 2, 40])

    def clan_info(self, clan_data):
        '''clan info 写入'''
        if clan_data['data'] == {}:
            self.text_list.append(
                [(1697, 448), 'None', (255, 255, 255), 2, 100])
        else:
            data_dict = {
                'commander': '指挥官',
                'executive_officer': '副指挥官',
                'recruitment_officer': '征募官',
                'commissioned_officer': '现役军官',
                'officer': '前线军官',
                'private': '军校见习生'
            }
            clan_name = '[{}]{}'.format(
                clan_data['data']['tag'], clan_data['data']['name'])
            clan_name = clan_name + '\n  '+data_dict[clan_data['data']['role']]
            self.text_list.append(
                [(421, 377), clan_name, (255, 255, 255), 2, 70])

    def ship_info(self, ship_data):
        '''船只信息及图片'''
        tier = ship_data['tier']
        type = ship_data['type']
        nation = ship_data['nation']
        name = ship_data['name'].split('_')[0]
        name_zh = ship_data['ship_name']['zh_sg']
        type_dict = {
            'AirCarrier': 'CV',
            'Battleship': 'BB',
            'Cruiser': 'CA',
            'Destroyer': 'DD',
            'Submarine': 'SS'
        }
        background_path = os.path.join(png_path, 'bg.jpg')
        ship_png_path = os.path.join(
            file_path, 'wows_ico', 'ship_large', '{}.png'.format(name))
        nation_png_path = os.path.join(
            file_path, 'wows_ico', 'nation', 'large', 'flag_{}.png'.format(name))
        if os.path.exists(nation_png_path) != True:
            nation_png_path = os.path.join(
                file_path, 'wows_ico', 'nation', 'large', 'flag_{}.png'.format(nation))
        type_png_path = os.path.join(
            png_path, 'type_icons', '{}.png'.format(type))
        res_img = cv2.imread(background_path, cv2.IMREAD_UNCHANGED)
        nation_png = cv2.imread(nation_png_path, cv2.IMREAD_UNCHANGED)
        nation_png = cv2.resize(nation_png, None, fx=1.6, fy=1.6)
        ship_png = cv2.imread(ship_png_path, cv2.IMREAD_UNCHANGED)
        ship_png = cv2.resize(ship_png, None, fx=1.4, fy=1.4)
        type_png = cv2.imread(type_png_path, cv2.IMREAD_UNCHANGED)
        type_png = cv2.resize(type_png, None, fx=1.4, fy=1.4)
        x1 = 242
        y1 = 1006
        x2 = x1 + nation_png.shape[1]
        y2 = y1 + nation_png.shape[0]
        res_img = self.merge_img(res_img, nation_png, y1, y2, x1, x2)
        x1 = 362
        y1 = 905
        x2 = x1 + ship_png.shape[1]
        y2 = y1 + ship_png.shape[0]
        res_img = self.merge_img(res_img, ship_png, y1, y2, x1, x2)
        x1 = 692
        y1 = 1655
        x2 = x1 + type_png.shape[1]
        y2 = y1 + type_png.shape[0]
        res_img = self.merge_img(res_img, type_png, y1, y2, x1, x2)
        self.text_list.append(
            [(283, 1645), 'T {}'.format(tier), (255, 255, 255), 2, 72])
        self.text_list.append(
            [(536, 1645), type_dict[type], (255, 255, 255), 2, 72])
        fontStyle = self.font[2][160]
        w = self.x_coord(name_zh, fontStyle)
        if w >= 1370:
            del_len = int(((w-1370)/w)*len(name_zh))
            name_zh = name_zh[:(len(name_zh)-del_len-1)]+'...'
        self.text_list.append([(285, 744), name_zh, (255, 255, 255), 2, 160])

        return res_img

    def number_pr(self, server_data, ship_data) -> dict:
        '''返回pr info'''
        if server_data['battles_count'] == 0 or ship_data['battles'] == 0:
            return(-1, -1, -1, -1, -1, -1)
        average_damage_dealt = ship_data['avg']['damage_dealt']
        average_wins = ship_data['avg']['wins']
        average_kd = ship_data['avg']['frags']
        average_xp = ship_data['avg']['xp']
        average_plane = ship_data['avg']['planes_killed']
        server_damage_dealt = server_data['avg_damage']
        server_frags = server_data['avg_frags']
        server_wins = server_data['avg_wins']*100
        server_xp = server_data['avg_xp']
        server_plane = server_data['avg_planes']
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
        pr = int(700*n_damage+300*n_kd+150*n_win_rate) + 1
        return (pr, average_wins, average_damage_dealt/server_damage_dealt, average_kd/server_frags, average_xp/server_xp, average_plane/server_plane)

    def number_pr2(self, server_data, ship_data) -> dict:
        '''返回pr info'''
        if server_data['battles_count'] == 0 or ship_data['battles'] == 0:
            return(-1, -1, -1, -1, -1, -1)
        average_damage_dealt = ship_data['avg']['damage_dealt']
        average_wins = ship_data['avg']['wins']
        average_kd = ship_data['avg']['frags']
        server_damage_dealt = server_data['avg_damage']
        server_frags = server_data['avg_frags']
        server_wins = server_data['avg_wins']*100
        return (server_wins, server_damage_dealt, server_frags, average_wins-server_wins, average_damage_dealt-server_damage_dealt, average_kd-server_frags)

    def pvp_info(self, res_img, server_data, pvp_data):
        '''pvp数据写入'''
        if pvp_data == {} or pvp_data['battles'] == 0:
            pvp_data = {
                "battles": 0,
                "avg": {
                    "wins": 0.00,
                    "frags": 0.00,
                    "damage_dealt": 0,
                    "scouting_damage": 0,
                    "planes_killed": 0,
                    "art_agro": 0,
                    "tpd_agro": 0,
                    "survived": 0.00,
                    "xp": 0
                },
                "max": {
                    "frags": 0,
                    "xp": 0,
                    "total_agro": 0,
                    "damage_dealt": 0,
                    "ship_spotted": 0,
                    "planes_killed": 0,
                    "scouting_damage": 0,
                    "frags_by_tpd": 0,
                    "frags_by_atba": 0,
                    "frags_by_dbomb": 0,
                    "frags_by_main": 0,
                    "frags_by_ram": 0,
                    "frags_by_planes": 0
                },
                "point": {
                    "control_dropped_points": 0,
                    "team_control_dropped_points": 0,
                    "control_captured_points": 0,
                    "team_control_captured_points": 0
                },
                "hit_rate": {
                    "hit_rate_of_main": 0.0,
                    "hit_rate_of_skip": 0.0,
                    "hit_rate_of_tpd": 0.0,
                    "hit_rate_of_tbomb": 0.0,
                    "hit_rate_of_bomb": 0.0,
                    "hit_rate_of_atba": 0.0,
                    "hit_rate_of_rocket": 0.0
                }
            }
        pr_data = self.number_pr(server_data, pvp_data)
        pr_data2 = self.number_pr2(server_data, pvp_data)
        res_img = self.main_pr(res_img, pr_data[0])
        i = 1
        while i <= 3:
            img_path = os.path.join(png_path, 'num_pr', '{}.png'.format(
                self.color_box(i-1, pr_data[i])[0]))
            img_png = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
            x1 = 2786
            y1 = 1307 + 220*(i-1)
            x2 = x1 + img_png.shape[1]
            y2 = y1 + img_png.shape[0]
            res_img = self.merge_img(res_img, img_png, y1, y2, x1, x2)
            fontStyle = self.font[1][60]
            if i == 2:
                add_data = int(pr_data2[i-1+3])
                avg_data = int(pr_data2[i-1])
            else:
                add_data = round(pr_data2[i-1+3], 2)
                avg_data = round(pr_data2[i-1], 2)
            if add_data >= 0:
                w = self.x_coord('+'+str(add_data), fontStyle)
                self.text_list.append(
                    [(3746-w, 1416+220*(i-1)), '+'+str(add_data), (103, 205, 52), 1, 60])
            else:
                w = self.x_coord(str(add_data), fontStyle)
                self.text_list.append(
                    [(3746-w+4, 1416+220*(i-1)), str(add_data), (205, 51, 51), 1, 60])
            w2 = self.x_coord(str(avg_data), fontStyle)
            self.text_list.append(
                [(3746-w2 - w - 10, 1416+220*(i-1)), str(avg_data), (236, 255, 255), 1, 60])
            i += 1
        pvpdata = [
            '{:,}'.format(pvp_data['battles']),
            '{}%'.format(pvp_data['avg']['wins']),
            '{:,}'.format(pvp_data['avg']['damage_dealt']),
            '{:.2f}'.format(pvp_data['avg']['frags']),
            '{:,}'.format(int(pvp_data['avg']['xp'])),
            '{:.2f}'.format(pvp_data['avg']['planes_killed']),
            '{}%'.format(pvp_data['hit_rate']['hit_rate_of_main']),
            '{}%'.format(pvp_data['avg']['survived'])
        ]
        maxdata = [
            '{:,}'.format(pvp_data['max']['damage_dealt']),
            '{:,}'.format(pvp_data['max']['frags']),
            '{:,}'.format(int(pvp_data['max']['xp'])),
            '{:,}'.format(pvp_data['max']['planes_killed'])
        ]
        fontStyle = self.font[1][90]
        i = 0
        for index in pvpdata:
            w = self.x_coord(index, fontStyle)
            self.text_list.append([(3746-w+4, 1089+220*i+4+2), index,
                                   (0, 0, 0), 1, 90])
            self.text_list.append([(3746-w, 1089+220*i+2), index,
                                   (236, 255, 255), 1, 90])
            i += 1
        i = 0
        for index in maxdata:
            w = self.x_coord(index, fontStyle)
            self.text_list.append([(1900-w+4, 1089+220*(i+4)+4+2), index,
                                   (0, 0, 0), 1, 90])
            self.text_list.append([(1900-w, 1089+220*(i+4)+2), index,
                                   (236, 255, 255), 1, 90])
            i += 1
        return res_img

    def type_info(self, res_img, server_data, pvp_data, num):
        '''pvp type 数据'''
        if pvp_data == {} or pvp_data['battles'] == 0:
            pvp_data = {
                "battles": 0,
                "avg": {
                    "wins": 0.00,
                    "frags": 0.00,
                    "damage_dealt": 0,
                    "scouting_damage": 0,
                    "planes_killed": 0,
                    "art_agro": 0,
                    "tpd_agro": 0,
                    "survived": 0.00,
                    "xp": 0
                },
                "max": {
                    "frags": 0,
                    "xp": 0,
                    "total_agro": 0,
                    "damage_dealt": 0,
                    "ship_spotted": 0,
                    "planes_killed": 0,
                    "scouting_damage": 0,
                    "frags_by_tpd": 0,
                    "frags_by_atba": 0,
                    "frags_by_dbomb": 0,
                    "frags_by_main": 0,
                    "frags_by_ram": 0,
                    "frags_by_planes": 0
                },
                "point": {
                    "control_dropped_points": 0,
                    "team_control_dropped_points": 0,
                    "control_captured_points": 0,
                    "team_control_captured_points": 0
                },
                "hit_rate": {
                    "hit_rate_of_main": 0.0,
                    "hit_rate_of_skip": 0.0,
                    "hit_rate_of_tpd": 0.0,
                    "hit_rate_of_tbomb": 0.0,
                    "hit_rate_of_bomb": 0.0,
                    "hit_rate_of_atba": 0.0,
                    "hit_rate_of_rocket": 0.0
                }
            }
        pr_data = self.number_pr(server_data, pvp_data)
        res_img = self.pvp_type_pr(res_img, pr_data[0], num)
        pvpdata = [
            '{:,}'.format(pvp_data['battles']),
            '{:,}'.format(pvp_data['avg']['damage_dealt']),
            '{}%'.format(pvp_data['avg']['wins']),
            '{:.2f}'.format(pvp_data['avg']['frags'])
        ]

        i = 0
        for index in pvpdata:
            x = int(i / 2)
            y = int(i % 2)
            self.text_list.append([(4632+546*x, 738+402*num+139*y), index,
                                   (236, 255, 255), 1, 80])
            i += 1
        return res_img

    def rank_info(self, res_img, server_data, pvp_data):
        '''rank 数据'''
        if pvp_data == {} or pvp_data['battles'] == 0:
            pvp_data = {
                "battles": 0,
                "avg": {
                    "wins": 0.00,
                    "frags": 0.00,
                    "damage_dealt": 0,
                    "scouting_damage": 0,
                    "planes_killed": 0,
                    "art_agro": 0,
                    "tpd_agro": 0,
                    "survived": 0.00,
                    "xp": 0
                },
                "max": {
                    "frags": 0,
                    "xp": 0,
                    "total_agro": 0,
                    "damage_dealt": 0,
                    "ship_spotted": 0,
                    "planes_killed": 0,
                    "scouting_damage": 0,
                    "frags_by_tpd": 0,
                    "frags_by_atba": 0,
                    "frags_by_dbomb": 0,
                    "frags_by_main": 0,
                    "frags_by_ram": 0,
                    "frags_by_planes": 0
                },
                "point": {
                    "control_dropped_points": 0,
                    "team_control_dropped_points": 0,
                    "control_captured_points": 0,
                    "team_control_captured_points": 0
                },
                "hit_rate": {
                    "hit_rate_of_main": 0.0,
                    "hit_rate_of_skip": 0.0,
                    "hit_rate_of_tpd": 0.0,
                    "hit_rate_of_tbomb": 0.0,
                    "hit_rate_of_bomb": 0.0,
                    "hit_rate_of_atba": 0.0,
                    "hit_rate_of_rocket": 0.0
                }
            }
        pr_data = self.number_pr(server_data, pvp_data)
        res_img = self.rank_type_pr(res_img, pr_data[0])
        pvpdata = [
            '{:,}'.format(pvp_data['battles']),
            '{:,}'.format(pvp_data['avg']['damage_dealt']),
            '{}%'.format(pvp_data['avg']['wins']),
            '{:.2f}'.format(pvp_data['avg']['frags'])
        ]
        i = 0
        for index in pvpdata:
            x = int(i / 2)
            y = int(i % 2)
            self.text_list.append([(4632+546*x, 738+402*3+139*y), index,
                                   (236, 255, 255), 1, 80])
            i += 1
        return res_img

    def color_box(self, index: int, num: float):
        '''自上向下 win dmg frag xp plane_kill'''
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
            return [8, (64, 16, 112)]
        elif num >= data[1] and num < data[0]:
            return [7, (121, 61, 182)]
        elif num >= data[2] and num < data[1]:
            return [6, (57, 114, 198)]
        elif num >= data[3] and num < data[2]:
            return [5, (49, 128, 0)]
        elif num >= data[4] and num < data[3]:
            return [4, (68, 179, 0)]
        elif num >= data[5] and num < data[4]:
            return [3, (255, 199, 31)]
        elif num >= data[6] and num < data[5]:
            return [2, (254, 121, 3)]
        elif num < data[6]:
            return [1, (205, 51, 51)]

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
            return [3, (255, 199, 31), '距离下一评级：+', 0, int(1350-pr), '平均水平']
        elif pr >= 1350 and pr < 1550:
            return [4, (68, 179, 0), '距离下一评级：+', -3, int(1550-pr), '好']
        elif pr >= 1550 and pr < 1750:
            return [5, (49, 128, 0), '距离下一评级：+', -2, int(1750-pr), '很好']
        elif pr >= 1750 and pr < 2100:
            return [6, (57, 114, 198), '距离下一评级：+', -1, int(2100-pr), '非常好']
        elif pr >= 2100 and pr < 2450:
            return [7, (121, 61, 182), '距离下一评级：+', 0, int(2450-pr), '大佬平均']
        elif pr >= 2450:
            return [8, (64, 16, 112), '已超过最高评级：+', 0, int(pr-2450), '神佬平均']

    def main_pr(self, res_img, pr):
        '''主pr条'''
        pr_data = self.pr_info(pr)
        pr_path = os.path.join(png_path, 'pr',
                               '{}.png'.format(pr_data[0]))
        img_png = cv2.imread(pr_path, cv2.IMREAD_UNCHANGED)
        # img_png = cv2.resize(img_png, None, fx=0.832, fy=0.832)
        x1 = 2134
        y1 = 742
        x2 = x1 + img_png.shape[1]
        y2 = y1 + img_png.shape[0]
        res_img = self.merge_img(res_img, img_png, y1, y2, x1, x2)
        fontStyle = self.font[2][80]
        str_pr = '{:,}'.format(int(pr))
        if len(str_pr) >= 5:
            str_pr = str_pr.replace(',', ' ')
        w = self.x_coord(str_pr, fontStyle)
        self.text_list.append([(3680-w, 767), str_pr, (255, 255, 255), 2, 90])
        self.text_list.append([(2183, 912), (pr_data[2] +
                                             str(pr_data[4])), (255, 255, 255), 2, 60])
        return res_img

    def pvp_type_pr(self, res_img, pr, num):
        '''pvp_pr条'''
        pr_data = self.pr_info(pr)
        pr_path = os.path.join(png_path, 'type_pr',
                               '{}.png'.format(pr_data[0]))
        img_png = cv2.imread(pr_path, cv2.IMREAD_UNCHANGED)
        x1 = 3926
        y1 = 700 + 401*num
        x2 = x1 + img_png.shape[1]
        y2 = y1 + img_png.shape[0]
        res_img = self.merge_img(res_img, img_png, y1, y2, x1, x2)
        str_pr = '+{}'.format(pr_data[4])
        fontStyle = self.font[1][80]
        w = self.x_coord(str_pr, fontStyle)
        self.text_list.append(
            [(4425-w, 806+402*num), str_pr, (255, 255, 255), 1, 80])
        return res_img

    def rank_type_pr(self, res_img, pr):
        '''rank_pr条'''
        pr_data = self.pr_info(pr)
        pr_path = os.path.join(png_path, 'type_pr',
                               '{}.png'.format(pr_data[0]))
        img_png = cv2.imread(pr_path, cv2.IMREAD_UNCHANGED)
        x1 = 3926
        y1 = 1905
        x2 = x1 + img_png.shape[1]
        y2 = y1 + img_png.shape[0]
        res_img = self.merge_img(res_img, img_png, y1, y2, x1, x2)
        str_pr = '+{}'.format(pr_data[4])
        fontStyle = self.font[1][80]
        w = self.x_coord(str_pr, fontStyle)
        self.text_list.append([(4425-w, 2011), str_pr, (255, 255, 255), 1, 80])
        return res_img

    def add_text(self, res_img):
        if (isinstance(res_img, np.ndarray)):
            res_img = Image.fromarray(cv2.cvtColor(res_img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(res_img)
        for index in self.text_list:
            fontStyle = self.font[index[3]][index[4]]
            draw.text(index[0], index[1], index[2], font=fontStyle)
        res_img = cv2.cvtColor(np.asarray(res_img), cv2.COLOR_RGB2BGR)
        del draw
        return res_img


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


# print(asyncio.run(pic(['asia', 2023619512, 4181604048]).main()))
