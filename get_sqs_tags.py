import boto3
from botocore.config import Config

#指定区域
region=['ap-southeast-1','eu-west-1','us-west-2']

#设置client的连接信息，不设置，默认值为3，超时的时候会报错，所以设置大一点
config = Config(
        retries=dict(
            max_attempts=20
        )
    )


country_code=['GH','NG','TZ']
env=['ci','prod','preprod','uat','test','dev']


#获取指定区域的队列的URL
def  _get_all_queues(each_region):
    client = boto3.client('sqs', region_name=each_region, config=config)
    response=client.list_queues()
    return response['QueueUrls']
    #打印队列的个数
    #print(len(response['QueueUrls']))


#获取指定区域的队列的queue_name,并以list的格式返回
def  _get_all_queue_name(each_region):
    client = boto3.client('sqs', region_name=each_region, config=config)
    response=client.list_queues()
    queue_name=[]
    for each_queue in response['QueueUrls']:
        queue_name.append(each_queue.split('/')[-1])   #处理格式，获取队列的名字
    return queue_name
    #打印队列的个数
    #print(len(response['QueueUrls']))


#根据队列的URL获取队列的详细信息
def _get_queues_attribute(url):
    client = boto3.client('sqs', region_name=each_region, config=config)
    response = client.get_queue_attributes(
        QueueUrl=url,
        AttributeNames=[
            'All',
        ]
    )
    return response

#对指定的queue打标签
def _create_tags(url,country_code,env_code):
    client = boto3.client('sqs', region_name=each_region, config=config)
    response = client.tag_queue(
        QueueUrl=url,
        Tags={
            'UsageCountry': country_code,
            'UsageEnvironment': env_code
        }
    )



#删除指定queue的标签
def _untag_queue(url,tag_name):
    client = boto3.client('sqs', region_name=each_region, config=config)
    response = client.untag_queue(
        QueueUrl=url,
        TagKeys=[
            tag_name,
        ]
    )



#对获取到的URL进行处理，获取他的queue_name,根据queue_name的信息对他进行标签
def _deal_queue(each_region):
    all_queue=_get_all_queues(each_region)
    for each_queue_url in all_queue:
        queue_name=each_queue_url.split('/')[-1]
        UsageCountry=''
        UsageEnvironment=''
        for sub_name in [name.upper() for name in queue_name.split('_')]:

            if sub_name in [code.upper() for code in country_code]:
                UsageCountry=sub_name
            if sub_name in [each_env.upper() for each_env in env]:
                UsageEnvironment=sub_name
            if UsageCountry.strip()=='':
                UsageCountry='NG'

        #_untag_queue(each_queue_url,UsageCountry)
        _create_tags(each_queue_url,UsageCountry,UsageEnvironment)

for each_region in region:
    _deal_queue(each_region)

