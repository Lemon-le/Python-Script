import boto3
from botocore.config import Config
from exec_command import ParamikoClient 

#Function：遍历AWS所有机器执行命令获得所有机器执行命令的结果，此脚本可以在最下面修改成自己想要的命令
#Author  ：李先生
#Date    ：20190419
#Version ：V1.0

# 指定区域
region = ['eu-west-1']
#region = ['eu-west-1', 'us-west-2', 'ap-southeast-1']

# 设置client的连接信息，不设置，默认值为3，超时的时候会报错，所以设置大一点
config = Config(
    retries=dict(
        max_attempts=20
    )
)

# 遍历指定的几个区域，打印实例的instanceid
for each_region in region:
    # 这里client指定region_name的时候，在第一步的时候只设置了一个国家，这里可以用一个列表遍历
    client = boto3.client('ec2', region_name=each_region, config=config)
    # 调用client.describe_instance()得到一个返回值
    response = client.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': [ 
                    'running',
                ]
             },
        ],
    )

    # 对返回的结果做解析，一般都是列表和字典，根据自己想要的信息做获取
    for each_list in response['Reservations']:
        for device in each_list['Instances']:

            keyName = device['KeyName']

            instanceTag = device['Tags']

            instanceIp = device['PrivateIpAddress']

#            print(instanceIp)

            arch = device['Architecture']


            if arch == "x86_64":
                for name in instanceTag:
                    if name['Key'] == "Name":
                        instanceName = name['Value'] 
                        instanceMessage = instanceName + ' ' + keyName

                        username = ['ec2-user','centos','ubuntu']
 
                        for user in username:
                            paramiko_config = {
                                'host': instanceIp,
                                'port': 22,
                                'username': user,
                                'key': keyName + '.pem',
                                }

                            paramik = ParamikoClient(paramiko_config)
                            if paramik.connects() == True:
                                result = paramik.exec_command("docker --version")
                                if result:
                                    #print(instanceName + ' ' + keyName + ' ' + bytes.decode(result))
                                    print(instanceName + ' '  + bytes.decode(result))

                     

