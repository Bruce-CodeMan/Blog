# @Time: 2022/3/3 10:38 上午
# @Author: Bruce

from flask import Flask
from flask_migrate import Migrate
from models import auth
from apps.fronts import bluePrint
from blog_celery import make_celery

# 导入配置
import config
# 导入数据库
from exts import db, mail

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
mail.init_app(app)

# 构建celery
celery = make_celery(app)

migrate = Migrate(app, db)

# 注册蓝图
app.register_blueprint(bluePrint)


if __name__ == '__main__':
    app.run()