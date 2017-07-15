# -*- coding: utf-8 -*-

#lib
import pymongo


# 连接到MongoDB
print(u'connect localhost mongodb')
mongo_conn = pymongo.MongoClient('localhost', 27017)
mongo_db = mongo_conn['gif_url']
collection = mongo_db['gif_collection']

# Find somethings are not upload in gif_server
items_count = collection.find({'is_commit_server': False}).count()

if items_count > 0:
    for item in collection.find({'is_commit_server': False}):
        collection.update_one({u'_id': item[u'_id']}, {"$set": {u'is_commit_server': True}})
        print (item)

print(u'......')
