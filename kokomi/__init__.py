import requests
import datetime
import httpx
import gc
import sqlite3
from datetime import date, timedelta
import platform
import json
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message, MessageSegment, Event
from nonebot.typing import T_State
from nonebot import on_startswith
import os
import yaml
from .scripts.ship import ship
from .scripts.recent import recent
from .scripts.contribution import contribution
from .scripts.monitor import monitor
from .scripts.name import name
from .scripts.set import set


isWin = True if platform.system().lower() == 'windows' else False
file_path = os.path.join(os.path.dirname(__file__), 'data')
user_id_path = os.path.join(os.path.dirname(__file__), 'data', 'userid.db')
#user_id_path = '/home/QQbot_linux/kokomi/src/plugins/nonebot_kokomi_plugin/shipdata/userid.db'
png_path = os.path.dirname(__file__)
server_data_path = os.path.join(
    os.path.dirname(__file__), 'data', 'server.json')


f = open(os.path.join(os.path.dirname(__file__), 'config.yaml'))
config_data = yaml.load(f.read(), Loader=yaml.FullLoader)
f.close()
SUPERUSER = config_data['BotConfig']['Superuser']
DEBUG = config_data['BotConfig']['Error_report']


wwsmeship = on_startswith({'wws me ship'})


@wwsmeship.handle()
async def me_ship(bot: Bot, event: Event, state: T_State):
    user_qqid = event.get_user_id()
    info_message = str(event.get_message())
    server_log().add_data()
    if 'rank' in info_message or 'recent' in info_message:
        await wwsmeship.finish()
    ship_name = ''.join(info_message.replace('wws me ship', '').split())
    account_id, server, pic_type = tool.get_account_id(user_qqid)
    if account_id == 0:
        await wwsmeship.finish(Message('未绑定账号，请先绑定，示例wws asia set your_id'))
    seach_res = seach().seach_name(ship_name)
    if seach_res['ship_id'] != None:
        ship_id = seach_res['ship_id']
    else:
        await wwsmeship.finish(Message('未查询到船只,您可以通过wws seach [type]查询船只名称及别名'))
    try:
        res = await ship.pic([server, account_id, ship_id]).main()
    except Exception as e:
        res = {'status': 'error', 'hidden': False,
               'message': 'UNKNOW ERROR', 'error': str(e)}
    gc.collect()
    if res['hidden']:
        await wwsmeship.finish(Message('该账号隐藏了战绩'))
    elif res['status'] == 'ok' and res['message'] == 'NO DATA':
        await wwsmeship.finish(Message('您在该船只上没有战斗记录'))
    elif res['status'] == 'ok' and res['message'] == 'SUCCESS':
        try:
            await wwsmeship.send(MessageSegment.image("file:///"+res['img']))
        except:
            if DEBUG:
                await bot.send_private_msg(user_id=SUPERUSER, message='ship发生错误，消息发送失败')
            else:
                await wwsmeship.finish()
        os.remove(res['img'])
    elif res['status'] == 'error' and res['message'] == 'NETWORK ERROR':
        await wwsmeship.finish(Message('网络错误，请稍后重试'))
    elif res['status'] == 'error' and res['message'] == 'STATUS ERROR':
        await wwsmeship.finish(Message('请求错误，请稍后重试'))
    else:
        canshu = {
            'accid': account_id,
            'server': server,
            'shipid': ship_id,
            'res': res
        }
        if DEBUG:
            await bot.send_private_msg(user_id=SUPERUSER, message='ship发生错误，参数：'+str(canshu))
        else:
            await wwsmeship.finish()
        await wwsmeship.finish(Message('呜呜呜，好像哪里坏掉了(该bug已上报,将会及时处理)'))


wwsupdate = on_startswith({'wws update'})


@wwsupdate.handle()
async def update_data(bot: Bot, event: Event, state: T_State):
    user_qqid = event.get_user_id()
    if int(user_qqid) != SUPERUSER:
        await wwsmeship.finish(Message('权限不足'))
    res = await update().update_name()
    gc.collect()
    if res['status'] == 'ok':
        await wwsmeship.finish(Message('更新完成'))
    else:
        await wwsmeship.finish(Message('更新失败，参数：'+str(res)))

wwsmerecent = on_startswith({'wws me recent'})


