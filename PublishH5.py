#!/usr/bin/python
# -*- coding: UTF-8 -*-

from GitSync import *
import gl

def PublishH5():
	Conf = gl.Conf
	SOURCE = Conf["C_OUT"]
	OUT = Conf["OUT"]
	Info("同步文件")
	code = GitPull(OUT)
	if code != 1:
		Warning("同步文件失败：%d" % code)
		return
	Info("整理文件")
	CopyTree(SOURCE, OUT, [])
	Info("推送文件")
		code = GitCommit(OUT,  ())
	if code == 1:
		code = GitPush(OUT)
	if code != 1:
		Warning("推送文件失败：%d" % code)
		return
	SaveJSON(gl.CONFFILE, Conf, True)
	Info("操作完毕\n%s" % ('=' * 33))
