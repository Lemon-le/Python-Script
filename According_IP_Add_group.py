import requests
import json

#Function：批量将指定的zabbix agent的IP添加至主机群组
#Author  ：李先生
#Date    ：20191122
#Version ：V1.0

#zabbix地址、用户名、密码
zabbix_root = 'https://xxx/zabbix'
url = zabbix_root + '/api_jsonrpc.php'
user = 'xxx'
password = 'xxx'

#登录
post_login = {
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
        "user": user,
        "password": password
    },
    "id": 1
    }

post_header = {
    "Content-Type": "application/json"
}

#返回的是json对象
req = requests.post(url, data=json.dumps(post_login), headers=post_header)
zabbix_req = json.loads(req.text)

# 获取群组的id
def get_group():
    get_groups = {
        "jsonrpc": "2.0",
        "method": "hostgroup.get",
        "params": {
            "output": "extend",
            "filter": {
                "name": [
                    group_name
                ]
            }
        },
        "auth": zabbix_req.get('result'),
        "id": 1
    }
    get_host_post = requests.post(url, data=json.dumps(get_groups), headers=post_header)
    get_host_res = json.loads(get_host_post.text)


    for i in get_host_res.get('result'):
        groupid=i['groupid']
    return groupid


# 将ip添加至群组
def add_ip_to_group(hostid):
    groupid = get_group()
    add_group = {
    "jsonrpc": "2.0",
    "method": "hostgroup.massadd",
    "params": {
        "groups": [
            {
                "groupid": groupid
            },
        ],
        "hosts": [
            {
                "hostid": hostid
            },
        ]
    },
    "auth": zabbix_req.get('result'),
    "id": 1
}
    get_host_post = requests.post(url, data=json.dumps(add_group), headers=post_header)
    get_host_res = json.loads(get_host_post.text)
    print(get_host_res)


def get_host_id():
    get_hosts_id = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": ["hostid"],
            "selectInterfaces": ["ip"],
        },
        "auth": zabbix_req.get('result'),
        "id": 1
    }
    get_host_post = requests.post(url, data=json.dumps(get_hosts_id), headers=post_header)
    get_host_res = json.loads(get_host_post.text)

    for i in get_host_res.get('result'):
        for ips in i['interfaces']:
            if ips['ip'] in ip_list:
                hostid = i['hostid']
                add_ip_to_group(hostid)
                print(str(hostid)+"已添加")


def main():
    get_host_id()


if __name__ == '__main__':
    ip_list = ['xxx', 'xxx']
    group_name = 'xx'
    main()
