# @Time: 2022/3/3 1:15 下午
# @Author: Bruce
import time
import string
import random
from flask import Blueprint, request, current_app, render_template, make_response
from exts import cache
from utils import restful
from utils.captcha import Captcha
from hashlib import md5
from io import BytesIO

front = Blueprint("fronts", __name__, url_prefix="/")


# 首页
@front.route("/")
def index():
    return "hello"


# 登录
@front.route("/login", methods=["GET"])
def login():
    if request.method == 'GET':
        return "hello front"


# 发送邮件
@front.get("/email/capture")
def email_capture():
    email = request.args.get('email')
    if not email:
        return restful.params_error(message="请先传入邮箱")

    # 随机生成六位验证码
    source = list(string.digits)
    code = "".join(random.sample(source, 6))
    subject = "Bruce"
    body = "您的注册验证码:%s" % code
    current_app.celery.send_task("send_mail", (email, subject, body))
    cache.set(email, code)
    return restful.ok(message="success")


# 注册
@front.get("/register")
def register():
    return render_template("front/register.html")


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