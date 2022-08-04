#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 获取过滤账号信息
import getpass
from utils import *
import gl

def GetFilter():
	user = getpass.getuser()
	return "%s:%s123@" % (user, user.lower())


# 拉取资源
def GitPull(path):
	userinfo = GetFilter()
	if not Call('git -C "%s" pull' % path, userinfo): return -1
	return 1


# 资源入库
def GitCommit(path, tag):
	userinfo = GetFilter()
	Call('echo %s > %s/tag.txt' % (tag, path))
	if not Call('git -C "%s" add * ' % path, userinfo): return -1
	if not Call('git -C "%s" commit -a -m "Publish %s" ' % (path, tag), userinfo): return -2
	return 1


# 推送资源
def GitPush(path):
	userinfo = GetFilter()
	if not Call('git -C "%s" push ' % path, userinfo): return -3
	return 1

# 获取 Git Tag
def GetTag():
	tag = ""
	if gl.ProduceBate.get() == 1:
		tag = "Beta "
	if gl.ProduceRC.get() == 1:
		tag += "RC "
	if tag == "":
		user = getpass.getuser()
		if not user or user == "":
			user = "Default"
		tag = "Dev %s" % user
	return tag.rstrip()


# 获取文件版本号
def GetFileVersion(root, file, info, up):
	fmd5 = ""
	if root != "":
		fmd5 = GetFileMD5("%s/%s" % (root, file))
	if not info.has_key(file):
		info[file] = {"md5": fmd5, "ver": 1}
		return 1
	fver = info[file]["ver"]
	if info[file]["md5"] != fmd5:
		if up:
			fver += 1
		info[file] = {"md5": fmd5, "ver": fver}
	return fver


