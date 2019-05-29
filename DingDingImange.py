import json,urllib.request

#Function：钉钉机器人发送图片信息；钉钉机器人的发送数据类型里没有图片这个类别
#          只能通过mardown类型，并且图片为URL类型，把自己需要发送的图片放到web里面就可以了
#Author  ：李先生
#Date    ：20190529
#Version ：V1.0

#DingDing的access_token
access_token = 'https://oapi.dingtalk.com/robot/send?access_token=7530e79f6c1cb90582c6ec140df60790a7595e677df7544c0786ae04822a0193'


def send_to_ding():
    header = {
        "Content-Type": "application/json",
        "charset": "utf-8"
        }
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "测试",
            "text": "![avatar](https://XXXXX/dingimage/1.jpg)"
        },
    }

    sendData = json.dumps(data)
    request = urllib.request.Request(access_token,data = sendData.encode(encoding='UTF8'),headers = header)
    urlopen = urllib.request.urlopen(request)
    print(urlopen.read())


def main():
    send_to_ding()

if __name__ == '__main__':
    main()