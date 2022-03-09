# @Time: 2022/3/9 3:28 下午
# @Author: Bruce
# @Description:

from apps.front.forms import BaseForm
from wtforms.fields import FileField
from flask_wtf.file import FileAllowed, FileSize


class UploadBannerImageForm(BaseForm):
    image = FileField(validators=[FileAllowed(["jpg", "jpeg", "png"], message="图片格式不符合要求"),
                                  FileSize(1024*1024*10, message="图片大小不可以超过10M")])
