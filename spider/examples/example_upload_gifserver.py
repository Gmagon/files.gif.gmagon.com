# -*- coding: utf-8 -*-

# system
import httplib
import urllib

# lib
import pymongo


def post_gif_data_to_server(item, api):
    """
    上传数据到gif server
    :param item:
    :return:
    """

    params = urllib.urlencode({
        "op": "create",
        "where": {
            "md5": item[u'file_md5']
        },
        "data": {
            "name": item[u'name'],
            "thumb": item[u'thumb'],
            "url": item[u'url'],
            "size": item[u'size'],
            "dimensions": item[u'dimensions'],
            "ext": item[u'ext'],
            "md5": item[u'file_md5'],
            "description": item[u'comment']
        }
    })
    headers = {
        "Content-Type: application/json"
    }

    conn = httplib.HTTPConnection(api)
    conn.request("POST", "", params, headers)
    responese = conn.getresponse()

    return False


# 连接到MongoDB
print(u'connect localhost mongodb')
mongo_conn = pymongo.MongoClient('localhost', 27017)
mongo_db = mongo_conn['gif_url']
collection = mongo_db['gif_collection']

# Find somethings are not upload in gif_server
items_count = collection.find({'is_commit_server': False}).count()

server_api = "http://127.0.0.1:5000/plugin/gif/api/v1.0.0/data_items"

if items_count > 0:
    for item in collection.find({'is_commit_server': False}):
        if post_gif_data_to_server(item, server_api):
            collection.update_one({u'_id': item[u'_id']}, {"$set": {u'is_commit_server': True}})
            print (item)

print(u'......')
