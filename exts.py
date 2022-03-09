# @Time: 2022/3/3 10:48 上午
# @Author: Bruce
# @Description : 用到的第三方库


from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_caching import Cache
from flask_wtf import CSRFProtect
from flask_avatars import Avatars
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
mail = Mail()
cache = Cache()
csrf = CSRFProtect()
avatars = Avatars()
jwt = JWTManager()
cors = CORS()