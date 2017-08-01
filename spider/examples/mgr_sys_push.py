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
    "server": ["127.0.0.1", "192.168.3.6"][0],
    "port": 5000
}

gif_data_server = test_gif_server if enable_use_test_server else office_gif_server
gif_files_url = test_office_file_url if enable_use_test_server else office_files_url


def build_data(api=None, in_params={}):
    if not api or not in_params:
        print("api or in_params is none...")
        return

    try:
        params = (in_params)
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


"""
查看当前的推送内容有哪些？
curl -i -H "Content-Type: application/json" http://127.0.0.1:5000/plugin/gif/api/v1.0.0/data_sys_push -d "{}" -X GET -v

curl -i -H "Content-Type: application/json" http://192.168.3.6:5000/plugin/gif/api/v1.0.0/data_sys_push -d "{\"where\":{\"name\":\"default.sys.push.recommend.carousel.data\"}}" -X GET -v

curl -i -H "Content-Type: application/json" http://127.0.0.1:5000/plugin/gif/api/v1.0.0/data_sets -d "{\"where\":\" id in (1,2,3,4,5,6) \"}" -X GET -v
"""

id_SysPushType = 7

# 1.默认的系统推送的轮播数据
name_item_SysPushType = "default.sys.push.recommend.carousel.data"
build_data(api="/plugin/gif/api/v1.0.0/data_sys_push", in_params={
    "op": "update",
    "where": {
        "name": name_item_SysPushType,
        "type_id": id_SysPushType,
    },
    "data": {
        "name": name_item_SysPushType,
        "type_id": id_SysPushType,
        "content": json.dumps(
            [
                {
                    "thumb": "http://192.168.3.6:5001/res/dwowan/gif_download/4f003cbbcd17992fb2a260b973d503fd.thumbnail.gif",
                    "id": 1,
                    "description": "让梦想起飞"
                },
                {
                    "thumb": "http://192.168.3.6:5001/res/dwowan/gif_download/fe69d07bb5a07bb157aabf9e051aadd5.thumbnail.gif",
                    "id": 2,
                    "description": "警察人生"
                },
                {
                    "thumb": "http://192.168.3.6:5001/res/dwowan/gif_download/baccdb621e7cf7c398891250f0f45da3.thumbnail.gif",
                    "id": 1,
                    "description": "让人温暖的微笑"
                },
                {
                    "thumb": "http://192.168.3.6:5001/res/dwowan/gif_download/5c285171467461ffe363fa4ba31e9f41.thumbnail.gif",
                    "id": 2,
                    "description": "倒霉事"
                },
                {
                    "thumb": "http://192.168.3.6:5001/res/dwowan/gif_download/18c4b973c4f5aee663b67ec26e20d957.thumbnail.gif",
                    "id": 1,
                    "description": "可口可乐"
                },
            ]
        ),
        "description": "配置系统默认推送的推荐部分的轮播图片"
    }
})

# 2.默认的系统个性推荐数据
name_item_SysPushType = "default.sys.push.recommend.sets.data"
build_data(api="/plugin/gif/api/v1.0.0/data_sys_push", in_params={

})

# Step4: 查询执行结果
# curl -i -H "Content-Type: application/json" http://127.0.0.1:5000/plugin/gif/api/v1.0.0/sets/1 -X GET -v
# curl -i -H "Content-Type: application/json" http://192.168.3.6:5000/plugin/gif/api/v1.0.0/sets/1 -X GET -v
print(u'......')
