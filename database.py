from pymysql import cursors, connect
from pymysql.err import IntegrityError
import log

class DB:
    _db_cursor = None
    _conn = None

    def __init__(self):
        self._host = "localhost"
        self._port = 3306
        self._user = "root"
        self._password = "root"
        self._db_name = "bb"
        self.connect(self._db_name)
        self.duplicate_count = 0
        self.serial_duplicate_count = 0

    def connect(self, db_name):
        self._db_name = db_name if db_name else ""
        if self._db_name:
            self._conn = connect(self._host,
                                 self._user,
                                 self._password,
                                 db_name,
                                 self._port,
                                 cursorclass=cursors.DictCursor)
            self._conn.autocommit(True)
            self._db_cursor = self._conn.cursor()
        else:
            raise Exception("no database selected")

    def close(self):
        self._db_cursor.close()
        self._conn.close()

    def sql_format(self, d, k):
        if k in d:
            s = d[k]
            if 'str' in str(type(s)):
                return "'" + s + "'"
            else:
                return s
        else:
            return "Null"

    def add_box(self, boxid,userid,booknum,picnum,vodnum,filmnum,collect,follow_times,name,img):
        try:
            sql = "insert into box(boxid,userid,booknum,picnum,vodnum,filmnum,collect,follow_times,`name`,img) " \
                  "values(%d,%s,%d,%d,%d,%d,%d,%d,%s,%s) " \
                  % (boxid,userid,booknum,picnum,vodnum,filmnum,collect,follow_times,name,img)
            self._db_cursor.execute(sql)
        except Exception:
            raise

    def add_res(self,uuid,video,img,follow_times,height,width,length,num,boxid,userid,name,nickname,type,timestamp,topnum):
        try:
            sql = "insert into " \
                  "res(uuid,video,img,follow_times,height,width,length,num,boxid,userid,`name`,nickname,type,`timestamp`,topnum)" \
                  " values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) " \
                  % (uuid,video,img,follow_times,height,width,length,num,boxid,userid,name,nickname,type,timestamp,topnum)
            self._db_cursor.execute(sql)
        except Exception:
            raise

    def add_box_res(self,boxid, resid):
        try:
            sql = "insert into box_res(box_id, res_id) " \
                  "values(%d,%d) " \
                  % (boxid, resid)
            self._db_cursor.execute(sql)
        except Exception:
            raise

    def add_image(self, uuid, res_id, height, width, img):
        try:
            sql = "insert into image(uuid,res_id,height,width,img) value (%s,%s,%s,%s,%s)" % (uuid, res_id, height, width, img)
            self._db_cursor.execute(sql)
        except Exception:
            raise

    def get_unfetchbox_one(self):
        try:
            sql = "select * from box where flag=0 or flag=1 limit 1"
            self._db_cursor.execute(sql)
            return self._db_cursor.fetchone()
        except Exception:
            raise

    def set_box_flag(self, boxid, flag):
        try:
            sql = "update box set flag = %s where boxid = %s" % (flag, boxid)
            self._db_cursor.execute(sql)
            return self._db_cursor.fetchone()
        except Exception:
            raise

    def get_undownload_res_one(self):
        try:
            sql = "select * from res where video_path is null and video is not null limit 1"
            self._db_cursor.execute(sql)
            return self._db_cursor.fetchone()
        except Exception:
            raise

    def get_undownload_image_one(self):
        try:
            sql = "select * from image where path is null and img is not null limit 1"
            self._db_cursor.execute(sql)
            return self._db_cursor.fetchone()
        except Exception:
            raise

    def set_imgage_path(self, uuid, path):
        try:
            sql = "update image set path='%s' where uuid=%d " % (path, uuid)
            return self._db_cursor.execute(sql)
        except Exception:
            raise

    def set_res_video_path(self, uuid, path):
        try:
            sql = "update res set video_path='%s' where uuid=%d " % (path, uuid)
            return self._db_cursor.execute(sql)
        except Exception:
            raise

    def set_res_img_path(self, uuid, path):
        try:
            sql = "update res set img_path='%s' where uuid=%d " % (path, uuid)
            return self._db_cursor.execute(sql)
        except Exception:
            raise

    def set_image_path(self, uuid, path):
        try:
            sql = "update image set path='%s' where uuid=%d " % (path, uuid)
            return self._db_cursor.execute(sql)
        except Exception:
            raise
