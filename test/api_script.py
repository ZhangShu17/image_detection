# -*- coding: utf-8 -*-

import requests
import json
# r = requests.post('http://127.0.0.1:8000/account/create')
# print(r.text)

# 登陆信息
# url = 'http://127.0.0.1:8000/'
# data = {
#     'gender': u'男',
#     'age': '50',
#     'longitude': '30.8087',
#     'latitude': '40.9673',
# }
# files = {
#     'file': open('E:\\project_django\\opencv\\build.jpg', 'rb')
# }
#
# params = {
#     'mode': 1
# }
#
# r = requests.post('http://127.0.0.1:8000/face_detection/', data=data, files=files)
# json_data = json.loads(r.text)
# print(r.text)
# print(json_data)
# print(type(json_data))

# 车辆轨迹  POST请求
url = 'http://132.232.84.235:8000/transaction/'
data = {
    'longitude': '30.809',
    'latitude': '90.0987',
    'velocity': 6.8,
    'angle': 30.8,
    'obstacle': []
}
# n表示障碍物的数量
n=5
for i in range(n):
    obstac = {
        'length': 0.6, # 表示障碍物长度
        'width': 0.3, # 表示障碍物宽度
        'height': 0.2, # 表示障碍物高度
        'distance': 1.4, # 表示距离车辆距离
        'angle': 30.6# 表示距离车轴线角度   正负定义: 车尾-车头为基准，顺时针为正，逆时针为负， 角度-180---+180
    }
    data['obstacle'].append(obstac)


def post_transaction(url, data):
    r = requests.post(url=url, json=json.dumps(data))

    json_data = json.loads(r.text)
    return json_data['retCode']
	
	
# 这个是get请求请求
r = requests.get(url=url)
print(r.text)
json_data = json.loads(r.text)
print(json_data)


	
	
	
url = 'http://132.232.84.235:8000/obstacle/'
data={
    'length': 1.2,
	'width': 0.7,
	'height': 0.3,
	'distance': 0.2,
	'angle': 0.5
}
def post_obstacle(url, data):
    r = requests.post(url=url, data=data)
	json_data = json.loads(r.text)
	return json_data['retCode']
    



