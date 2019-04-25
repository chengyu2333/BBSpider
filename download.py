from database import DB
from fetch import Fetch
import log

db = DB()
fetch = Fetch()

apiserver = {
    "type1" : "http://172.80.57.10",
    "type2" : "http://app.sohutvt.com",
    "type3" : "https://beautybox9.com",
    "type4" : "https://beautybox3.com",
    "type5" : "https://beautybox1.com",
    "type6" : "http://69.87.192.74:32119"
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
            log.log_info("下载视频[%s]%s" % (res['uuid'], video_url))
            if fetch.download_file(video_url, video_path + video_name):
                db.set_res_video_path(res['uuid'], video_name)

            img_type = res['img'][0:5]
            img_url = apiserver[img_type] + res['img'][5:]
            img_name = res['img'].split("/")[-1]
            log.log_info("下载封面[%s]%s" % (res['uuid'], video_url))
            if fetch.download_file(video_url, cover_path + img_name):
                db.set_res_img_path(res['uuid'], img_name)
            count += 1
        else:
            log.log_success("全部视频下载完毕，总计：" + count)
            break


def download_image():
    count = 0
    while True:
        res = db.get_undownload_image_one()
        if res:
            image_type = res['img'][0:5]
            image_url = apiserver[image_type] + res['img'][5:]
            image_name = res['img'].split("/")[-1]
            log.log_info("下载图片[%s]%s" % (res['uuid'], image_url))
            if fetch.download_file(image_url, image_path + image_name):
                db.set_image_path(res['uuid'], image_name)
            count += 1
        else:
            log.log_success("全部图片下载完毕，总计：" + count)
            break