@wwsmerecent.handle()
async def me_recent(bot: Bot, event: Event, state: T_State):
    user_qqid = event.get_user_id()
    info_message = str(event.get_message())
    server_log().add_data()
    date = ''.join(info_message.replace('wws me recent', '').split())
    if info_message in ['wws me recent ', 'wws me recent']:
        date = 1
    account_id, server, pic_type = tool.get_account_id(user_qqid)
    if account_id == 0:
        await wwsmerecent.finish(Message('未绑定账号，请先绑定，示例wws asia set your_id'))
    try:
        date = int(date)
    except:
        await wwsmerecent.finish(Message('命令格式错误'))
    if date >= 120:
        await wwsmerecent.finish(Message('由于服务器云硬盘大小限制，最多只能储存120天的数据'))
    try:
        res = recent.pic().main('pvp', await recent.recent((account_id, server, date)).recent_data())
    except Exception as e:
        res = {'status': 'error', 'hidden': False,
               'message': 'UNKNOW ERROR', 'error': str(e)}
    gc.collect()
    # try:
    if res['status'] == 'ok' and res['message'] == 'Hidden profile':
        await wwsmerecent.finish(Message('无有效数据或隐藏了战绩'))
    elif res['status'] == 'error' and res['message'] == 'Network Error':
        await wwsmerecent.finish(Message('数据更新失败，请稍后尝试'))
    elif res['status'] == 'error' and res['message'] == 'New User':
        await wwsmerecent.finish(Message('由于后台数据更新需要一段时间，新绑定的账号无法立即查询recent'))
    elif res['status'] == 'ok' and res['message'] == 'Recent data is None':
        await wwsmerecent.finish(Message('该日期范围内没有战斗记录'))
    elif res['status'] == 'ok' and res['message'] == 'ID not found':
        await wwsmerecent.finish(Message('ID not found'))
    elif res['status'] == 'ok' and res['message'] == 'Data is none':
        await wwsmerecent.finish(Message('该账号无战斗数据'))
    elif res['status'] == 'ok' and res['message'] == 'Date too long':
        if datetime.datetime.now().hour >= 0 and datetime.datetime.now().hour <= 4:
            date_num = 2
        else:
            date_num = 1
        await wwsmerecent.finish(Message('无当前天数数据，最多可查询 {} 天\n'.format(res['bind_num']-date_num)))
    elif res['status'] == 'ok' and res['message'] == 'SUCCESS':

        try:
            await wwsmerecent.send(MessageSegment.image("file:///"+res['img']))
        except:
            if DEBUG:
                await bot.send_private_msg(user_id=SUPERUSER, message='pvp recent发生错误，消息发送失败')
            else:
                await wwsmerecent.finish()
        os.remove(res['img'])
    elif res['status'] == 'error' and res['message'] == 'NETWORK ERROR':
        await wwsmerecent.finish(Message('网络错误，请稍后重试'))
    else:
        canshu = {
            'accid': account_id,
            'server': server,
            'date': date,
            'res': res
        }
        if DEBUG:
            await bot.send_private_msg(user_id=SUPERUSER, message='recent发生错误，参数：'+str(canshu))
        else:
            await wwsmerecent.finish()
        await wwsmerecent.finish(Message('呜呜呜，好像哪里坏掉了(该bug已上报,将会及时处理)'))
    # except:
    #     await bot.send_private_msg(user_id=SUPERUSER, message='recent发生错误，消息发送失败')

wwsmerankrecent = on_startswith({'wws me rank recent'})


