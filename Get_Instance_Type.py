import boto3
from botocore.config import Config

#Function：根据AWS Instance的Image Id获取所有Instance的系统是Linux还是Windows
#Author  ：李先生
#Date    ：20191028
#Version ：V1.0
#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_images

config = Config(
    retries=dict(
        max_attempts=20
    )
)
client = boto3.client('ec2', config=config)

def get_ami_arch(amiName):
    response = client.describe_images(
        ImageIds=[
            amiName,
        ]

    )
    #i386 | x86_64 | arm64
    for arch in response['Images']:
        Architecture = arch['Architecture']
    return Architecture

