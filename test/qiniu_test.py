# -*- coding: utf-8 -*-
from constants.constants import qiniu_ak, qiniu_sk, qiniu_bucket_name
from qiniu import Auth, put_file, etag

def upload_pic(file_name, file_path):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = qiniu_ak
    secret_key = qiniu_sk
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = qiniu_bucket_name
    # 上传到七牛后保存的文件名
    key = file_name
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    # 要上传文件的本地路径
    localfile = file_path
    ret, info = put_file(token, key, localfile)
    print(info)
    # assert ret['key'] == key
    # assert ret['hash'] == etag(localfile)

file_name = '1542631178.jpg'
file_path = 'E:\\project_django\\detection\\face\\1542631178.jpg'
upload_pic(file_name, file_path)