#!/usr/bin/python
# -*- coding: UTF-8 -*-

ICONDATA = ""
# 版本号
VERSION = 5
# 是否同步测试版
ProduceBate = 0
# 是否同步预发版
ProduceRC = 0

# 配置文件名
CONFFILE = "config.json"
CONFFILE_1024 = "config_1024.json"
CONFFILE_caishen = "config_caishen.json"
CONFFILE_EXT = "config_EXT.json"
CONFFILE_forest = "config_forest.json"
CONFFILE_goldshark = "config_goldshark.json"
CONFFILE_redBag = "config_redBag.json"
# 配置信息
Conf = {}
# 日志文件
LOGFILE = "Jointer.log"

# 运行标志
isRun = False
# 发布模式: [0: H5, 1:AS, 2:AGFlash, 3:KenoFlash]
PUBLISH_TYPE = 0
# 调试模式
DEBUG = False
# Web服务
httpd = None
