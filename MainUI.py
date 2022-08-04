#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tkFileDialog
import signal
import base64
import thread

from Tkinter import *
from PublishH5 import *
from PublishFlash import *
from CompilerH5 import *
from HttpServer import *
import gl

def Publish():
	if gl.isRun:
		return
		
	gl.isRun = True
	if gl.PUBLISH_TYPE < 2:
		PublishH5()
	else:
		PublishFlash()
	Info("=" * 33)
	gl.isRun = False

# 点击发布
def clickPublish():
	Conf = gl.Conf
	if (not "SOURCE" in Conf) or (not os.path.isdir(Conf["SOURCE"])):
		Conf["SOURCE"] = tkFileDialog.askdirectory(title="请选择项目源:")
		if Conf["SOURCE"] == "": Warning("未指定源目录不能发布!")
	if (not "OUT" in Conf) or (not os.path.isdir(Conf["OUT"])):
		Conf["OUT"] = tkFileDialog.askdirectory(title="请选择发布目录:")
		if Conf["OUT"] == "":
			Warning("未指定目标目录不能发布!")
	if Conf["SOURCE"] == "" or Conf["OUT"] == "": return
	
	if not os.listdir(Conf["OUT"]) or not os.path.isdir("%s/.git" % Conf["OUT"]):
		user = getpass.getuser()
		Call('git config --global user.name %s' % user)
		Call('git config --global user.email %s@Iv66.net' % user)
		Call('git config --global core.autocrlf false')
		userinfo = GetFilter()
		gitUrl = re.sub('http://.*?', 'http://%s' % userinfo, Conf["GIT"])
		if Call('git clone "%s" "%s"' % (gitUrl, Conf["OUT"]), userinfo) == False:
			Warning("拉取目标库失败！")
			return
	if not os.path.isdir("%s/.git" % Conf["OUT"]):
		Warning("目标目录非有效Git目录！")
		return
	thread.start_new_thread(Publish, ())

# 点击编译
def clickCompiler():
	# CompilerH5(1)
	thread.start_new_thread(CompilerH5, (1,))
def clickWithOneKey():
	# CompilerH5(2)
	thread.start_new_thread(CompilerH5, (2,))

def runHttpServer(port):
	if gl.httpd is None:
		specDir = gl.Conf["C_OUT"]
		try:
			server_address = ('', port)
			gl.httpd = RootedHTTPServer(specDir, server_address, RootedHTTPRequestHandler)
		
			sa = gl.httpd.socket.getsockname()
			Info("Serving HTTP on %s:%s ..." % (sa[0], sa[1]))
			gl.httpd.serve_forever()
		except:
			gl.httpd = None
			runHttpServer(port + 1)

def clickHttpServer():
	if gl.httpd is None:
		thread.start_new_thread(runHttpServer, (8080,))
	
def CtrlC(signal_num, frame):
	Info("Ctrl-C 触发退出")
	if gl.httpd is not None:
		gl.httpd.shutdown()
	sys.exit(signal_num)
	
# 创建GUI
def CreateGUI():

	ui = Tk()
	ui.title("Jointer v%d" % gl.VERSION)
	ui.iconbitmap('')
	ui.geometry("456x153")
	ui.resizable(width=False, height=False)
	if gl.ICONDATA != "":
		iconstr = base64.b64decode(gl.ICONDATA)
		icon = PhotoImage(data=iconstr)
		ui.tk.call('wm', 'iconphoto', ui._w, icon)
		
	gl.ProduceBate = IntVar()
	gl.ProduceRC = IntVar()
	
	Checkbutton(ui, text="同步测试版", variable=gl.ProduceBate).grid(column=0, row=0, sticky=W)
	Checkbutton(ui, text="同步预发版", variable=gl.ProduceRC).grid(column=0, row=1, sticky=W)
	
	if len(sys.argv) > 1:
		gl.CONFFILE = sys.argv[1]
	# 配置信息
	gl.Conf = LoadJSON(gl.CONFFILE)
	Conf = gl.Conf
	if not Conf:
		Info("not found config.json")
		os._exit(-1)
		return
	
	title = ""
	if Conf["Model"] == "aggameh5":
		title = "AG旗舰 HTML5"
		gl.PUBLISH_TYPE = 0
	elif Conf["Model"] == "asgame":
		title = "AS 亚洲之星"
		gl.PUBLISH_TYPE = 1
	elif Conf["Model"] == "aggame":
		title = "AG旗舰 Flash"
		gl.PUBLISH_TYPE = 2
	elif Conf["Model"] == "kenogame":
		title = "AG彩票 Flash"
		gl.PUBLISH_TYPE = 3
	else:
		os._exit(-2)
	Button(ui, text="发布 (%s)" % title, width=23, command=clickPublish).grid(column=1, row=0, rowspan=1, sticky=W + E + N + S)
	if gl.PUBLISH_TYPE < 2:
		Button(ui, text="编译 (%s)" % title, width=23, command=clickCompiler).grid(column=1, row=1, rowspan=1, sticky=W + E + N + S)
	Button(ui, text="Web服务 (%s)" % title, width=23, command=clickHttpServer).grid(column=1, row=2, rowspan=1, sticky=W + E + N + S)
	Button(ui, text="一键打包 (%s)" % title, width=23, command=clickWithOneKey).grid(column=1, row=3, rowspan=1, sticky=W + E + N + S)
	Info("Jointer v%d \n%s 发布器\nAuthor: Akon Amender:  Fisker   User: %s" % (gl.VERSION, title, getpass.getuser()))
	Info("Target:%s\nCOut:%s\nOut:%s\n%s" % (Conf["SOURCE"], Conf["C_OUT"], Conf["OUT"], '=' * 58))

	ui.mainloop()

signal.signal(signal.SIGINT, CtrlC)
CreateGUI()
