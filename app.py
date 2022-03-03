# @Time: 2022/3/3 10:38 上午
# @Author: Bruce

from flask import Flask
from flask_migrate import Migrate
from models import auth
# 导入配置
import config
# 导入数据库
from exts import db

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

migrate = Migrate(app, db)


@app.route("/")
def index():
    return "hello"


if __name__ == '__main__':
    app.run()
