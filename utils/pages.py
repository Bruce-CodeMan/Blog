# @Time : 2022/3/12 11:15 
# @Author : Bruce
# @Description : 获取页数

from flask import current_app


def get_pages(page):
    per_page_count = current_app.config.get("PER_PAGE_COUNT")
    start = (page - 1) * per_page_count
    end = start + per_page_count
    return start, end

