# @Time: 2022/3/3 1:15 下午
# @Author: Bruce
# @Description : 博客的视图函数

import os
import time
import string
import random
from flask import (
    Blueprint,
    request,
    current_app,
    render_template,
    make_response,
    session,
    redirect,
    g,
    jsonify,
    url_for
)
from exts import cache, db
from utils import restful
from utils.captcha import Captcha
from hashlib import md5
from io import BytesIO
from . import forms
from models import auth, border
from .decorator import login_required
from flask_avatars import Identicon
from flask_paginate import get_page_parameter, Pagination
from sqlalchemy import func
from flask_jwt_extended import create_access_token

front = Blueprint("front", __name__, url_prefix="/")


# 钩子函数
@front.before_request
def front_before_request():
    if 'user_id' in session:
        user_id = session.get('user_id')
        user = auth.UserModel.query.get(user_id)
        setattr(g, "user", user)


# 上下文处理器
@front.context_processor
def front_context_processor():
    if hasattr(g, "user"):
        return {"user": g.user}
    else:
        return {}


# 首页
@front.route("/")
def index():
    # 排序
    sort = request.args.get("st", type=int, default=1)
    # 过滤
    bd = request.args.get("bd", type=int, default=None)
    borders = border.BorderModel.query.order_by(border.BorderModel.priority.desc()).all()
    posters_query = border.PosterModel.query
    if sort == 1:
        posters_query = posters_query.order_by(border.PosterModel.create_time.desc())
    else:
        posters_query = db.session.query(border.PosterModel).\
            outerjoin(border.CommentModel).\
            group_by(border.PosterModel.id).\
            order_by(func.count(border.CommentModel.id).desc(), border.PosterModel.create_time.desc())

    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * current_app.config["PER_PAGE_COUNT"]
    end = start + current_app.config["PER_PAGE_COUNT"]

    if bd:
        posters_query = posters_query.filter(border.PosterModel.border_id==bd)
    # 同级帖子数
    total = posters_query.count()

    posters = posters_query.slice(start, end)
    pagination = Pagination(bs_version=3, page=page, total=total)

    # 轮播图的界面
    banners = border.BannerModel.query.order_by(border.BannerModel.priority.desc()).all()
    context = {
        "borders": borders,
        "posters": posters,
        "pagination": pagination,
        "st": sort,
        "bd": bd,
        "banners": banners
    }
    return render_template("front/index.html", **context)


# 登录
@front.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("front/login.html")
    else:
        form = forms.LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember_me = form.remember_me.data
            user = auth.UserModel.query.filter_by(email=email).first()
            if not user:
                return restful.params_error("邮箱或者密码错误")
            if not user.check_password(password):
                return restful.params_error("邮箱或者密码错误")
            session['user_id'] = user.id
            token = ""
            if user.is_staff:
                token = create_access_token(identity=user.id)
            if remember_me == 1:
                # session的默认时间就是浏览器的关闭时间
                session.permanent = True
            print(user.to_dict())
            return restful.ok(data={"token": token, "user": user.to_dict()})
        else:
            return restful.params_error(form.messages[0])


# 退出
@front.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# 发送邮件
@front.get("/email/capture")
def email_capture():
    email = request.args.get('email')
    if not email:
        return restful.params_error(message="请先传入邮箱")

    # 随机生成六位验证码
    source = list(string.digits)
    code = "".join(random.sample(source, 6))
    print("code:", code)
    subject = "Bruce"
    body = "您的注册验证码:%s" % code
    current_app.celery.send_task("send_mail", (email, subject, body))
    cache.set(email, code)
    return restful.ok(message="success")


# 注册
@front.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("front/register.html")
    else:
        form = forms.RegisterForm(request.form)
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            identicon = Identicon()
            filenames = identicon.generate(text=md5(email.encode("utf-8")).hexdigest())
            avatar = filenames[0]
            user = auth.UserModel(username=username, email=email, password=password, avatar=avatar)
            db.session.add(user)
            db.session.commit()
            return restful.ok()
        else:
            message = form.messages[0]
            return restful.params_error(message)