@wwsmerankrecent.handle()
async def me_recent(bot: Bot, event: Event, state: T_State):
    user_qqid = event.get_user_id()
    info_message = str(event.get_message())
    server_log().add_data()
    date = ''.join(info_message.replace('wws me rank recent', '').split())
    if info_message in ['wws me rank recent ', 'wws me rank recent']:
        date = 1
    account_id, server, pic_type = tool.get_account_id(user_qqid)
    if account_id == 0:
        await wwsmerankrecent.finish(Message('未绑定账号，请先绑定，示例wws asia set your_id'))
    try:
        date = int(date)
    except:
        await wwsmerankrecent.finish(Message('命令格式错误'))
    if date >= 120:
        await wwsmerankrecent.finish(Message('由于服务器云硬盘大小限制，最多只能储存120天的数据'))
    try:
        res = recent.pic().main('rank', await recent.recent((account_id, server, date)).recent_data())
    except Exception as e:
        res = {'status': 'error', 'hidden': False,
               'message': 'UNKNOW ERROR', 'error': str(e)}
    gc.collect()
    # try:
    if res['status'] == 'ok' and res['message'] == 'Hidden profile':
        await wwsmerankrecent.finish(Message('无有效数据或隐藏了战绩'))
    elif res['status'] == 'error' and res['message'] == 'Network Error':
        await wwsmerankrecent.finish(Message('数据更新失败，请稍后尝试'))
    elif res['status'] == 'error' and res['message'] == 'New User':
        await wwsmerankrecent.finish(Message('由于后台数据更新需要一段时间，新绑定的账号无法立即查询recent'))
    elif res['status'] == 'ok' and res['message'] == 'Recent data is None':
        await wwsmerankrecent.finish(Message('该日期范围内没有战斗记录'))
    elif res['status'] == 'ok' and res['message'] == 'ID not found':
        await wwsmerankrecent.finish(Message('ID not found'))
    elif res['status'] == 'ok' and res['message'] == 'Data is none':
        await wwsmerankrecent.finish(Message('该账号无战斗数据'))
    elif res['status'] == 'ok' and res['message'] == 'Date too long':
        if datetime.datetime.now().hour >= 0 and datetime.datetime.now().hour <= 4:
            date_num = 2
        else:
            date_num = 1
        await wwsmerankrecent.finish(Message('无当前天数数据，最多可查询 {} 天\n'.format(res['bind_num']-date_num)))
    elif res['status'] == 'ok' and res['message'] == 'SUCCESS':
        try:
            await wwsmerankrecent.send(MessageSegment.image("file:///"+res['img']))
        except:
            if DEBUG:
                await bot.send_private_msg(user_id=SUPERUSER, message='rank recent发生错误，消息发送失败')
            else:
                await wwsmerankrecent.finish()
        os.remove(res['img'])
    elif res['status'] == 'error' and res['message'] == 'NETWORK ERROR':
        await wwsmerankrecent.finish(Message('网络错误，请稍后重试'))
    else:
        canshu = {
            'accid': account_id,
            'server': server,
            'date': date,
            'res': res
        }
        if DEBUG:
            await bot.send_private_msg(user_id=SUPERUSER, message='recent发生错误，参数：'+str(canshu))
        else:
            await wwsmerankrecent.finish()
        await wwsmerankrecent.finish(Message('呜呜呜，好像哪里坏掉了(该bug已上报,将会及时处理)'))
    # except:
    #     await bot.send_private_msg(user_id=SUPERUSER, message='recent发生错误，消息发送失败')

wws_rl = on_startswith({'wows日历', 'wws日历', 'wows 日历', 'wws 日历'})


@wws_rl.handle()
async def rl(bot: Bot, event: Event, state: T_State):
    user_qqid = event.get_user_id()
    server_log().add_data()
    account_id, server, pic_type = tool.get_account_id(user_qqid)
    if account_id == 0:
        await wws_rl.finish(Message('未绑定账号，请先绑定，示例wws asia set your_id'))
    try:
        res = await contribution.pic((account_id, server)).main()
    except Exception as e:
        res = {'status': 'error', 'hidden': False,
               'message': 'UNKNOW ERROR', 'error': str(e)}
    gc.collect()
    # try:
    if res['status'] == 'error' and res['message'] == 'Network Error':
        await wws_rl.finish(Message('数据更新失败，请稍后尝试'))
    elif res['status'] == 'error' and res['message'] == 'New User':
        await wws_rl.finish(Message('本功能需先绑定7天后才可查询'))
    elif res['status'] == 'ok' and res['message'] == 'SUCCESS':
        await wws_rl.send(MessageSegment.image("file:///"+res['img']))
        os.remove(res['img'])
    elif res['status'] == 'error' and res['message'] == 'NETWORK ERROR':
        await wws_rl.finish(Message('网络错误，请稍后重试'))
    else:
        canshu = {
            'accid': account_id,
            'server': server,
            'res': res
        }
        if DEBUG:
            await bot.send_private_msg(user_id=SUPERUSER, message='calendar发生错误，参数：'+str(canshu))
        else:
            await wws_rl.finish()
        await wws_rl.finish(Message('呜呜呜，好像哪里坏掉了(该bug已上报,将会及时处理)'))

