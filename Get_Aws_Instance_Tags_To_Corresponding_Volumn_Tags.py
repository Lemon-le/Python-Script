import boto3
from botocore.config import Config

#Function：#在所有的卷都没有标签的情况下，获取主机的标签，达到对应的卷组上
#Author  ：李先生
#Date    ：20190419
#Version ：V1.0

#指定AWS上的区域
region=['eu-west-1','us-west-2','ap-southeast-1']


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
                for volumn in device['BlockDeviceMappings']:
                    volumID=volumn['Ebs']['VolumeId']
                    print(instanceid,volumID,key,value)
                    if key != 'aws:elasticmapreduce:instance-group-role' and key != 'aws:elasticmapreduce:job-flow-id':
                        #删除标签
                        #response = client.delete_tags(
                        #创建标签
                        response = client.create_tags(
                            Resources=[
                                volumID,
                            ],
                            Tags=[
                                {
                                    'Key': key,
                                    'Value': value,
                                },
                            ],
                        )

                        print(response)

