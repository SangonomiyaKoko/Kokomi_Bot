import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.monitor.v20180724 import monitor_client, models
import os
import yaml
import time
import base64
import matplotlib.pyplot as plt
from PIL import ImageFont, Image, ImageDraw
import platform
import datetime
from datetime import date, timedelta
import sqlite3
import threading
import gc
'''
CpuUsage        CPU 利用率
MemUsed         使用的内存量，不包括系统缓存和缓存区占用内存，依赖监控组件安装采集
TcpCurrEstab    处于 ESTABLISHED 状态的 TCP 连接数量，依赖监控组件安装采集
'''
isWin = True if platform.system().lower() == 'windows' else False
file_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
png_path = os.path.dirname(__file__)

f = open(os.path.join(file_path, 'config.yaml'))
config_data = yaml.load(f.read(), Loader=yaml.FullLoader)
DATABASE_PATH = config_data['DatabaseConfig']['Database_path']
f.close()


def decode_key(token: str) -> str:
    decode = base64.b64decode(token)
    return decode.decode("utf-8")


def request_data(MetricName: str):
    try:
        cred = credential.Credential(decode_key(config_data['MonitorConfig']['SecretId']), decode_key(
            config_data['MonitorConfig']['SecretKey']))
        httpProfile = HttpProfile()
        httpProfile.endpoint = "monitor.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = monitor_client.MonitorClient(
            cred, config_data['MonitorConfig']['Region'], clientProfile)
        req = models.GetMonitorDataRequest()
        params = {
            "Namespace": config_data['MonitorConfig']['Namespace'],
            "MetricName": MetricName,
            "Period": 3600,
            "StartTime": time.strftime("%Y-%m-%dT%H:%M:%S+08:00", time.localtime(time.time()-5*24*60*60)),
            "EndTime": time.strftime("%Y-%m-%dT%H:%M:%S+08:00", time.localtime(time.time())),
            "Instances": [
                {
                    "Dimensions": [
                        {
                            "Name": config_data['MonitorConfig']['Dimensions_Name'],
                            "Value": config_data['MonitorConfig']['Dimensions_Value']
                        }
                    ]
                }
            ]
        }
        req.from_json_string(json.dumps(params))
        resp = client.GetMonitorData(req)
        return eval(resp.to_json_string())
    except TencentCloudSDKException as err:
        return str(err)


