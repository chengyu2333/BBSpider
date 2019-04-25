# Host: localhost  (Version: 5.5.53)
# Date: 2019-04-24 17:26:38
# Generator: MySQL-Front 5.3  (Build 4.234)

/*!40101 SET NAMES utf8 */;

#
# Structure for table "box"
#

DROP TABLE IF EXISTS `box`;
CREATE TABLE `box` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `boxid` int(11) DEFAULT NULL,
  `userid` int(11) DEFAULT NULL,
  `booknum` int(11) DEFAULT NULL COMMENT '小说数量',
  `picnum` int(11) DEFAULT NULL COMMENT '图片数量',
  `vodnum` int(11) DEFAULT NULL COMMENT '小视频数量',
  `filmnum` int(11) DEFAULT NULL COMMENT '电影数量',
  `collect` int(11) DEFAULT NULL COMMENT '总收藏数',
  `follow_times` int(11) DEFAULT NULL COMMENT '关注人数',
  `name` varchar(255) DEFAULT NULL COMMENT '盒子名',
  `img` varchar(255) DEFAULT NULL COMMENT '封面',
  `img_path` int(11) DEFAULT NULL,
  `flag` int(11) DEFAULT '0' COMMENT '爬取状态 0待爬 1 正爬 2完成',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `boxid` (`boxid`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8 COMMENT='盒子';

#
# Structure for table "box_res"
#

DROP TABLE IF EXISTS `box_res`;
CREATE TABLE `box_res` (
  `box_id` int(11) DEFAULT NULL,
  `res_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Structure for table "image"
#

DROP TABLE IF EXISTS `image`;
CREATE TABLE `image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` int(11) DEFAULT NULL,
  `res_id` int(11) DEFAULT NULL,
  `height` int(11) DEFAULT NULL,
  `width` int(11) DEFAULT NULL,
  `img` varchar(255) DEFAULT NULL,
  `path` varchar(255) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1705 DEFAULT CHARSET=utf8;

#
# Structure for table "res"
#

DROP TABLE IF EXISTS `res`;
CREATE TABLE `res` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` int(11) DEFAULT NULL COMMENT '官方的资源ID',
  `video` varchar(255) DEFAULT NULL COMMENT '视频路径',
  `img` varchar(255) DEFAULT NULL COMMENT '封面路径',
  `follow_times` int(11) DEFAULT NULL COMMENT '关注次数',
  `height` int(11) DEFAULT NULL,
  `width` int(11) DEFAULT NULL,
  `length` int(11) DEFAULT NULL,
  `num` int(11) DEFAULT NULL COMMENT '图片数量',
  `boxid` int(10) DEFAULT NULL COMMENT '盒子ID',
  `userid` int(11) DEFAULT NULL COMMENT '用户ID',
  `name` varchar(255) DEFAULT NULL COMMENT '盒子名',
  `nickname` varchar(255) DEFAULT NULL COMMENT '用户名',
  `type` int(11) DEFAULT NULL COMMENT '1图片 2短视频  3小说  4电影',
  `timestamp` varchar(255) DEFAULT NULL,
  `topnum` int(11) DEFAULT NULL COMMENT '排序',
  `video_path` varchar(255) DEFAULT NULL COMMENT '本地路径',
  `img_path` varchar(255) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`,`type`)
) ENGINE=InnoDB AUTO_INCREMENT=697 DEFAULT CHARSET=utf8 COMMENT='资源';
