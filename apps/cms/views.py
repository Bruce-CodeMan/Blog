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
from models.border import BannerModel, PosterModel, CommentModel
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


# 上传轮播图照片
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


# 增加轮播图信息
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


# 获取轮播图列表
@cms.get("/banner/list")
def list_banner():
    banners = BannerModel.query.order_by(BannerModel.create_time.desc()).all()
    banner_dict = [banner.to_dict() for banner in banners]
    return restful.ok(data=banner_dict)


# 删除轮播图
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


# 编辑轮播图
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


# 帖子获取
@cms.get("/poster/list")
def list_poster():
    page = request.args.get("page", default=1, type=int)
    per_page_count = current_app.config.get("PER_PAGE_COUNT")
    start = (page - 1) * per_page_count
    end = start + per_page_count
    query_poster = PosterModel.query.order_by(PosterModel.create_time.desc())
    total_count = query_poster.count()
    posters = query_poster.slice(start, end)
    poster_list = [poster.to_dict() for poster in posters]
    return restful.ok(data={"total_count": total_count, "poster_list": poster_list, "page": page})


# 删除帖子
@cms.post("/poster/delete")
def delete_poster():
    poster_id = request.form.get("id")
    try:
        poster_model = PosterModel.query.get(poster_id)
    except Exception as e:
        return restful.params_error(message="帖子不存在")
    db.session.delete(poster_model)
    db.session.commit()
    return restful.ok()


# 评论展示
@cms.get("/comment/list")
def list_comment():
    page = request.args.get("page", default=1, type=int)
    per_page_count = current_app.config["PER_PAGE_COUNT"]
    start = (page - 1) * per_page_count
    end = start + per_page_count
    query_comment = CommentModel.query.order_by(CommentModel.create_time.desc())
    total_count = query_comment.count()
    comments = query_comment.slice(start, end)
    comment_list = [comment.to_dict() for comment in comments]
    return restful.ok(data={"total_count": total_count, "comment_list": comment_list, "page": page})


# 评论删除
@cms.post("/comment/delete")
def delete_comment():
    comment_id = request.form.get("id")
    try:
        comment_model = CommentModel.query.get(comment_id)
    except Exception as e:
        return restful.params_error(message="评论不存在")
    db.session.delete(comment_model)
    db.session.commit()
    return restful.ok()


# 获取用户列表
@cms.get("/user/list")
def list_user():
    page = request.args.get("page", default=1, type=int)
    per_page_count = current_app.config.get("PER_PAGE_COUNT")
    start = (page - 1) * per_page_count
    end = start + per_page_count
    query_user = UserModel.query.order_by(UserModel.join_time.desc())
    total_count = query_user.count()
    users = query_user.slice(start, end)
    user_list = [user.to_dict() for user in users]
    return restful.ok(data={
        "total_count": total_count,
        "user_list": user_list,
        "page": page
    })


# 用户激活或者拉黑
@cms.post("/user/active")
def active_user():
    is_active = request.form.get("is_active", type=int)
    user_id = request.form.get("id")
    user = UserModel.query.get(user_id)
    user.is_active = bool(is_active)
    db.session.commit()
    return restful.ok(data=user.to_dict())
