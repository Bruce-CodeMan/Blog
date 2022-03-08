# @Time : 2022/3/6 23:16 
# @Author : Bruce
# @Description : 自定义命令行


import random
from models.border import BorderModel, PosterModel
from models.auth import UserModel
from exts import db


def init_boards():
    board_names = ["Movie", "Technology", "Car"]
    for board_name in board_names:
        board = BorderModel(name=board_name)
        db.session.add(board)
    db.session.commit()
    print("版本添加成功")


def create_test_posters():
    boards = list(BorderModel.query.all())
    for i in range(99):
        title = "title_%d" % i
        content = "content_%d" % i
        author = UserModel.query.first()
        index = random.randint(0, len(boards) - 1)
        board = boards[index]
        poster_model = PosterModel(title=title, content=content, author=author, border=board)
        print("已经成功创建:", title)
        db.session.add(poster_model)
    db.session.commit()
    print("帖子添加成功")
