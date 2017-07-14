# -*- coding: utf-8 -*-
# coding：UTF-8
import urllib
import urllib2
import time
import os
import shutil
import hashlib
import datetime


# Libs
import pymongo
from gittle import Gittle
from scrapy.exceptions import DropItem
from PIL import Image
from images2gif import readGif, writeGif






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


def getAutoThumbSize(orgSize, min_spec):
    org_width, org_height = orgSize

    dest_width = dest_height = min_spec
    w_ratio = h_ratio = 1
    w_ratio = int(org_height / min_spec)
    h_ratio = int(org_width / min_spec)
    ratio = min(w_ratio, h_ratio)
    ratio = ratio if ratio > 1 else 1

    return (org_width/ratio, org_height/ratio)

def resize_gif(path, save_as=None, resize_to=None):
    """
    Resizes the GIF to a given length:

    Args:
        path: the path to the GIF file
        save_as (optional): Path of the resized gif. If not set, the original gif will be overwritten.
        resize_to (optional): new size of the gif. Format: (int, int). If not set, the original GIF will be resized to
                              half of its size.
    """
    all_frames = extract_and_resize_frames(path, resize_to)

    if not save_as:
        save_as = path

    if len(all_frames) == 1:
        print("Warning: only 1 frame found")
        all_frames[0].save(save_as, optimize=True)
    else:
        all_frames[0].save(save_as, optimize=True, save_all=True, append_images=all_frames[1:], loop=1000)


def analyseImage(path):
    """
    Pre-process pass over the image to determine the mode (full or additive).
    Necessary as assessing single frames isn't reliable. Need to know the mode
    before processing all frames.
    """
    im = Image.open(path)
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return results


def extract_and_resize_frames(path, resize_to=None):
    """
    Iterate the GIF, extracting each frame and resizing them

    Returns:
        An array of all frames
    """
    mode = analyseImage(path)['mode']

    im = Image.open(path)

    if not resize_to:
        resize_to = (im.size[0] // 2, im.size[1] // 2)

    i = 0
    p = im.getpalette()
    last_frame = im.convert('RGBA')

    all_frames = []

    try:
        while True:
            # print("saving %s (%s) frame %d, %s %s" % (path, mode, i, im.size, im.tile))

            '''
            If the GIF uses local colour tables, each frame will have its own palette.
            If not, we need to apply the global palette to the new frame.
            '''
            if not im.getpalette():
                im.putpalette(p)

            new_frame = Image.new('RGBA', im.size)

            '''
            Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image?
            If so, we need to construct the new frame by pasting it on top of the preceding frames.
            '''
            if mode == 'partial':
                new_frame.paste(last_frame)

            new_frame.paste(im, (0, 0), im.convert('RGBA'))

            new_frame.thumbnail(resize_to, Image.ANTIALIAS)
            all_frames.append(new_frame)

            i += 1
            last_frame = new_frame
            im.seek(im.tell() + 1)
    except EOFError:
        pass

    return all_frames




def runGit(working_dir):
    """执行Git提交及push动作"""
    repo_path = working_dir
    repo_url = u'https://lauer3912:Hapsion1985@github.com/Gmagon/files.gif.gmagon.com.git'
    repo = Gittle(repo_path, origin_uri=repo_url)

    want_add =  want_commit = False

    # 检查是否有新增的文件
    print (u'#检测是否有新增的文件.....')
    untrackedObj = repo.modified_unstaged_files
    if len(untrackedObj) > 0:
        #print(repo.add(untrackedObj))
        want_add = True

    # 检查是否有变化的文件
    print (u'#检测是否有修改的文件.....')
    diffObj = repo.modified_unstaged_files
    if len(diffObj) > 0:
        now = datetime.datetime.now()
        nowStr = now.strftime('%Y-%m-%d %H:%M:%S')

        commit_user = 'Ian'
        commit_user_email = 'ian@gmagon.com'
        commit_msg = '%s dwowan gif update [fileChanges=%d] [fileAdd=%d]' % (nowStr, len(diffObj), len(untrackedObj))

        repo.stage(diffObj)

        print (repo.commit(name=commit_user, email=commit_user_email, message=commit_msg))

        want_commit = True

    # 检测是否需要push到远程服务器中
    print (u'#检测是否需要上传到远程服务器.....')
    if want_commit or want_add:
        print(u'git push')
        repo.push(branch_name='master')
        print ('git end')


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

                    if os.path.isfile(save_file_path):
                        file_md5 = md5Checksum(save_file_path)
                        try:
                            with Image.open(save_file_path) as im:
                                dimensions = '%dx%d' % im.size

                                # thumb gif
                                thumb_file = os.path.splitext(save_file_path)[0] + '.thumbnail.gif'
                                thumb_size = getAutoThumbSize(im.size, 64)
                                # im.seek(im.tell() + 1)

                                # 获得缩图
                                if not os.path.isfile(thumb_file):
                                    resize_gif(save_file_path, thumb_file, thumb_size)

                                # 查询数据库是否已经有记录
                                found_count = self.collection.find({'file_md5': file_md5}).count()
                                if found_count < 1:
                                    gif_url = [{
                                        'site': 'dwowan',
                                        "org_url": one_gif_url,
                                        'url': u'http://files.gif.gmagon.com/res/dwowan/gif_download/' + '%s.gif' % fname,
                                        'thumb': u'http://files.gif.gmagon.com/res/dwowan/gif_download/' + '%s.thumbnail.gif' % fname,
                                        'save_file_path': save_file_path,
                                        'file_md5': file_md5,
                                        'ext': ext,
                                        'dimensions': dimensions,
                                        'size': os.path.getsize(save_file_path),
                                        'is_commit_server': False,  # 是否提交到了远程数据库
                                        "comment": item['gif_comment'][index_comment]
                                    }]
                                    self.collection.insert(gif_url)

                        except IOError:
                            print('cannot create thumbnail for', save_file_path)



        else:
            raise DropItem(item)
        return item


    # 爬虫关闭时调用
    def close_spider(self, spider):
        work_dir = u'/Users/ian/gmagon_projects/gmagon_all/files.gif.gmagon.com/'
        runGit(working_dir=work_dir)

        
        print("Done")
