# -*- coding: utf-8 -*-

from database import DB
from fetch import Fetch
import log

db = DB()
fetch = Fetch()

apiserver = {
    "type1": "http://172.80.57.10",
    "type2": "http://app.sohutvt.com",
    "type3": "https://beautybox9.com",
    "type4": "https://beautybox3.com",
    "type5": "https://beautybox1.com",
    "type6": "http://69.87.192.74:32119"
}
video_path = "video/"
cover_path = "cover/"
image_path = "image/"


def download_video():
    count = 0
    while True:
        res = db.get_undownload_res_one()
        if res:
            video_type = res['video'][0:5]
            video_url = apiserver[video_type] + res['video'][5:]
            video_name = res['video'].split("/")[-1]
            log.log_info("download video [%s]%s" % (res['uuid'], video_url))
            if fetch.download_file(video_url, video_path + video_name):
                db.set_res_video_path(res['uuid'], video_name)

            img_type = res['img'][0:5]
            img_url = apiserver[img_type] + res['img'][5:]
            img_name = res['img'].split("/")[-1]
            log.log_info("download cover [%s]%s" % (res['uuid'], video_url))
            if fetch.download_file(img_url, video_path + video_name + ".jpg"):
                db.set_res_img_path(res['uuid'], video_name + ".jpg")
            count += 1
        else:
            log.log_success("download finished, count：" + count)
            break


def download_image():
    count = 0
    while True:
        res = db.get_undownload_image_one()
        if res:
            image_type = res['img'][0:5]
            image_url = apiserver[image_type] + res['img'][5:]
            image_name = res['img'].split("/")[-1]
            log.log_info("down image[%s]%s" % (res['uuid'], image_url))
            if fetch.download_file(image_url, image_path + image_name):
                db.set_image_path(res['uuid'], image_name)
            count += 1
        else:
            log.log_success("download finished, count:" + count)
            break


def download_box_cover():
    count = 0
    while True:
        res = db.get_undownload_box_image_one()
        if res:
            image_type = res['img'][0:5]
            image_url = apiserver[image_type] + res['img'][5:]
            image_name = res['img'].split("/")[-1]
            log.log_info("download box cover[%s]%s" % (res['boxid'], image_url))
            if fetch.download_file(image_url, cover_path + image_name):
                db.set_box_image_path(res['boxid'], image_name)
            count += 1
        else:
            log.log_success("download box cover finished,total：" + str(count))
            break

# download_box_cover()

# download_image()

# download_video()