import boto3

#Function：根据AWS API给指定的Volumn ID打上指定的标签
#Author  ：李先生
#Date    ：20190419
#Version ：V1.0

client = boto3.client('ec2',region_name='ap-southeast-1')
response = client.create_tags(
    Resources=[
        'vol-03dfe5d125ce7956a',
    ],
    Tags=[
        {
            'Key': 'UsageService',
            'Value': 'OPS-Monitor',
        },
    ],
)

print(response)




