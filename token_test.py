# @Time: 2022/3/8 5:24 下午
# @Author: Bruce
# @Description: 用于测试jwt的登录

import requests

headers = {
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0NjczMjE4MiwianRpIjoiYzE4MjFjNDYtODE2MS00YjQxLTkyY2EtYmFmNDk0YmY1ZDM4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IlVhRXVhUmpSTUc0dnhYbzRzTlo4UDciLCJuYmYiOjE2NDY3MzIxODIsImV4cCI6MTY0NjczMzA4Mn0.cdwBs8FBqbdMLfOWV9M0XfQ6Nb5pojopb4tFXG4ufSE"
}

resp = requests.get("http://127.0.0.1:5000/cms", headers=headers)
print(resp.text)