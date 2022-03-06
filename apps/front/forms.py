# @Time : 2022/3/6 12:39
# @Author : Bruce

from wtforms import Form, ValidationError
from wtforms.fields import StringField, IntegerField, FileField
from wtforms.validators import Email, Length, EqualTo
from flask_wtf.file import FileAllowed, FileSize
from models.auth import UserModel
from exts import cache
from flask import request


class BaseForm(Form):
    @property
    def messages(self):
        message_list = []
        if self.errors:
            for error in self.errors.values():
                message_list.extend(error)
        return message_list


# 注册表单验证
class RegisterForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确的邮箱!")])
    email_captcha = StringField(validators=[Length(6, 6, message="请输入正确格式的邮箱验证码")])
    username = StringField(validators=[Length(5, 20, message="请输入5-20位的用户名")])
    password = StringField(validators=[Length(6, 20, message="请输入6-20位的密码")])
    repeat_password = StringField(validators=[EqualTo("password", message="两次密码不一致")])
    graph_captcha = StringField(validators=[Length(4, 4, message="请输入正确长度的图形验证码")])

    # 验证邮箱是否已经被注册过
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise ValidationError(message="邮箱已经被注册!")

    # 验证用户名是否已经被注册过
    def validata_username(self, field):
        username = field.data
        user = UserModel.query.filter_by(username=username).first()
        if user:
            raise ValidationError(message="用户名已经被注册过!")

    # 验证邮箱验证码是否存在
    def validate_email_captcha(self, field):
        email_captcha = field.data
        email = self.email.data
        cache_captcha = cache.get(email)
        if not cache_captcha or cache_captcha != email_captcha:
            raise ValidationError(message="邮箱验证码错误!")

    # 验证图形验证码是否正确
    def validate_graph_captcha(self, field):
        key = request.cookies.get("_graph_captcha_key")
        cache_captcha = cache.get(key)
        graph_captcha = field.data
        if not cache_captcha or cache_captcha.lower() != graph_captcha.lower():
            raise ValidationError(message="图形验证码错误!")


# 登录表单验证
class LoginForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确格式的邮箱")])
    password = StringField(validators=[Length(6, 20, message="请输入6-20位的密码")])
    remember_me = IntegerField()


# 自定义头像表单验证
class UploadAvatarForm(BaseForm):
    image = FileField(validators=[FileAllowed(['jpg', 'jpeg', 'png'], message="图片格式不符合要求，请传递jpg,jpeg,png"), FileSize(max_size=(1024*1024*5), message="图片最大不能超过5M")])


# 修改个人资料
class EditProfileForm(BaseForm):
    signature = StringField(validators=[Length(min=1, max=50, message="长度要在1-50之间！")])
