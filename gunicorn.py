# @Author : Bruce
# @Time : 2022/3/14 21:41 
# Description : 服务器的部署


import multiprocessing

bind = "127.0.0.1:5000"
workers = multiprocessing.cpu_count() * 2 + 1
threads = 10
accesslog = "/var/log/Blog/access.log"
errorlog = "/var/log/Blog/error.log"
preload_app = True
daemon = True
