# @Time: 2022/3/3 10:38 上午
# @Author: Bruce
# @Description : 主的入口函数


import commands
from flask import Flask
from flask_migrate import Migrate
from models import auth
from apps.front import front
from apps.media import media
from blog_celery import make_celery


# 导入配置
import config
# 导入数据库
from exts import db, mail, cache, csrf, avatars

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
mail.init_app(app)
cache.init_app(app)
csrf.init_app(app)
avatars.init_app(app)

# 构建celery
celery = make_celery(app)

migrate = Migrate(app, db)

# 注册蓝图
app.register_blueprint(front)
app.register_blueprint(media)

# 注册命令
app.cli.command("init_board")(commands.init_boards)
app.cli.command("create_test_posters")(commands.create_test_posters)

if __name__ == '__main__':
    app.run()