wws_seach = on_startswith({'wws seach'})


@wws_seach.handle()
async def name_seach(bot: Bot, event: Event, state: T_State):
    info_message = str(event.get_message()).replace('wws seach', '')
    server_log().add_data()
    try:
        res = name.seach_name().main(info_message)
    except Exception as e:
        res = {'status': 'error', 'hidden': False,
               'message': 'UNKNOW ERROR', 'error': str(e)}
    gc.collect()
    if res['status'] == 'error' and res['message'] == 'Too Much Ship':
        await wws_seach.finish(Message('当前筛选条件下的船只过多，请缩小范围'))
    elif res['status'] == 'error' and res['message'] == 'No Data':
        await wws_seach.finish(Message('未筛选到数据'))
    elif res['status'] == 'error' and res['message'] == 'Invalid Parameter':
        await wws_seach.finish(Message('不合法的参数:[{}]'.format(res['data'])))
    elif res['status'] == 'ok' and res['message'] == 'SUCCESS':
        await wws_seach.send(MessageSegment.image("file:///"+res['img']))
        os.remove(res['img'])
    else:
        if DEBUG:
            await bot.send_private_msg(user_id=SUPERUSER, message='seach发生错误'+str(res))
        else:
            await wws_seach.finish()
        await wws_seach.finish(Message('呜呜呜，好像哪里坏掉了(该bug已上报,将会及时处理)'))


wws_add = on_startswith({'wws add'})


@wws_add.handle()
async def name_add(bot: Bot, event: Event, state: T_State):
    info_message = (str(event.get_message()).replace('wws add', '')).split()
    if len(info_message) != 2:
        await wws_add.finish(Message('格式错误，wws add [标准名称] [别称]'))
    try:
        res = name.add_name().main(info_message[0], info_message[1])
    except Exception as e:
        res = {'status': 'error', 'hidden': False,
               'message': 'UNKNOW ERROR', 'error': str(e)}
    gc.collect()
    if res['status'] == 'error' and res['message'] == 'Invalid Standardname':
        await wws_add.finish(Message('未查询到船只[{}]'.format(info_message[0])))
    elif res['status'] == 'ok' and res['message'] == 'SUCCESS':
        await bot.send_private_msg(user_id=SUPERUSER, message='为[{}]添加别名[{}]'.format(info_message[0], info_message[1]))
        await wws_add.finish(Message('添加成功'))
    else:
        if DEBUG:
            await bot.send_private_msg(user_id=SUPERUSER, message='add发生错误'+str(res))
        else:
            await wws_add.finish()
        await wws_add.finish(Message('呜呜呜，好像哪里坏掉了(该bug已上报,将会及时处理)'))

wws_monitor = on_startswith({'wws monitor'})


@wws_monitor.handle()
async def kokomi_monitor(bot: Bot, event: Event, state: T_State):
    try:
        res = monitor.pic().kokomi()
    except Exception as e:
        res = {'status': 'error', 'hidden': False,
               'message': 'UNKNOW ERROR', 'error': str(e)}
    gc.collect()
    if res['status'] == 'ok' and res['message'] == 'SUCCESS':
        await wws_monitor.send(MessageSegment.image("file:///"+res['img']))
        os.remove(res['img'])
    else:
        if DEBUG:
            await bot.send_private_msg(user_id=SUPERUSER, message='monitor发生错误'+str(res))
        else:
            await wws_monitor.finish()
        await wws_monitor.finish(Message('呜呜呜，好像哪里坏掉了(该bug已上报,将会及时处理)'))

wws_set = on_startswith({'wws asia set', 'wws eu set', 'wws na set', 'wws ru set', 'wws cn set',
                        'wws 亚服 set', 'wws 欧服 set', 'wws 美服 set', 'wws 俄服 set', 'wws 国服 set', 'wws Asia set', 'wws aisa set'})


