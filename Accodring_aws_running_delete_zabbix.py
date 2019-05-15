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
zabbix_root = 'https://xxxx/zabbix'
url = zabbix_root + '/api_jsonrpc.php'
user = "xxx"
password = "xxxx"
#trigger的name描述信息
post_header = {
        "Content-Type": "application/json"
    }

aws_list={}
zabbix_list=[]

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

#获取host ID
def get_host_ids(host_ip):
    host_id = {
    "jsonrpc": "2.0",
    "method": "host.get",
    "params": {
        "output": ["name"],
        "selectInterfaces": ["ip"],
    },
    "auth": get_session(),
    "id": 1
}

    host_id_post = requests.post(url, data=json.dumps(host_id), headers=post_header)
    host_id_res = json.loads(host_id_post.text)
    print(host_id_res)
    if host_id_res['result']:
        for a in host_id_res.get('result'):
            for b in a['interfaces']:
                if b['ip'] == host_ip:
                    hostid = a['hostid']
                    hostname = a['name']
        return hostid
    else:
        print("指定的ip" + host_ip + "不存在")
        return -200


# 删除host
def delete_host(hostid):
    host_id = {
       "jsonrpc": "2.0",
        "method": "host.delete",
        "params": [
            hostid,
        ],
        "auth": get_session(),
        "id": 1
    }

    host_id_post = requests.post(url, data=json.dumps(host_id), headers=post_header)
    host_id_res = json.loads(host_id_post.text)
    print(host_id_res)


#获取Zabbix上的所有IP
def get_zabbix_ips():
    get_ip = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": ["hostid"],
            "selectInterfaces": ["ip"],
        },
        "auth": get_session(),
        "id": 1
    }

    get_ip_post = requests.post(url, data=json.dumps(get_ip), headers=post_header)
    get_ip_res = json.loads(get_ip_post.text)

    # 得到一个所有IP的列表
    all = get_ip_res.get('result')
    # 处理格式，打印所有的IP

    for all_ip in all:
        for ip in all_ip['interfaces']:
            zabbix_list.append(ip['ip'])
    return zabbix_list


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
                        aws_list[ip]=name
    return aws_list


def main ():
    zabbix=get_zabbix_ips()
    aws=_get_aws_running_instance()
    #print(zabbix)
    #print(aws)

    #print(len(zabbix))
    #print(len(aws))
    for each_ip in zabbix:
        if each_ip not in aws.keys():
            hostids=get_host_ids(each_ip)
            delete_host(hostids)

main()


