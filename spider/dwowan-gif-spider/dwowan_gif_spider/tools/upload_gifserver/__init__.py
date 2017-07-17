# -*- coding: utf-8 -*-


"""
模拟Http的处理逻辑，post，get
"""

# system
import httplib, urllib


def upload_data_with_mongodb(collection):
    """上传Mongodb中的数据到gifserver"""
    items = collection.find({'is_commit_server': False})
    pass