@wws_set.handle()
async def rl(bot: Bot, event: Event, state: T_State):
    user_qqid = event.get_user_id()
    info_message = str(event.get_message()).split()
    server_log().add_data()
    server_dict = {
        'asia': 'asia',
        '亚服': 'asia',
        'Asia': 'asia',
        'aisa': 'asia',
        'eu': 'eu',
        '欧服': 'eu',
        'na': 'na',
        '美服': 'na',
        'ru': 'ru',
        '欧服': 'ru',
        'cn': 'cn',
        '国服': 'cn',
    }
    server = server_dict[info_message[1]]
    if server == 'cn':
        await wws_set.finish(Message('kokomi暂时不支持国服数据的查询'))
    nickname = info_message[3]
    try:
        res = await set.bind().set_id(user_qqid, nickname, server)
    except Exception as e:
        res = {'status': 'ok', 'hidden': False,
               'message': 'UNKNOW ERROR', 'error': str(e)}
    gc.collect()
    if res['status'] == 'error' and res['message'] == 'NETWORK ERROR':
        await wws_set.finish(Message('网络错误，请稍后重试'))
    elif res['status'] == 'error' and res['message'] == 'No Result':
        await wws_set.finish(Message('无查询结果，请检查id拼写'))
    elif res['status'] == 'ok' and res['message'] == 'Bind Id':
        await wws_set.finish(Message('绑定成功'))
    elif res['status'] == 'ok' and res['message'] == 'Change Id':
        await wws_set.finish(Message('改绑成功'))
    else:
        if DEBUG:
            await bot.send_private_msg(user_id=SUPERUSER, message='set发生错误'+str(res))
        else:
            await wws_set.finish()
        await wws_set.finish(Message('呜呜呜，好像哪里坏掉了(该bug已上报,将会及时处理)'))


class tool:
    def get_account_id(user_qqid: str):
        conn = sqlite3.connect(user_id_path)
        c = conn.cursor()
        cursor = c.execute(
            "SELECT QQID,ACCID,TYPE,LANGUAGE,TIME,SERVER,EXTER1,EXTER2  from userid")
        account_id = 0
        row_list = list(cursor)
        conn.close()
        for row in row_list:
            userqqid = row[0]
            accountid = row[1]
            if userqqid == int(user_qqid):
                pic_type = row[2]
                server = row[5]
                return (accountid, server, pic_type)
        if account_id == 0:
            return (0, '0', '0')


class seach:
    def __init__(self) -> None:
        self.ship_info_data = json.load(
            open(os.path.join(file_path, 'ship_name.json'), "r", encoding="utf-8"))

    def seach_name(self, info):
        info = self.name_format(info)
        return_dict = {
            'status': 'ok',
            'ship_id': None
        }
        for ship_id, ship_data in self.ship_info_data.items():
            if info in ship_data['ship_name']['other']:
                return_dict['ship_id'] = ship_id
        return return_dict

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


class update:
    def __init__(self) -> None:
        self.ship_info_data = json.load(
            open(os.path.join(file_path, 'ship_name.json'), "r", encoding="utf-8"))

    async def update_name(self):
        async with httpx.AsyncClient() as client:
            try:
                url1 = 'https://api.wows-numbers.com/personal/rating/expected/json/'
                res1 = await client.get(url1, timeout=3)
                if res1.status_code != 200:
                    return {'status': 'error', 'data': 'Network Error'}
                result1 = res1.json()
                with open(server_data_path, 'w', encoding='utf-8') as f:
                    f.write(json.dumps(result1, ensure_ascii=False))
                f.close()
                return {'status': 'ok'}
            except Exception as e:
                return {'status': 'error', 'data': str(e)}

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


class server_log():
    def __init__(self) -> None:
        self.serverlog = json.load(open(os.path.join(
            file_path, 'server_log.json'), "r", encoding="utf-8"))

    def add_data(self):
        hour = datetime.datetime.now().hour
        day = date.today().strftime("%Y-%m-%d")
        if day not in self.serverlog['day']:
            self.serverlog['day'][day] = 0
        add_hour = hour + 1
        if add_hour == 24:
            add_hour = 0
        if self.serverlog['hour'][str(add_hour)] != 0:
            self.serverlog['hour'][str(add_hour)] = 0
        self.serverlog['day'][day] += 1
        self.serverlog['hour'][str(hour)] += 1
        self.serverlog['all']['times'] += 1
        with open(os.path.join(file_path, 'server_log.json'), 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.serverlog, ensure_ascii=False))
        f.close()
        gc.collect()
