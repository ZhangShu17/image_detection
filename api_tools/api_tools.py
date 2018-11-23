# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.response import Response
import dateutil.parser
import time
from qiniu import Auth, put_file, etag
import qiniu.config
from constants.constants import qiniu_ak, qiniu_sk, qiniu_bucket_name

def generate_error_response(error_message, error_type):
    return Response({'retCode': error_message[0],
                     'retMsg': error_message[1]}, error_type)


# 使用 dateutil 来解析时间字符串, 转换成时间戳，如果出错返回 None
def str_to_standard_timestamp(raw_date_str):
    try:
        d = dateutil.parser.parse(raw_date_str)
    except:
        return None
    return time.mktime(d.timetuple()) + d.microsecond / 1e6


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
    # print(info)
