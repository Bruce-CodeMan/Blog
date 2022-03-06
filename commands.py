# @Time : 2022/3/6 23:16 
# @Author : Bruce

from models.border import BorderModel
from exts import db


def init_boards():
    board_names = ["Movie", "Technology", "Car"]
    for board_name in board_names:
        board = BorderModel(name=board_name)
        db.session.add(board)
    db.session.commit()
    print("版本添加成功")
