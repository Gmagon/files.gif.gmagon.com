# -*- coding: utf-8 -*-


def upload_data_with_mongodb(collection):
    """上传Mongodb中的数据到gifserver"""
    items = collection.find({'is_commit_server': False})
    pass