# -*- coding: utf-8 -*-

"""
本实例用途：
用来创建Item与tag的对应关系，建立联系
1. 为以后用来管理Item与tag提供帮助

下面是具体用法

"""


# system
import httplib
import json
import trace

# lib
import pymongo


##
enable_use_test_server = True
office_files_url = 'files.gif.gmagon.com'
test_office_file_url = '192.168.3.6:5001'

office_gif_server = {
    "server": "api.gmagon.com",
    "port": None
}
test_gif_server = {
    "server": ["127.0.0.1", "192.168.3.6"][1],
    "port": 5000
}

gif_data_server = test_gif_server if enable_use_test_server else office_gif_server
gif_files_url = test_office_file_url if enable_use_test_server else office_files_url


##
def post_data_to_server(api):
    """
    上传数据到gif server
    :param item:
    :return:
    """

    try:
        params = ({
            "op": "create",
            "where": "id = 64",  # 过滤Tags
            "filter": "id = 1"  # 过滤Set
        })

        body = json.JSONEncoder().encode(params)
        headers = {
            "Content-Type": "application/json",
            "Accept": "text/plain"
        }

        conn = httplib.HTTPConnection(gif_data_server["server"], gif_data_server["port"])
        conn.request(method="POST", url=api, body=body, headers=headers)
        response = conn.getresponse()
        if response.status == 200:
            return True

    except Exception , e:
        trace(e)

    return False


server_api = "/plugin/gif/api/v1.0.0/sets_tags_data"
post_data_to_server(server_api)


print(u'......')