class pic():
    def __init__(self) -> None:
        self.server_log_data = json.load(
            open(os.path.join(file_path, 'data', 'server_log.json'), "r", encoding="utf-8"))

    def x_coord(self, in_str: str, font: ImageFont.FreeTypeFont):
        x, y = font.getsize(in_str)
        out_coord = x/2
        return out_coord

    def getFileSize(self, filePath, size=0):
        f_num = 0
        for root, dirs, files in os.walk(filePath):
            for f in files:
                f_num += 1
                size += os.path.getsize(os.path.join(root, f))
        return (round(size/1024/1024/1024, 2), f_num)

    def kokomi(self):
        img = Image.open(os.path.join(png_path, 'background.jpg'))
        draw = ImageDraw.Draw(img)
        font_path = os.path.join(file_path, 'data', 'SourceHanSansCN-Bold.ttf') if isWin else os.path.join(
            '/usr/share/fonts', 'SourceHanSansCN-Bold.ttf')
        font2_path = os.path.join(file_path, 'data', 'NZBZ.ttf') if isWin else os.path.join(
            '/usr/share/fonts', 'NZBZ.ttf')
        font = ImageFont.truetype(font_path, 38)
        font2 = ImageFont.truetype(font2_path, 120)
        font3 = ImageFont.truetype(font2_path, 80)
        now_hour = datetime.datetime.now().hour
        hour_list = []
        i = 1
        while i <= 24:
            add_hour = now_hour+i
            if add_hour >= 24:
                add_hour -= 24
            hour_list.append(add_hour)
            i += 1
        max_times = 0
        for index in hour_list:
            if self.server_log_data['hour'][str(index)] > max_times:
                max_times = self.server_log_data['hour'][str(index)]
        max_list = [
            [200, 150, 100, 50, 0],
            [400, 300, 200, 100, 0],
            [600, 450, 300, 150, 0],
            [800, 600, 400, 200, 0],
            [1000, 750, 500, 250, 0]
        ]
        i = 0
        plt_y_list = [1000, 750, 500, 250, 0]
        while i < len(max_list):
            if max_list[i][0] >= max_times:
                plt_y_list = max_list[i]
                break
            i += 1
        i = 0
        for index in plt_y_list:
            x_coord = self.x_coord(str(index), font)
            draw.text((790-x_coord*2, 310+102*i),
                      str(index), (100, 100, 100), font=font)
            i += 1
        i = 0
        a = ImageDraw.ImageDraw(img)
        for index in hour_list:
            y1 = 738 - \
                self.server_log_data['hour'][str(index)]/plt_y_list[0]*400
            a.rectangle(((835+72*i, y1), (835+38+72*i, 738)),
                        fill=(167, 196, 252), outline=None)
            x_coord = self.x_coord(str(index), font)
            draw.text((835+19+72*i-x_coord, 745),
                      str(index), (100, 100, 100), font=font)

            i += 1
        draw.text((112, 352), str(
            self.server_log_data['all']['times']), (0, 0, 0), font=font2)
        yestoday = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
        draw.text(
            (122, 494), '+'+str(self.server_log_data['day'][yestoday]), (17, 170, 20), font=font3)
        conn = sqlite3.connect(os.path.join(file_path, 'data', 'accountid.db'))
        c = conn.cursor()
        cursor = c.execute("SELECT ACCID,TIME,SERVER  from accid")
        user_list = list(cursor)
        all_user = len(user_list)
        conn.close()
        db_dict = {
            'asia': 0,
            'na': 0,
            'eu': 0,
            'ru': 0
        }
        for user in user_list:
            db_dict[user[2]] += 1
        draw.text((2739, 352), str(all_user), (0, 0, 0), font=font2)
        i = 0
        for server, num in db_dict.items():
            draw.text((2933, 509+55*i), str(num), (0, 0, 0), font=font)
            i += 1

        plt_data = []
        for server, num in db_dict.items():
            plt_data.append(num)
        pic_path = self.user_plt(plt_data)
        achieve_img = Image.open(pic_path)
        img.paste(achieve_img, (3200, 280))
        os.remove(pic_path)
        achieve_img.close()
        global server_result
        server_result = {
            'CpuUsage': {},
            'MemUsed': {},
            'TcpCurrEstab': {},
            'Database': None
        }
        thread = []
        for index in ['CpuUsage', 'MemUsed', 'TcpCurrEstab', 'Database']:
            thread.append(threading.Thread(
                target=self.server_data, args=(index,)))
        for t in thread:
            t.start()
        for t in thread:
            t.join()
        draw.text((4085, 422), str(
            server_result['Database'][1]), (0, 0, 0), font=font3)
        draw.text((4085, 650), str(
            server_result['Database'][0])+' GB', (0, 0, 0), font=font3)
        if server_result['CpuUsage']['status'] == 'ok':
            png_data = self.plt_png(
                'CpuUsage', server_result['CpuUsage']['data'])
            achieve_img = Image.open(png_data['img'])
            achieve_img = achieve_img.resize((3200, 300))
            img.paste(achieve_img, (742, 934))
            os.remove(png_data['img'])
            achieve_img.close()
            draw.text((136, 1032), str(
                round(png_data['data'], 2))+'%', (0, 0, 0), font=font2)
        else:
            return {'status': 'error', 'message': 'Plt Error'}
        if server_result['MemUsed']['status'] == 'ok':
            png_data = self.plt_png(
                'MemUsed', server_result['MemUsed']['data'])
            achieve_img = Image.open(png_data['img'])
            achieve_img = achieve_img.resize((3200, 300))
            img.paste(achieve_img, (742, 1410))
            os.remove(png_data['img'])
            achieve_img.close()
            draw.text((136, 1508), str(
                round(png_data['data']/2048*100, 2))+'%', (0, 0, 0), font=font2)
        else:
            return {'status': 'error', 'message': 'Plt Error'}
        if server_result['TcpCurrEstab']['status'] == 'ok':
            png_data = self.plt_png(
                'TcpCurrEstab', server_result['TcpCurrEstab']['data'])
            achieve_img = Image.open(png_data['img'])
            achieve_img = achieve_img.resize((3200, 300))
            img.paste(achieve_img, (742, 1886))
            os.remove(png_data['img'])
            achieve_img.close()
            draw.text((136, 1984), str(
                png_data['data']), (0, 0, 0), font=font2)
        else:
            return {'status': 'error', 'message': 'Plt Error'}
        pic_path = os.path.join(file_path, 'temp', '4-{}.png'.format(
            png_name().generate_name(str(int(time.time()*100000)))))
        img.resize((1600, 800))
        img.save(pic_path)
        img.close()
        del server_result
        del draw
        gc.collect()
        return {'status': 'ok', 'message': 'SUCCESS', 'img': pic_path}

    def user_plt(self, user_data):
        labels = ['AS', 'NA', 'EU', 'RU']
        colors = ['#60acfc', '#32d3eb', '#5bc49f', '#feb64d']
        plt.pie(x=user_data, labels=labels, colors=colors, autopct='%.2f%%', pctdistance=0.7, labeldistance=1.1,
                startangle=0, radius=1.6, counterclock=False, textprops={'fontsize': 20, 'color': 'black'},)
        pic_name = str(time.time())
        pic_path = os.path.join(file_path, 'temp', f'bind-{pic_name}.jpg')
        plt.savefig(pic_path, format='jpg')
        plt.close()
        return pic_path

    def plt_png(self, data_type, res):
        plt.style.use('seaborn-whitegrid')
        plt.figure(figsize=(106, 10))
        x_ticks = []
        for index in res['DataPoints'][0]['Timestamps']:
            x_ticks.append(time.strftime(
                "%m-%d %H:00", time.localtime(index)))
        num = res['DataPoints'][0]['Values']
        now_data = res['DataPoints'][0]['Values'][len(num)-1]
        x = x_ticks
        y1 = num
        x_ = range(len(x))
        y_ = range(len(y1))
        plt.xticks(list(x_)[::10], x[::10], rotation=25)
        plt.plot(x, y1, color='#CB4B4B', label='label1', linewidth=4.0)
        plt.tick_params(labelsize=50)
        plt.tight_layout(pad=1.0)
        pic_name = str(time.time())
        pic_path = os.path.join(
            file_path, 'temp', f'{data_type}-{pic_name}.jpg')
        plt.savefig(pic_path, format='jpg')
        plt.close()
        return {'status': 'ok', 'message': 'SUCCESS', 'img': pic_path, 'data': now_data}

    def server_data(self, data_type):
        if data_type == 'Database':
            server_result[data_type] = self.getFileSize(DATABASE_PATH)
            return None
        res = request_data(data_type)
        if type(res) != dict:
            server_result[data_type] = {
                'status': 'error', 'message': 'NETWORK ERROR', 'error': res}
            return None
        else:
            server_result[data_type] = {
                'status': 'ok', 'message': 'SUCCESS', 'data': res}
            return None


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


'''
CpuUsage        CPU 利用率
MemUsed         使用的内存量，不包括系统缓存和缓存区占用内存，依赖监控组件安装采集
TcpCurrEstab    处于 ESTABLISHED 状态的 TCP 连接数量，依赖监控组件安装采集
'''
