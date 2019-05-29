import pymysql
import matplotlib.pyplot as plt
import time,datetime
import json,urllib.request

#从数据库读取数据并显示在饼装图里，然后把饼状图通过钉钉机器人发送到钉钉群
class dbConnect(object):

    def __init__(self,dbconfig):
        self.user = dbconfig['username']
        self.password = dbconfig['password']
        self.url = dbconfig['host']
        self.port = dbconfig['port']
        self.dbname = dbconfig['db']

        self.db = pymysql.connect(host=self.url,user=self.user,password=self.password,db=self.dbname,port=self.port,charset='utf8')
        self.cursor = self.db.cursor()

    def query(self,sql):
        result = self.cursor.execute(sql)
        return result

    def close(self):
        self.cursor.close()
        self.db.close()




def send_to_ding():
    access_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX'
    header = {
        "Content-Type": "application/json",
        "charset": "utf-8"
        }
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "测试",
            "text": "![avatar](https://XXXXXXX/dingimage/1.jpg)"
        },
    }

    sendData = json.dumps(data)
    request = urllib.request.Request(access_token,data = sendData.encode(encoding='UTF8'),headers = header)
    urlopen = urllib.request.urlopen(request)
    print(urlopen.read())

if __name__ == "__main__":
    dbconfig = {
        'host': 'xxxxxxxxx',
        'port': 3306,
        'username': 'xxxxxxxxxx',
        'password': 'xxxxxxxxxx',
        'db': 'xxxxx',
        'charset': 'utf8'
    }

    dbconn = dbConnect(dbconfig)
    sql = "select * from alert_count where date=date_sub(date_format(now(),'%Y-%m-%d'),interval 1 day)"
    dbconn.query(sql)
    result = dbconn.cursor.fetchall()

    value_list = {
        "unreachable": result[0][3],
        "disk": result[0][4],
        "IO": result[0][5],
        "memory": result[0][6],
        "processor": result[0][7],
        "system": result[0][8],
        "custom": result[0][9]
    }

    file_date = datetime.date.today() - datetime.timedelta(days=1)
    file_date=str(file_date)
    labels=[]
    values=[]
    for key,value in value_list.items():
        if value != 0:
            labels.append(key)
            values.append(value)

    colors = ["pink", "coral", "yellow", "orange"]
    plt.pie(values, explode=None,colors=None,autopct='%1.2f%%',labels=labels)
    plt.title(file_date+'Daily Alert Type Analyze')
    plt.savefig('1.png')
    send_to_ding()
    dbconn.close()






