# @Time: 2022/3/8 5:18 下午
# @Author: Bruce
# @Description: CMS管理视图

import os
import time
from hashlib import md5
from .forms import UploadBannerImageForm, AddBannerForm, EditBannerForm
from flask import Blueprint, request, g, current_app
from utils import restful
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.auth import UserModel
from models.border import BannerModel
from exts import db

cms = Blueprint("cms", __name__, url_prefix="/cms")


# 获取用户的token
@cms.before_request
@jwt_required()
def cms_before_request():
    if request.method == "OPTIONS":
        return
    identity = get_jwt_identity()
    user = UserModel.query.filter_by(id=identity).first()
    if user:
        setattr(g, "user", user)


@cms.get("/")
@jwt_required()
def index():
    identity = get_jwt_identity()
    print(identity)
    return restful.ok(message="success", data={"identity": identity})


# 后台上传轮播图的接口
@cms.post("/banner/image/upload")
def upload_banner_image():
    form = UploadBannerImageForm(request.files)
    if form.validate():
        image = form.image.data
        filename = image.filename
        _, ext = os.path.splitext(filename)
        filename = md5((g.user.email+str(time.time())).encode("utf-8")).hexdigest() + ext
        image_path = os.path.join(current_app.config["BANNERS_SAVE_PATH"], filename)
        image.save(image_path)
        return restful.ok(data={"image_url": filename})
    else:
        return restful.params_error(message=form.messages[0])


@cms.post("/banner/add")
def add_banner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner_model = BannerModel(name=name, image_url=image_url, link_url=link_url, priority=priority)
        db.session.add(banner_model)
        db.session.commit()
        print(banner_model.to_dict())
        return restful.ok(data=banner_model.to_dict())
    else:
        return restful.params_error(form.messages[0])


@cms.get("/banner/list")
def list_banner():
    banners = BannerModel.query.order_by(BannerModel.create_time.desc()).all()
    banner_dict = [banner.to_dict() for banner in banners]
    return restful.ok(data=banner_dict)


@cms.post("/banner/delete")
def delete_banner():
    banner_id = request.form.get("id")
    if not banner_id:
        return restful.params_error(message="请传入要删除的ID")
    try:
        banner_model = BannerModel.query.get(banner_id)
    except:
        return restful.params_error(message="轮播图不存在")
    db.session.delete(banner_model)
    db.session.commit()
    return restful.ok()


@cms.post("/banner/edit")
def edit_banner():
    form = EditBannerForm(request.form)
    if form.validate():
        banner_id = form.id.data
        try:
            banner_model = BannerModel.query.get(banner_id)
        except:
            return restful.params_error(message="轮播图不存在")
        # 表单获取数据
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data

        # 数据的赋值
        banner_model.name = name
        banner_model.image_url = image_url
        banner_model.link_url = link_url
        banner_model.priority = priority

        db.session.commit()
        return restful.ok(banner_model.to_dict())
    else:
        return restful.params_error(message=form.messages[0])
