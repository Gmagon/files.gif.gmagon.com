# -*- coding: utf-8 -*-
# coding：UTF-8
import hashlib


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
