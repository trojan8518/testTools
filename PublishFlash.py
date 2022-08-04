#!/usr/bin/python
# -*- coding: UTF-8 -*-

from GitSync import *

def PublishFlash():
	Conf = gl.Conf
	SOURCE = Conf["SOURCE"]
	OUT = Conf["OUT"]
	Info("同步文件")
	code = GitPull(OUT)
	if code != 1:
		Warning("同步文件失败：%d" % code)
		return
	Info("整理文件")
	CopyTree(SOURCE, OUT, [])
	Info("推送文件")
	code = GitCommit(OUT, GetTag())
	if code == 1:
		code = GitPush(OUT)
	if code != 1:
		Warning("推送文件失败：%d" % code)
		return
	SaveJSON(gl.CONFFILE, Conf, True)
	Info("操作完毕")
