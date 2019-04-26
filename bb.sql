create schema bb collate utf8_general_ci;

create table box
(
	id int auto_increment
		primary key,
	boxid int null,
	userid int null,
	booknum int null comment '小说数量',
	picnum int null comment '图片数量',
	vodnum int null comment '小视频数量',
	filmnum int null comment '电影数量',
	collect int null comment '总收藏数',
	follow_times int null comment '关注人数',
	name varchar(255) null comment '盒子名',
	img varchar(255) null comment '封面',
	img_path int null,
	create_time timestamp default CURRENT_TIMESTAMP null,
	flag int default 0 null comment '小视频爬取状态 0待爬 1 正爬 2完成',
	flag_img int default 0 null comment '图片爬取状态 0待爬 1 正爬 2完成',
	flag_film int default 0 null comment '电影爬取状态',
	flag_store int default 0 null comment '小说爬取状态',
	constraint boxid
		unique (boxid)
)
comment '盒子' engine=InnoDB;

create table box_res
(
	id int auto_increment
		primary key,
	box_id int null,
	res_id int null
)
engine=InnoDB;

create table image
(
	id int auto_increment
		primary key,
	uuid int null,
	res_id int null,
	height int null,
	width int null,
	img varchar(255) null,
	path varchar(255) null,
	create_time timestamp default CURRENT_TIMESTAMP null
)
engine=InnoDB;

create table res
(
	id int auto_increment
		primary key,
	uuid int null comment '官方的资源ID',
	video varchar(255) null comment '视频路径',
	img varchar(255) null comment '封面路径',
	follow_times int null comment '关注次数',
	height int null,
	width int null,
	length int null,
	num int null comment '图片数量',
	boxid int(10) null comment '盒子ID',
	userid int null comment '用户ID',
	name varchar(255) null comment '盒子名',
	nickname varchar(255) null comment '用户名',
	type int null comment '1图片 2短视频  3小说  4电影',
	timestamp varchar(255) null,
	topnum int null comment '排序',
	video_path varchar(255) null comment '本地路径',
	img_path varchar(255) null,
	create_time timestamp default CURRENT_TIMESTAMP null,
	constraint uuid
		unique (uuid, type)
)
comment '资源' engine=InnoDB;

