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


def build_data(set_id=None, api=None):
    if set_id is None:
        print(u'set_id is null')
        return

    def sub_create_data(set_id):
        try:
            params = ({
                "machine_id": "NOGUserMachines",
                "id": set_id
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

    sub_create_data(set_id)


# Step1: 创建Machines记录
# curl -i -H "Content-Type: application/json" http://127.0.0.1:5000/api/v1.0.0/machines -d "{\"op\":\"create\",\"where\":{\"id\":\"NOGUserMachines\"},\"data\":{\"id\":\"NOGUserMachines\"}}" -X POST -v
# curl -i -H "Content-Type: application/json" http://192.168.3.6:5000/api/v1.0.0/machines -d "{\"op\":\"create\",\"where\":{\"id\":\"NOGUserMachines\"},\"data\":{\"id\":\"NOGUserMachines\"}}" -X POST -v

# Step2: 创建User用户
# curl -i -H "Content-Type: application/json" http://127.0.0.1:5000/plugin/gif/api/v1.0.0/data_user -d "{\"op\":\"create\",\"where\":{\"machine_id\":\"NOGUserMachines\"},\"data\":{\"machine_id\":\"NOGUserMachines\"}}" -X POST -v
# curl -i -H "Content-Type: application/json" http://192.168.3.6:5000/plugin/gif/api/v1.0.0/data_user -d "{\"op\":\"create\",\"where\":{\"machine_id\":\"NOGUserMachines\"},\"data\":{\"machine_id\":\"NOGUserMachines\"}}" -X POST -v

# Step3: 执行构建记录
for set_id in range(1, 3):
    build_data(set_id, api ="/plugin/gif/api/v1.0.0/sets_download")
    build_data(set_id, api="/plugin/gif/api/v1.0.0/sets_preview")
    build_data(set_id, api="/plugin/gif/api/v1.0.0/sets_collection")
    build_data(set_id, api="/plugin/gif/api/v1.0.0/sets_share")

# Step4: 查询执行结果
# curl -i -H "Content-Type: application/json" http://127.0.0.1:5000/plugin/gif/api/v1.0.0/sets/1 -X GET -v
# curl -i -H "Content-Type: application/json" http://192.168.3.6:5000/plugin/gif/api/v1.0.0/sets/1 -X GET -v
print(u'......')
