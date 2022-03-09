# @Time: 2022/3/8 5:24 下午
# @Author: Bruce
# @Description: 用于测试jwt的登录

import requests

headers = {
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0NjczNDg0MSwianRpIjoiZmJkZWU3MDAtOGM5OC00MzA3LTgwMDktYWY3MjcxYTNhNGZhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IlVhRXVhUmpSTUc0dnhYbzRzTlo4UDciLCJuYmYiOjE2NDY3MzQ4NDEsImV4cCI6MTY0NjczNTc0MX0.ovyasqNR8SnT9x2uBIDzP1UXM_oCZtMtTfjNafObPjkg"
}

resp = requests.get("http://127.0.0.1:5000/cms", headers=headers)
print(resp.text)