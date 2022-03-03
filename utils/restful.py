# @Time: 2022/3/3 6:18 下午
# @Author: Bruce

from flask import jsonify


class HttpCode(object):
    # 响应正常
    ok = 200
    # 没有登录错误
    unLoginError = 401
    # 没有权限错误
    permissionError = 403
    # 客户端参数错误
    paramsError = 400
    # 服务器错误
    serverError = 500


def _restful_result(code, message, data):
    return jsonify({"code": code, "message": message or "", "data": data or {}})


def ok(message=None, data=None):
    return _restful_result(code=HttpCode.ok, message=message, data=data)


def un_login_error(message="没有登录!"):
    return _restful_result(code=HttpCode.unLoginError, message=message, data=None)
