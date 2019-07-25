from elasticsearch import Elasticsearch
import requests
import json
import datetime
from ESS_DB import DB

# 通过ES的接口获取所有document的位置信息

class Connect(object):

    def get_all_location(self):

        date = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y.%m.%d')
        now = datetime.date.today().strftime('%Y-%m-%d')

        url = 'http://username:password@IP:9200/' + \
              'wazuh-alerts-3.x-' + date + '/_search?q=attack&size=10000'
        #print(url)
        response = requests.get(url)
        message = json.loads(response.text)
        #print(message['hits']['hits'])

        config = {
            "host": "****",
            "port": 3306,
            "user": "****",
            "password": "****",
            "db": "****",
            "charset": "utf8"
        }
        db = DB(config)

        for i in message['hits']['hits']:
            indexs = i['_index']
            id = i['_id']
            if 'city_name' in i['_source']['GeoLocation']:
                city_name = i['_source']['GeoLocation']['city_name']
            else:
                city_name = "NULL"
            if 'country_name' in i['_source']['GeoLocation']:
                country_name = i['_source']['GeoLocation']['country_name']
            else:
                country_name = "NULL"
            if 'region_name' in i['_source']['GeoLocation']:
                region_name = i['_source']['GeoLocation']['region_name']
            else:
                region_name = "NULL"
            location_lon = i['_source']['GeoLocation']['location']['lon']
            location_lat = i['_source']['GeoLocation']['location']['lat']

            sql = """insert into index_message(dates, indexs, index_id,city_name,country_name,region_name,location_lon,location_lat) value(
                         '%s','%s','%s','%s','%s','%s',%s,%s)""" % (now, indexs, id, city_name,country_name, region_name, location_lon, location_lat)

            db.insert_table(sql)
            #print(index, id, city_name, country_name, region_name, location_lon, location_lat)
        db.close()





if __name__ == "__main__":
    ess = Connect()
    ess.get_all_location()
