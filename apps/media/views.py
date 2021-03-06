# @Time : 2022/3/6 20:22 
# @Author : Bruce
# @Description : 获取头像和发布帖子的照片


from flask import Blueprint, send_from_directory, current_app

media = Blueprint("media", __name__, url_prefix="/media")


@media.get("/avatar/<filename>")
def get_avatar(filename):
    return send_from_directory(current_app.config["AVATARS_SAVE_PATH"], filename)


@media.get("/posters/<filename>")
def get_poster(filename):
    return send_from_directory(current_app.config["POSTERS_SAVE_PATH"], filename)


@media.get("/banners/<filename>")
def get_banner(filename):
    return send_from_directory(current_app.config["BANNERS_SAVE_PATH"], filename)