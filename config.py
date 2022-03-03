# @Time: 2022/3/3 10:45 上午
# @Author: Bruce

DB_USERNAME = 'root'
DB_PASSWORD = '12345678'
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
