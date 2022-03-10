# @Time: 2022/3/9 3:28 下午
# @Author: Bruce
# @Description: "后端的form表单"

from apps.front.forms import BaseForm
from wtforms.fields import FileField, StringField, IntegerField
from wtforms.validators import InputRequired
from flask_wtf.file import FileAllowed, FileSize


class UploadBannerImageForm(BaseForm):
    image = FileField(validators=[FileAllowed(["jpg", "jpeg", "png"], message="图片格式不符合要求"),
                                  FileSize(1024*1024*10, message="图片大小不可以超过10M")])


class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message="请输入轮播图的名称")])
    image_url = StringField(validators=[InputRequired(message="请输入传入图片的路径")])
    link_url = StringField(validators=[InputRequired(message="请传入图片的链接")])
    priority = IntegerField(validators=[InputRequired(message="请传入优先级")])


class EditBannerForm(AddBannerForm):
    id = IntegerField(validators=[InputRequired(message="请输入轮播图的id")])
