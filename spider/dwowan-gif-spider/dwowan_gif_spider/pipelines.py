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

        self.base_dir = u'/Users/ian/gmagon_projects/gmagon_all/files.gif.gmagon.com/docs/res/'
        self.save_dir = self.base_dir + u'dwowan/gif_download/'

        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        self.f = open(self.save_dir + 'url_gif.txt', 'wb')

    # 爬虫启动时调用，处理获取到的item数据,注意item是每一个页面的数据集合
    def process_item(self, item, spider):
        # 去除没用的数据
        if item['gif_url']:

            # 遍历每个页面item集合里面的所有url
            # 字符串判断，过滤所有.jpg和.png文件，只下载gif文件
            # 将url插入mongo数据库
            # 将url存放进txt，稍后可以用迅雷下载
            index_comment = -1
            for one_gif_url in item['gif_url']:
                index_comment += 1

                if ".gif" in one_gif_url:
                    self.f.write(one_gif_url)
                    self.f.write('\r\n')

                    fname, ext = os.path.splitext(os.path.basename(one_gif_url))
                    save_file_path = self.save_dir + '%s.gif' % fname

                    print ('gif_image_save: %s' % save_file_path)

                    # 检查是否文件已经下载过，没有下载过，进行下载
                    if not os.path.isfile(save_file_path):
                        urllib.urlretrieve(one_gif_url, save_file_path, downloadCallback)

                    file_md5 = md5Checksum(save_file_path)

                    # 查询数据库是否已经有记录
                    found_count = self.collection.find({'file_md5': file_md5}).count()
                    if found_count < 1:
                        gif_url = [{
                            'site': 'dwowan',
                            "org_url": one_gif_url,
                            'url': u'https://files.gif.gmagon.com/res/dwowan/gif_download/' + '%s.gif' % fname,
                            'save_file_path': save_file_path,
                            'file_md5': file_md5,
                            "comment": item['gif_comment'][index_comment]
                        }]
                        self.collection.insert(gif_url)

        else:
            raise DropItem(item)
        return item


        # 爬虫关闭时调用

    def close_spider(self, spider):
        print("Done")
