import boto3,requests,json,urllib.request
from botocore.config import Config

#获取AWS上处于Running状态的机器，全部添加到zabbix

#指定区域
region=['eu-west-1','us-west-2','ap-southeast-1']

#client连接信息设置
config = Config(
        retries=dict(
            max_attempts=20
        )
    )


#zabbix的URL、账号、密码
zabbix_root = 'https://XXXX/zabbix'
url = zabbix_root + '/api_jsonrpc.php'
user = "xxx"
password = "xxxx"
#trigger的name描述信息
post_header = {
        "Content-Type": "application/json"
    }

#登录获取Session
def get_session():
    post_login = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": user,
            "password": password
        },
        "id": 1
    }

    req = requests.post(url, data=json.dumps(post_login), headers=post_header)
    zabbix_req = json.loads(req.text)

   # print("Session为：" + zabbix_req.get('result'))
    return zabbix_req.get('result')

#创建主机
def create_host(ip,name):
    host = {
    "jsonrpc": "2.0",
    "method": "host.create",
    "params": {
        "host": name,
        "interfaces": [
            {
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": ip,
                "dns": "",
                "port": "10050"
            }
        ],
        "groups": [
            {
                "groupid": "2"
            }
        ],

        "templates": [
            {
                "templateid": "10001"
            }
        ],

    },
    "auth": get_session(),
    "id": 1
}

    req = requests.post(url, data=json.dumps(host), headers=post_header)
    zabbix_req = json.loads(req.text)

    print(zabbix_req)

#获取AWS上正在Running状态的机器
def _get_aws_running_instance():
    for each_region in region:

        client = boto3.client('ec2',region_name=each_region,config=config)

        response = client.describe_instances(
            Filters=[
                {
                    'Name': 'instance-state-code',
                    'Values': [
                        '16',
                    ]
                },
            ]
        )

        for each_instance in response['Reservations']:
            for each in each_instance['Instances']:
                ip=each['PrivateIpAddress']
                for each_name in each['Tags']:
                    if each_name['Key']=='Name':
                        name=each_name['Value']
                        create_host(ip, name)



_get_aws_running_instance()