# 图形验证码
@front.get("/graph/captcha")
def graph_captcha():
    # 返回的image是一个类
    captcha, image = Captcha.gene_graph_captcha()
    key = md5((captcha+str(time.time())).encode("utf-8")).hexdigest()
    cache.set(key, captcha)
    # 将image保存成二进制文件
    # with open("captcha.png", "wb") as fp:
    #    image.save(fp, "png")
    out = BytesIO()
    image.save(out, "png")
    # 在保存的时候，out的文件指针会指向最后一位
    # 所以在保存完毕的时候，要将指针归位
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = "image/png"
    # 3600秒就是1个小时
    resp.set_cookie("_graph_captcha_key", key, max_age=3600)
    return resp


# 个人设置
@front.get("/setting")
@login_required
def setting():
    return render_template("front/setting.html")


# 自定义上传头像
@front.post("/avatar/upload")
@login_required
def upload_avatar():
     form = forms.UploadAvatarForm(request.files)
     if form.validate():
         image = form.image.data
         filename = image.filename
         _, ext = os.path.splitext(filename)
         # 不适用用户上传的文件，容易被黑客攻击
         filename = md5((g.user.email + str(time.time())).encode("utf-8")).hexdigest() + ext
         image_path = os.path.join(current_app.config["AVATARS_SAVE_PATH"], filename)
         image.save(image_path)
         g.user.avatar = filename
         db.session.commit()
         return restful.ok(data={"avatar": filename})
     else:
         message = form.messages[0]
         return restful.params_error(message=message)


# 修改个人资料
@front.post("/profile/edit")
@login_required
def edit_profile():
    form = forms.EditProfileForm(request.form)
    if form.validate():
        signature = form.signature.data
        g.user.signature = signature
        db.session.commit()
        return restful.ok()
    else:
        return restful.params_error(form.messages[0])


# 发布帖子
@front.route("/poster/public", methods=["GET", "POST"])
@login_required
def poster_public():
    if request.method == "GET":
        borders = border.BorderModel.query.all()
        return render_template("front/public_poster.html", borders=borders)
    else:
        form = forms.UploadPosterForm(request.form)
        if form.validate():
            title = form.title.data
            board_id = form.board_id.data
            content = form.content.data
            try:
                board = border.BorderModel.query.get(board_id)
            except Exception as e:
                return restful.params_error("板块不存在")
            poster = border.PosterModel(
                title=title,
                content=content,
                border=board,
                author=g.user
            )
            db.session.add(poster)
            db.session.commit()
            return restful.ok(data={"poster_id": poster.id})
        else:
            return restful.params_error(message=form.messages[0])


# 帖子图片上传的保存路径
@front.post("/poster/image/upload")
@login_required
def poster_image_upload():
    form = forms.UploadImgForm(request.files)
    if form.validate():
        image = form.image.data
        filename = image.filename
        _, ext = os.path.splitext(filename)
        filename = md5((g.user.email + str(time.time())).encode("utf-8")).hexdigest() + ext
        image_path = os.path.join(current_app.config["POSTERS_SAVE_PATH"], filename)
        image.save(image_path)
        return jsonify({
            "errno": 0,
            "data": [{
                "url": url_for("media.get_poster", filename=filename),
                "alt": filename,
                "href": ""
            }]
        })
    else:
        return restful.params_error(form.messages[0])


# 帖子详情页面
@front.get("/poster/detail/<int:poster_id>")
def poster_detail(poster_id):
    try:
        poster_model = border.PosterModel.query.get(poster_id)
    except Exception as e:
        return "404"
    return render_template("front/poster_detail.html", poster=poster_model)


# 发布评论
@front.post("/comment")
@login_required
def public_comment():
    form = forms.PublicCommentForm(request.form)
    if form.validate():
        content = form.content.data
        poster_id = form.poster_id.data
        try:
            border.PosterModel.query.get(poster_id)
        except Exception as e:
            return restful.params_error(message="帖子不存在")
        comment = border.CommentModel(content=content,
                                      poster_id=poster_id,
                                      author_id=g.user.id)
        db.session.add(comment)
        db.session.commit()
        return restful.ok()
    else:
        return restful.params_error(form.messages[0])
