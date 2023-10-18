from werobot import WeRoBot
import config as cfg
import requests
import datetime

myrobot = WeRoBot(token=cfg.token)
myrobot.config["APP_ID"] = cfg.appid
myrobot.config['ENCODING_AES_KEY'] = cfg.aeskey
urlmd = "http://127.0.0.1:6806/api/filetree/createDocWithMd"
openid = "你的微信openid"
notebook = "你的笔记本ID"
apitoken = "你的思源笔记apitoken"

weekday_dict = {
    '0': '日',
    '1': '一',
    '2': '二',
    '3': '三',
    '4': '四',
    '5': '五',
    '6': '六'
}
now = datetime.datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")
weekday = weekday_dict[now.strftime("%w")]
hour = now.strftime("%H")
minute = now.strftime("%M")
second = now.strftime("%S")
path = f"{year}年{month}月{day}日星期{weekday}-{hour}:{minute}:{second}"

headers = {
    'Content-Type': 'application/json',
    'Authorization' : f'Token {apitoken}'
}
headers2 = {
    'Authorization' : f'Token {apitoken}'
}

@myrobot.image
def image_note(message, session):
    if message.source == openid:
        name = f"{year}-{month}-{day}--{hour}:{minute}:{second}"
        url = "http://127.0.0.1:6806/api/asset/upload"
        file_url = message.img
        response = requests.get(file_url)
        file_content = response.content
        payload = {
            "assetsDirPath": "/assets/",
            "file[]": (f"{name}.jpg", file_content)
        }
        response = requests.post(url, files=payload, headers=headers2)
        data = response.json()
        pathp = data['data']['succMap'][f"{name}.jpg"]
        data = {
            "notebook": notebook,
            "path": f"【图片】-{path}",
            "markdown": f"![微信图片{name}]({pathp})"
        }
        response = requests.post(urlmd, headers=headers, json=data)
        result = response.json()
        if 'code' in result and result['code'] == 0:
            return f"记录成功:{path}"
        else:
            return "记录失败"
    else:
        return f"此用户无权限:{message.source}"

@myrobot.text
def test_note(message, session):
    if message.source == openid:
        data = {
        "notebook": notebook,
        "path": f"【文字】-{path}",
        "markdown": message.content
        }
        response = requests.post(urlmd, headers=headers, json=data)
        result = response.json()
        if 'code' in result and result['code'] == 0:
            return f"记录成功:{path}"
        else:
            return "记录失败"
    else:
        return f"此用户无权限:{message.source}"

@myrobot.voice
def voice_note(message, session):
    if message.source == openid:
        data = {
        "notebook": notebook,
        "path": f"【语音】-{path}",
        "markdown": message.recognition
        }
        response = requests.post(urlmd, headers=headers, json=data)
        result = response.json()
        if 'code' in result and result['code'] == 0:
            return f"记录成功:{path}"
        else:
            return "记录失败"
    else:
        return f"此用户无权限:{message.source}"

@myrobot.location
def location_note(message, session):
    if message.source == openid:
        location = message.location
        scale = message.location
        latitude = str(location[0])
        longitude = str(location[1])
        scale_str = str(scale)
        data = {
        "notebook": notebook,
        "path": f"【位置】-{path}",
        "markdown": f"经：{longitude}\n纬：{latitude}\n放缩：{scale_str}\n描述：{message.label}"
        }
        response = requests.post(urlmd, headers=headers, json=data)
        result = response.json()
        if 'code' in result and result['code'] == 0:
            return f"记录成功:{path}"
        else:
            return "记录失败"
    else:
        return f"此用户无权限:{message.source}"

@myrobot.link
def link_note(message, session):
    if message.source == openid:
        data = {
        "notebook": notebook,
        "path": f"【链接】-{path}",
        "markdown": f"链接：{message.url}\n标题：{message.title}\n描述：{message.description}"
        }
        response = requests.post(urlmd, headers=headers, json=data)
        result = response.json()
        if 'code' in result and result['code'] == 0:
            return f"记录成功:{path}"
        else:
            return "记录失败"
    else:
        return f"此用户无权限:{message.source}"