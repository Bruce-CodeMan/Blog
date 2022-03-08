# @Time : 2022/3/6 23:11 
# @Author : Bruce
# @Description : 博客的数据库模型


from exts import db
from datetime import datetime


# 板块
class BorderModel(db.Model):
    __tablename__ = "border"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True)
    priority = db.Column(db.Integer, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)


# 帖子
class PosterModel(db.Model):
    __tablename__ = "poster"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.TEXT, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    border_id = db.Column(db.Integer, db.ForeignKey("border.id"))
    author_id = db.Column(db.String(100), db.ForeignKey("user.id"))
    border = db.relationship("BorderModel", backref=db.backref("posters"))
    author = db.relationship("UserModel", backref=db.backref("posters"))


# 轮播图
class BannerModel(db.Model):
    __tablename__ = "banner"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    link_url = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)


class CommentModel(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    poster_id = db.Column(db.Integer, db.ForeignKey("poster.id"))
    author_id = db.Column(db.String(100), db.ForeignKey("user.id"), nullable=False)

    post = db.relationship("PosterModel", backref=db.backref('comments', order_by="CommentModel.create_time.desc()", cascade="delete, delete-orphan"))
    author = db.relationship("UserModel", backref='comments')