# @Time: 2022/3/8 5:18 下午
# @Author: Bruce
# @Description: CMS管理视图


from flask import Blueprint
from utils import restful
from flask_jwt_extended import jwt_required, get_jwt_identity

cms = Blueprint("cms", __name__, url_prefix="/cms")


@cms.get("/")
@jwt_required()
def index():
    identity = get_jwt_identity()
    print(identity)
    return restful.ok(message="success", data={"identity": identity})
