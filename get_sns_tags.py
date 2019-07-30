import boto3
from botocore.config import Config

#指定区域
region=['ap-southeast-1','eu-west-1','us-west-2']
each_region='ap-southeast-1'
#设置client的连接信息，不设置，默认值为3，超时的时候会报错，所以设置大一点
config = Config(
        retries=dict(
            max_attempts=20
        )
    )

def _get_cost():


    client = boto3.client('cur',region_name=each_region,config=config)
    response=client.describe_report_definitions()
    print(response)

_get_cost()