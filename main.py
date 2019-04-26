# -*- coding: utf-8 -*-

import requests
import json
import log
import download

from database import DB
from fetch import Fetch

fetch = Fetch("213", "213")


# 我的关注
# fetch.fetch_mine_following_res(page=1, recursion=True)

# 爬取单个盒子
# fetch.fetch_res_by_box_id(793157, page=1, type=2, recursion=True)

# 爬取用户关注的盒子列表
# fetch.fetch_user_follow_box_list(user_id=213, page=1, recursion=True)

# 爬取已抓取的全部盒子
fetch.fetch_res_by_all_box(type=1, startPage=1)

# 用户盒子
# fetch.fetch_user_follow_box_list(user_id=2381483, page=1, recursion=True)

# 首页最热/最新盒子
# fetch.fetch_box_list(1, order="top", recursion=True)

# 首页最热/最新资源
# fetch.fetch_res(page=1, type=2, order="top", recursion=True)


# 下载文件
# download.download_image()
# download.download_video()