# @Time: 2022/3/3 10:45 上午
# @Author: Bruce
import os
from datetime import timedelta

# 配置数据库
DB_USERNAME = 'root'
DB_PASSWORD = '123456'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'blog'

DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME,
                                                          DB_PASSWORD,
                                                          DB_HOST,
                                                          DB_PORT,
                                                          DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 配置邮箱
# MAIL_USE_TLS: 端口号587
# MAIL_USE_SSL: 端口号465
# QQ邮箱不支持非加密凡事发送邮件
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
# 如果指定MAIL_USE_SSL=True,那MAIL_PORT=465
MAIL_USERNAME = "1033684650@qq.com"
MAIL_PASSWORD = "bgqoazpxnckfbcjb"
MAIL_DEFAULT_SENDER = "1033684650@qq.com"

# 配置celery的redis
CELERY_BROKER_URL = "redis://127.0.0.1:6379/8"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/8"

# Flask-Caching的配置
CACHE_TYPE = 'redis'
CACHE_DEFAULT_TIMEOUT = 120
CACHE_REDIS_HOST = '127.0.0.1'
CACHE_REDIS_PORT = 6379

# 设置secret key
SECRET_KEY = "bruce"


# 设置项目的跟路径
# dirname就可以获取当前所在文件的文件夹，就是Blog
BASE_DIR = os.path.dirname(__file__)

# session.permanent=True的情况下设置过期时间
PERMANENT_SESSION_LIFETIME = timedelta(days=7)
