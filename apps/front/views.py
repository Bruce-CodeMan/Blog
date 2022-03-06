# @Time: 2022/3/3 1:15 下午
# @Author: Bruce
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
    g
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
    borders = border.BorderModel.query.order_by(border.BorderModel.priority.desc()).all()
    return render_template("front/index.html", borders=borders)


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
            if remember_me == 1:
                # session的默认时间就是浏览器的关闭时间
                session.permanent = True
            return restful.ok()
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
        return render_template("front/poster_public.html", borders=borders)
