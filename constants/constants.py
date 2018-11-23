# coding=utf-8

# 这两个是识别的人脸和车辆存放在服务器的绝对路劲
face_dir_path = 'E:\\project_django\\detection\\face_django\\'
car_dir_path = 'E:\\project_django\\detection\\car_django\\'


socket_host = '127.0.0.1'
socker_port = 8080

qiniu_ak = 'oSdS21mNqwRN08uTNbi0Go4bkmS5ZDj3l5Tk8kHu'
qiniu_sk = 'lvtKr6BSGwgYEMIJ3mgW91GFbBy0UF6nbn-mZL7g'
qiniu_bucket_name = 'face-detection'

# 这个用nginx或者tomcat配置网络文件地址，按照实际情况修改
base_url = 'http://127.0.0.1/face_django/'