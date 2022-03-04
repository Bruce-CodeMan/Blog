# @Time: 2022/3/3 1:15 下午
# @Author: Bruce

import string
import random
from flask import Blueprint, request, current_app
from exts import cache
from utils import restful

bluePrint = Blueprint("fronts", __name__, url_prefix="/")


# 首页
@bluePrint.route("/")
def index():
    return "hello"


# 登录
@bluePrint.route("/login", methods=["GET"])
def login():
    if request.method == 'GET':
        return "hello front"


# 发送邮件
@bluePrint.get("/email/capture")
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

