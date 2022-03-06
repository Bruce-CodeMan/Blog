# @Time : 2022/3/6 20:22 
# @Author : Bruce
from flask import Blueprint, send_from_directory, current_app

media = Blueprint("media", __name__, url_prefix="/media")


@media.get("/avatar/<filename>")
def get_avatar(filename):
    return send_from_directory(current_app.config["AVATARS_SAVE_PATH"], filename)