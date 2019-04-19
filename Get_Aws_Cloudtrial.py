import boto3,json
from datetime import datetime
from botocore.config import Config

#Function：根据AWS API获取所有cludtrail的信息，可以对其做分析
#Author  ：李先生
#Date    ：20190419
#Version ：V1.0

region=['ap-southeast-1']

config = Config(
    retries=dict(
        max_attempts=20
    )
)
for each_region in region:
    client = boto3.client('cloudtrail', region_name=each_region, config=config)

    response = client.lookup_events(
        LookupAttributes=[
            {
            'AttributeKey': 'EventName',
            'AttributeValue': 'RunInstances'
            }
        ],
        StartTime=datetime(2018, 1, 1)
    )
    for each_events in response['Events']:
        event_name=each_events['EventName']
        event_user=each_events['Username']

        for each in json.loads(each_events['CloudTrailEvent'])['responseElements']['instancesSet']['items']:
            print(each['instanceId'])

