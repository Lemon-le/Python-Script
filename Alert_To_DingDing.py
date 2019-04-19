import json,urllib.request

#Function：将一个目录下的所有文件内容汇总到一个文件
#Author  ：李先生
#Date    ：20190419
#Version ：V1.0

#DingDing的access_token
access_token = 'xxxxx'
#发送的内容
content='xxx'
#电话
tel='xxx'

def send_to_ding(content,tel):
    header = {
        "Content-Type": "application/json",
        "charset": "utf-8"
        }
    data = {
         "msgtype": "text",
            "text": {
                "content": content
            },
         "at": {
            "atMobiles": [
                 tel
             ],
                "isAtAll":False   # at为非必须
             }
        }
    sendData = json.dumps(data)
    request = urllib.request.Request(access_token,data = sendData.encode(encoding='UTF8'),headers = header)
    urlopen = urllib.request.urlopen(request)
    print(urlopen.read())

def main():
    send_to_ding(content, tel)

if __name__ == '__main__':
    main()