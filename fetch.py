# -*- coding: utf-8 -*-

import requests
from urllib import request
import time
import os
import json
import log
from retry import retry
from database import DB
from pymysql.err import IntegrityError


class Fetch:

    def __init__(self, username=None, password=None):
        self.db = DB()
        self.__token = None
        self.username = username
        self.password = password
        self.duplicate_count = 0
        self.serial_duplicate_count = 0

    @retry(stop_max_attempt_number=5,
           stop_max_delay=1000,
           wait_exponential_multiplier=2000,
           wait_exponential_max=6000)
    def __fetch_api(self, url, need_token=False):
        try:
            if need_token:
                if self.__token is None:
                    raw = requests.post("http://172.80.57.10/auth/sign_in",
                                        json={"password": self.password, "username": self.username}).text
                    data = json.loads(raw)
                    if data['code'] == 200:
                        self.__token = "Basic " + data['data']['token']
                        log.log_info("get token：" + self.__token)
                    else:
                        raise Exception("Get token failed")
                self.__headers = {"Authorization": self.__token}
                raw = requests.get(url, headers=self.__headers).text
            else:
                raw = requests.get(url).text

            data = json.loads(raw)
            if data["code"] == 200:
                return data['data']
            else:
                log.log_error(url + "\n" + raw)
                raise Exception("api return error")
        except Exception as e:
            log.log_error(url + "\n" + raw)
            raise e

    @retry(stop_max_attempt_number=3,
           stop_max_delay=1000,
           wait_exponential_multiplier=2000,
           wait_exponential_max=6000)
    def download_file(self, url, filename):
        try:
            req = request.Request(url)
            data = request.urlopen(req).read()
            with open(filename, 'wb') as f:
                f.write(data)
                f.flush()
                f.close()
            log.log_info("download finished%s[%s]" % (filename, url))
            return True
        except Exception as e:
            log.log_error(url + str(e))
            raise e

    # 抓取首页盒子列表 order: top | new
    def fetch_box_list(self, page=1, order="top", recursion=False):
        if order == "top":
            url = "http://172.80.57.10/store/box/follow/top?page=%d&by=100" % page
        elif order == "new":
            url = "http://172.80.57.10/store/box/new?page=%d" % page
        data, pages = None, None
        try:
            data = self.__fetch_api(url)
            pages = data["pages"]
            log.log_info("fetch box %s,current page %d,total page %d" % (order, page, pages))
            for i in data["items"]:
                print(i)
                show = i['show']
                self.db.add_box(i['id'], 'NULL', i['bookmun'], i['picmun'], i['vodmun'], i['filmmun'], i['collect'],
                                i['follow_times'],
                                self.db.sql_format(i, 'name'), self.db.sql_format(show, 'img'))
            log.log_success("fetched box %s,current page %d,total page %d" % (order, page, pages))
            self.serial_duplicate_count = 0
        except IntegrityError:
            self.duplicate_count += 1
            self.serial_duplicate_count += 1
            if self.serial_duplicate_count % 10 == 1:
                log.log_info("serial duplicate %d times，total duplicate %d times" % (self.serial_duplicate_count, self.duplicate_count))
            self.fetch_box_list(page, order, True)
        except Exception as e:
            log.log_error(str(e))
            self.fetch_box_list(page, order, True)
        if recursion:
            if pages == page:
                return
            else:
                self.fetch_box_list(page + 1, order, True)

    # 递归爬取首页资源列表
    # order: top  new
    # type : type 1图片 2短视频  3小说  4电影
    def fetch_res(self, page=1, type=2, order="top", recursion=False):
        if order == "top":
            url = "http://172.80.57.10/api/v1.%d/top?page=%d&by=100" % (type,page)
        elif order == "new":
            url = "http://172.80.57.10//api/v1.%d/?page=%d" % (type,page)
        data, pages = None, None
        try:
            data = self.__fetch_api(url)
            pages = data["pages"]
            log.log_info("fetch type:%d,order:%s,current page %d, total page %d" % (type, order, page, pages))
            for i in data["items"]:
                self.__get_res(type, i['id'])
            log.log_success("fetched type:%d,order:%s,current page %d, total page %d" % (type, order, page, pages))
        except Exception as e:
            log.log_error(str(e))
            self.fetch_res(page, type, order, True)
        if recursion:
            if pages == page:
                return
            else:
                self.fetch_res(page + 1, type, order, True)

    # 递归爬取某个用户关注的盒子列表
    def fetch_user_follow_box_list(self, user_id, page=1, recursion=False):
        url = "http://172.80.57.10/store/user/followed/%s?page=%d&t=2" % (user_id, page)
        data, pages = None, None
        try:
            data = self.__fetch_api(url)
            pages = data["pages"]
            if pages == 0:
                log.log_success("user %s box is empty" % user_id)
                return
            log.log_info("fetch user %s box, current page %d, total page %d" % (user_id, page, pages))
            for i in data["items"]:
                print(i)
                show = i['show']
                self.db.add_box(i['id'], user_id, i['bookmun'], i['picmun'], i['vodmun'], i['filmmun'], i['collect'],
                                i['follow_times'], self.db.sql_format(i, 'name'), self.db.sql_format(show, 'img'))
            log.log_success("fetch user %s box, current page %d, total page %d" % (user_id, page, pages))
        except Exception as e:
            log.log_error(str(e))
            time.sleep(1)
            self.fetch_user_follow_box_list(user_id, page, True)
        if recursion:
            if pages == page:
                return
            else:
                self.fetch_user_follow_box_list(user_id, page + 1, True)

    # 递归爬取我的关注列表
    def fetch_mine_following_res(self, page=1, recursion=False):
        data, pages = None, None
        url = "http://172.80.57.10/api/v1.0/user/following?page=%d" % page
        try:
            data = self.__fetch_api(url, need_token=True, )
            pages = data["pages"]
            if pages == 0:
                log.log_success("Mine follow is empty")
                return
            log.log_info("fetch mine follow res, current page %d, total page %d" % (page, pages))
            for i in data["items"]:
                self.__get_res(i['t'], i['id'])
            log.log_success("fetched mine follow res, current page %d, total page %d" % (page, pages))
        except Exception as e:
            log.log_error(str(e))
            time.sleep(1)
            self.fetch_mine_following_res(page, True)
        if recursion:
            if pages == page:
                return
            else:
                self.fetch_mine_following_res(page + 1, True)

    # 递归爬取盒子内容 type 1图片 2短视频  3小说  4电影
    def fetch_res_by_box_id(self, boxid, page=1, type=2, recursion=False):
        data, pages = None, None
        url = "http://172.80.57.10/store/box/%d?page=%d&t=%d" % (boxid, page, type)
        try:
            data = self.__fetch_api(url)
            pages = data["pages"]
            if pages == 0:
                log.log_success("type %d box %s is empty"%(boxid, type))
                return
            log.log_info("fetch box %s, current page %d, total page %d" % (boxid, page, pages))
            for i in data["items"]:
                self.__get_res(type, i['id'])
                self.db.add_box_res(boxid, i['id'])
            log.log_success("fetched box %s, current page %d, total page %d" % (boxid, page, pages))
        except Exception as e:
            log.log_error(str(e))
            time.sleep(1)
            self.fetch_res_by_box_id(boxid, page,type, True)
        if recursion:
            if pages == page:
                return
            else:
                self.fetch_res_by_box_id(boxid, page + 1, type, True)

    # 爬取全部盒子 type : 1 图片 2小视频 3小说  4电影
    def fetch_res_by_all_box(self, type, startPage=1):
        count = 0
        while True:
            res = self.db.get_unfetchbox_one(type)
            print(res)
            if res:
                self.db.set_box_flag(res['boxid'], 1, type)
                self.fetch_res_by_box_id(res['boxid'], startPage, type, True)
                count += 1
                self.db.set_box_flag(res['boxid'], 2, type)
            else:
                log.log_success("all box fetched,total:" + str(count))
                break

    # 爬取资源并入库
    # TODO 小说和电影
    def __get_res(self, type, uuid):
        try:
            data = self.__fetch_api("http://172.80.57.10/api/v1.%d/show/%d" % (type, uuid))
            if type == 1:
                type_str = "photo"
            elif type == 2:
                type_str = "video"
            else:
                type_str = "video"
            res = data[type_str]
            collect = res['collect']
            num = self.db.sql_format(res, "num")
            topnum = self.db.sql_format(res, "topnum")
            video = self.db.sql_format(res, "video")
            length = self.db.sql_format(res, "length")
            img = self.db.sql_format(res, "img")
            timestamp = self.db.sql_format(res, "timestamp")
            name = self.db.sql_format(collect, "name")
            nickname = self.db.sql_format(collect, "nickname")
            self.db.add_res(res["id"], video, img, res['follow_times'], res['height'], res['width'], length,
                            num, collect['id'], collect['userid'], name, nickname, type, timestamp,
                            topnum)
            self.db.add_box_res(collect['id'], res['id'])
            log.log_info("fetched %s[%s], name:%s" % (type_str, uuid, ""))
            if type == 1:
                images = data['image']
                for image in images:
                    self.db.add_image(image['id'], res['id'], image['height'], image['width'], self.db.sql_format(image, "img"))
            self.serial_duplicate_count = 0
        except IntegrityError:
            self.duplicate_count += 1
            self.serial_duplicate_count += 1
            if self.serial_duplicate_count % 10 == 1:
                log.log_info("serial duplicate %d times，total duplicate %d times" % (self.serial_duplicate_count, self.duplicate_count))
        except Exception:
            raise
