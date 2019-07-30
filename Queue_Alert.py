import boto3
from botocore.config import Config
import json, urllib.request
import re

# 指定区域
region = ['ap-southeast-1', 'eu-west-1', 'us-west-2']

# 设置client的连接信息，不设置，默认值为3，超时的时候会报错，所以设置大一点
config = Config(
        retries=dict(
            max_attempts=20
        )
    )


# 获取指定区域的队列的URL
def _get_all_queues(each_region):
    client = boto3.client('sqs', region_name=each_region, config=config)
    response = client.list_queues()
    # print(response)

    # 打印队列的个数
    # print(len(response['QueueUrls']))
    if 'QueueUrls' in response:
        return response['QueueUrls']


#获取指定区域的队列的queue_name,并以list的格式返回
def _get_all_queue_name(each_region):
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

def send_to_ding(contents,access_token):
    header = {
        "Content-Type": "application/json",
        "charset": "utf-8"
        }
    data = {
         "msgtype": "text",
            "text": {
                "content": contents + '@tel1,@tel2'
            },
         "at": {
            "atMobiles": [
                "tel1",
                'tel2',
            ],
                "isAtAll":False   # at为非必须
             }
        }
    sendData = json.dumps(data)
    request = urllib.request.Request(access_token, data=sendData.encode(encoding='UTF8'), headers=header)
    urlopen = urllib.request.urlopen(request)
    print(urlopen.read())


if __name__ == '__main__':
    # DingDing的access_token
    other_access_token = 'xxxx'
    prod_access_token = 'xxxx'

    for each_region in region:
        all_queue = _get_all_queues(each_region)

        for all_url in all_queue:
            queue_name = all_url.split('/')[4]
            response = _get_queues_attribute(all_url)

            if re.findall('_prod_', all_url, flags=re.IGNORECASE):
                access_token = prod_access_token
            else:
                access_token = other_access_token

            # 队列中的消息数量
            message = response['Attributes']['ApproximateNumberOfMessages']

            # 队列中延迟且无法立即读取的消息数量
            delay_message = response['Attributes']['ApproximateNumberOfMessagesNotVisible']

            # 处于飞行状态的队列数量
            fly_message = response['Attributes']['ApproximateNumberOfMessagesDelayed']

            if int(message) > 10:
                content = "队列中的消息数量大于10，请李乐、再方两位小同学关注此队列" + queue_name
                send_to_ding(content, access_token)
            if int(delay_message) > 10:
                content = "队列中延迟且无法立即读取的消息数量大于10，请李乐、再方同学关注此队列" + queue_name
                send_to_ding(content, access_token)
            if int(fly_message) > 10:
                content = "处于飞行状态的队列数量大于10，请李乐、再方同学关注此队列" + queue_name
                send_to_ding(content, access_token)



