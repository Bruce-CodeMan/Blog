# @Time: 2022/3/8 5:18 下午
# @Author: Bruce
# @Description: CMS管理视图

import os
import time
from hashlib import md5
from .forms import UploadBannerImageForm
from flask import Blueprint, request, g, current_app
from utils import restful
from flask_jwt_extended import jwt_required, get_jwt_identity

cms = Blueprint("cms", __name__, url_prefix="/cms")


@cms.get("/")
@jwt_required()
def index():
    identity = get_jwt_identity()
    print(identity)
    return restful.ok(message="success", data={"identity": identity})


# 后台上传轮播图的接口
@cms.post("/banner/image/upload")
@jwt_required()
def upload_banner_image():
    form = UploadBannerImageForm(request.files)
    if form.validate():
        image = form.image.data
        filename = image.filename
        _, ext = os.path.splitext(filename)
        filename = md5((g.user.email+str(time.time())).encode("utf-8")).hexdigest() + ext
        image_path = os.path.join(current_app.config["BANNERS_SAVE_PATH"], filename)
        image.save(image_path)
        return restful.ok({"image_url": filename})
    else:
        return restful.params_error(message=form.messages[0])
