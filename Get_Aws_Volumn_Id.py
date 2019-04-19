import boto3
from botocore.config import Config

#Function：根据AWS API获取所有的Volumn ID
#Author  ：李先生
#Date    ：20190419
#Version ：V1.0

# 指定区域
region = ['eu-west-1', 'us-west-2', 'ap-southeast-1']

# 设置client的连接信息，不设置，默认值为3，超时的时候会报错，所以设置大一点
config = Config(
    retries=dict(
        max_attempts=20
    )
)

for each_region in region:
    client = boto3.client('ec2',region_name=each_region,config=config)
    response = client.describe_volumes()

    for each in response['Volumes']:
        for volumn_id in each['Attachments']:
            print(volumn_id['VolumeId'])