import boto3
from botocore.config import Config

#Function：根据AWS API获取所有Instance的Tags并打到对应的卷组上,先删除所有卷组的标签，再重新根据Instance的打上
#Author  ：李先生
#Date    ：20190419
#Version ：V1.0


region=['eu-west-1','us-west-2','ap-southeast-1']


#在所有的卷都没有标签的情况下，获取主机的标签，达到对应的卷组上


def __create_tags(instanceid,key,value):
    response = client.create_tags(
        Resources=[
            instanceid,
        ],
        Tags =[
            {
                'Key': key,
                'Value': value,
            },
        ],
    )

    print(response)


def __delete_tags(instanceid,key,value):
    response = client.delete_tags(
        Resources=[
            instanceid,
        ],
        Tags =[
            {
                'Key': key,
                'Value': value,
            },
        ],
    )

    print(response)

for each_region in region:

    config = Config(
        retries=dict(
            max_attempts=20
        )
    )

    client = boto3.client('ec2',region_name=each_region,config=config)
    response = client.describe_instances()

    for each_list in response['Reservations']:
        for device in each_list['Instances']:
            instanceid=device['InstanceId']
            for each_tags in device['Tags']:
                key=each_tags['Key']
                value=each_tags['Value']
                key1=each_tags['Key']
                value1=each_tags['Value'].upper()
                if key != 'aws:elasticmapreduce:instance-group-role' and key != 'aws:elasticmapreduce:job-flow-id':
                    __delete_tags(instanceid, key, value)
                    __create_tags(instanceid, key1, value1)
                    print(instanceid,key,value)
                    print(instanceid,key1,value1)


