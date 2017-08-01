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


def create_new_set():
    """
    创建新的Set_id
    :return:
    """
    set_id = None
    api = "/plugin/gif/api/v1.0.0/data_sets"
    conn = None
    try:
        set_name = u"十张让你笑的图"

        params = ({
            "op": "create",
            "where": {
                "name": set_name
            },
            "data": {
                "name": set_name,
                "thumb": "http://192.168.3.6:5001/res/dwowan/gif_download/bf6ba5ccda5cc3eee70b356b9f71762a.thumbnail.gif",
                "url": "http://192.168.3.6:5001/res/dwowan/gif_download/bf6ba5ccda5cc3eee70b356b9f71762a.thumbnail.gif",
                "description": "测试数据，好玩而已... 不要当真"
            }
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
            dataStr = response.read()
            dataJSON = json.loads(dataStr)

            if len(dataJSON[u'data']) > 0:
                ele = dataJSON[u'data'][0]
                set_id = ele[u'id']

    except Exception, e:
        trace(e)
    finally:
        if conn:
            conn.close()

    return set_id


def build_set_with_items2(set_id=None):
    if set_id is None:
        print(u'set_id is null')
        return

    api = "/plugin/gif/api/v1.0.0/data_set2items"

    def sub_create_data(set_id, item_id, order):
        try:
            params = ({
                "op": "create",
                "where": {
                    "set_id": set_id,
                    "item_id": item_id
                },
                "data": {
                    "set_id": set_id,
                    "item_id": item_id,
                    "order": order,
                    "bewrite": u"ItemID-%s 测试数据" % item_id
                }
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

        except Exception, e:
            trace(e)

        return False

    order_index = -1
    for item_id in range(64, 108):
        order_index = order_index + 1
        sub_create_data(set_id, item_id, order_index)




def build_set_with_items(set_id=None):
    if set_id is None:
        print(u'set_id is null')
        return

    api = "/plugin/gif/api/v1.0.0/sets_items_data"

    def sub_create_data(set_id, item_id, order):
        try:
            params = ({
                "op": "create",
                "where": {
                    "id": item_id,
                },
                'filter':{
                    'id': set_id
                },
                "data": {
                    "order": order,
                    "bewrite": u"ItemID-%s 测试数据" % item_id
                }
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

        except Exception, e:
            trace(e)

        return False

    order_index = 0
    for item_id in [11, 12, 13, 14, 15, 16, 17, 18, 19]:
        sub_create_data(set_id, item_id, order_index)
        ++order_index


new_set_id = create_new_set()
build_set_with_items2(new_set_id)

print(u'......')
