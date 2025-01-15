import requests
import uuid

'''
curl 'https://ulink.game.qq.com/app/8328/18139773431f8885/index.php?route=Information/getUserData&iActId=10332&game=kq' \
  -H 'accept: */*' \
  -H 'accept-language: en,zh-CN;q=0.9,zh;q=0.8' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundaryOemQbrx2n6UJEvPh' \
  -H 'cookie: eas_sid=d1m763t6m8R3A3t9P8T1f6d2K0; _qpsvr_localtk=0.6874483518290031; RK=bbnxO9x++Q; ptcz=e6c2e26cb122bd574bb17ac2f2c57bff856ec2b7768d4a257594fb349e681ac0; acctype=qc; openid=5934DF1F6BD774DD014CF341AAD59F87; access_token=41E1EA262936C669CB4A81EFF9C275FE; appid=101511284' \
  -H 'origin: https://klbq.qq.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://klbq.qq.com/' \
  -H 'sec-ch-ua: "Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' \
  --data-raw $'------WebKitFormBoundaryOemQbrx2n6UJEvPh\r\nContent-Disposition: form-data; name="gameMode"\r\n\r\n0\r\n------WebKitFormBoundaryOemQbrx2n6UJEvPh\r\nContent-Disposition: form-data; name="seasonId"\r\n\r\n0\r\n------WebKitFormBoundaryOemQbrx2n6UJEvPh\r\nContent-Disposition: form-data; name="e_code"\r\n\r\n0\r\n------WebKitFormBoundaryOemQbrx2n6UJEvPh\r\nContent-Disposition: form-data; name="eas_url"\r\n\r\nhttp://klbq.qq.com/cp/oceanus202312launcher/military.html\r\n------WebKitFormBoundaryOemQbrx2n6UJEvPh\r\nContent-Disposition: form-data; name="eas_refer"\r\n\r\nhttp://klbq.qq.com/cp/oceanus202312launcher/military.html?reqid=acc86dcb-df50-4200-84e3-38bff26d25a0&version=27\r\n------WebKitFormBoundaryOemQbrx2n6UJEvPh--\r\n'
'''
# 请求的 URL 和查询参数
url = "https://ulink.game.qq.com/app/8328/18139773431f8885/index.php"
params = {
    "route": "Information/getMapListInfo",
    "iActId": "10332",
    "game": "kq",
}

# 表单数据
data = {
    "gameMode": 5,
    "seasonId": 0,
    "e_code": 0,
    "eas_url": "http://klbq.qq.com/cp/oceanus202312launcher/military.html",
    "eas_refer": f"http://noreferrer/?reqid={uuid.uuid4()}&version=27",
}

# 请求头
headers = {
    "accept": "*/*",
    "accept-language": "en,zh-CN;q=0.9,zh;q=0.8",
    "origin": "https://klbq.qq.com",
    "referer": "https://klbq.qq.com/",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
}

cooikes = {
    "acctype": "qc",
    "openid": "5934DF1F6BD774DD014CF341AAD59F87",
    "access_token": "41E1EA262936C669CB4A81EFF9C275FE",
    "appid": "101511284"
}

# 发送 POST 请求
response = requests.post(url, params=params, headers=headers, cookies=cooikes, data=data)
# 输出响应
print(response.status_code)
print(response.json())

print(response.request.headers)
