import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.monitor.v20180724 import monitor_client, models
import os
import sys
import time
import matplotlib.pyplot as plt
'''
CpuUsage        CPU 利用率
MemUsed         使用的内存量，不包括系统缓存和缓存区占用内存，依赖监控组件安装采集
TcpCurrEstab    处于 ESTABLISHED 状态的 TCP 连接数量，依赖监控组件安装采集
'''
if True:
    config_path = os.path.join(os.path.dirname(
        __file__).replace('4-monitor', ''), 'config')
    sys.path.append(config_path)
    import config


def request_data(MetricName: str):
    try:
        cred = credential.Credential(
            config.MonitorConfig.SecretId, config.MonitorConfig.SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "monitor.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = monitor_client.MonitorClient(
            cred, config.MonitorConfig.Region, clientProfile)
        req = models.GetMonitorDataRequest()
        params = {
            "Namespace": config.MonitorConfig.Namespace,
            "MetricName": MetricName,
            "Period": 3600,
            "StartTime": time.strftime("%Y-%m-%dT%H:%M:%S+08:00", time.localtime(time.time()-5*24*60*60)),
            "EndTime": time.strftime("%Y-%m-%dT%H:%M:%S+08:00", time.localtime(time.time())),
            "Instances": [
                {
                    "Dimensions": [
                        {
                            "Name": config.MonitorConfig.Dimensions_Name,
                            "Value": config.MonitorConfig.Dimensions_Value
                        }
                    ]
                }
            ]
        }
        req.from_json_string(json.dumps(params))
        resp = client.GetMonitorData(req)
        return resp.to_json_string()
    except TencentCloudSDKException as err:
        print(err)


res = eval(request_data('MemUsed'))
plt.style.use('seaborn-whitegrid')
plt.figure(figsize=(90, 10))
x_ticks = []
for index in res['DataPoints'][0]['Timestamps']:
    x_ticks.append(time.strftime("%m-%d %H:00", time.localtime(index)))
num = res['DataPoints'][0]['Values']
x = x_ticks
y1 = num
x_ = range(len(x))
y_ = range(len(y1))
plt.xticks(list(x_)[::10], x[::10], rotation=25)
plt.plot(x, y1, color='#CB4B4B', label='label1', linewidth=4.0)
plt.tick_params(labelsize=50)
plt.tight_layout(pad=1.0)
pic_name = str(time.time())
pic_path = os.path.join(os.path.dirname(__file__), 'temp', f'{pic_name}.jpg')
plt.savefig(pic_path, format='jpg')
