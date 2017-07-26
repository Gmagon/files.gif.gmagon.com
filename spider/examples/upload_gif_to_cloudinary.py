# -*- coding: utf-8 -*-

# system
import httplib
import json
import trace
import os


key_cloudinary = "cloudinary://338794126122569:hln5rH9Ul8-QfsU5X4gVTRtXXt8@gmagonshare"

os.putenv("CLOUDINARY_URL", key_cloudinary)
os.environ["CLOUDINARY_URL"] =  key_cloudinary

# lib
import pymongo
from cloudinary.uploader import upload as cloudinary_upload
from cloudinary.utils import cloudinary_url


def dump_response(response):
    print("Upload response:")
    for key in sorted(response.keys()):
        print("  %s: %s" % (key, response[key]))

def post_gif_data_to_server(item):
    """
    上传数据到gif server
    :param item:
    :return:
    """

    try:
        response = cloudinary_upload(
            item[u'url'],
            public_id=item[u'file_md5'],
            folder="gif/dwowan/"
        )
        dump_response(response)
        img_url, options = cloudinary_url(response['public_id'],
            format= response['format'],
            width= 200,
            height= 150,
            crop= "fill"
        )
        return True

        


    except Exception , e:
        trace(e)

    return False


# 连接到MongoDB
print(u'connect localhost mongodb')
mongo_conn = pymongo.MongoClient('localhost', 27017)
mongo_db = mongo_conn['gif_url']
collection = mongo_db['gif_collection']

enable_recover = True ## 是否重新操作

if enable_recover:
    for item in collection.find({'is_commit_server': True}):
        collection.update_one({u'_id': item[u'_id']}, {"$set": {u'is_commit_server': False}})

# Find somethings are not upload in gif_server
items = collection.find({'is_commit_server': False})

if items.count() > 0:
    for item in items:
        if post_gif_data_to_server(item):
            collection.update_one({u'_id': item[u'_id']}, {"$set": {u'is_commit_server': True}})
            print (item)

print(u'......')
