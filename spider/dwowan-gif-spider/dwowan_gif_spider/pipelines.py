# -*- coding: utf-8 -*-
# coding：UTF-8
import urllib
import urllib2
import time
import os
import shutil
import hashlib
import uuid
from scrapy.exceptions import DropItem
import pymongo


def md5Checksum(filePath):
    """获取文件的md5值"""
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

def downloadCallback(blocknum, blocksize, totalsize):
    """
    回调函数
    :param blocknum: 已经下载的数据块
    :param blocksize: 数据块的大小
    :param totalsize: 远程文件的大小
    :return:
    """

    percent = 100.0 * blocknum * blocksize / totalsize
    if percent > 100:
        percent = 100
    print("%.2f%%" % percent)



# Pineline用于处理获取到的item数据
class GifPipeline(object):
    # 启动爬虫时执行，新建一个名为gif_download的文件
    # 创建一个名为gif_url的mongo数据库, 并创建一个集合my_collection
    # 创建一个名为gif_url的txt文件
    def __init__(self):
        conn = pymongo.MongoClient('localhost', 27017)
        db = conn['gif_url']
        self.collection = db['gif_collection']

        self.save_dir = u''

        curDir = os.getcwdu()

        self.f = open('url_gif.txt', 'wb')

        if os.path.exists('gif_download'):
            shutil.rmtree("gif_download")
        else:
            os.mkdir("gif_download")

    # 爬虫启动时调用，处理获取到的item数据,注意item是每一个页面的数据集合
    def process_item(self, item, spider):
        # 去除没用的数据
        if item['gif_url']:

            # 遍历每个页面item集合里面的所有url
            # 字符串判断，过滤所有.jpg和.png文件，只下载gif文件
            # 将url插入mongo数据库
            # 将url存放进txt，稍后可以用迅雷下载
            index_comment = -1
            for i in item['gif_url']:
                index_comment += 1
                if ".gif" in i:
                    self.f.write(i)
                    self.f.write('\r\n')

                    fname = 'gif_download/%s.gif' % uuid.uuid4().hex
                    result = urllib.urlretrieve(i, fname, downloadCallback)

                    # 文件路径

                    gif_url = [{
                        'site':'',
                        "url": i,
                        "comment": item['gif_comment'][index_comment]
                    }]
                    self.collection.insert(gif_url)

                    print ('%s\n' % result)
        else:
            raise DropItem(item)
        return item


        # 爬虫关闭时调用

    def close_spider(self, spider):
        print("Done")