#!/usr/bin/python
# -*- coding: UTF-8 -*-
from GitSync import *
from CompilerExeGame import  *
import gl

def CompilerH5(type):
	print ("type = %ld" % type)
	#配置文件
	# gl.Conf = LoadJSON(gl.CONFFILE)
	Conf = gl.Conf
	# if Conf["Model"] == "aggameh5":
	# 	gl.PUBLISH_TYPE = 0
	# elif Conf["Model"] == "asgame":
	# 	gl.PUBLISH_TYPE = 1
	# elif Conf["Model"] == "aggame":
	# 	gl.PUBLISH_TYPE = 2
	# elif Conf["Model"] == "kenogame":
	# 	gl.PUBLISH_TYPE = 3
	# else:
	# 	os._exit(-2)

	SOURCE = Conf["SOURCE"]
	OUT = Conf["C_OUT"]
	PACKS = Conf["PACKS"]
	ResDepot = Conf["ResDepot"]
	infoFile = "FilesInfo.json"
	
	Info("------------build----编译程序")
	Call("egret publish --version h5 --runtime html5 \"%s\"" % SOURCE)

	Info("----------delete resource --清空以前的包")
	PRODIR = "%s/bin-release/web/h5" % SOURCE.replace('\\', '/')
	filter = [infoFile]
	EmptyTree(OUT, filter)
	Info("----------merge pics --打包图集--")
	# 合图
	with open("%s/resource/default.res.json" % PRODIR) as jsonfile:
		resJson = json.load(jsonfile)
		resDepot = {}
		resDepot['addCrc'] = True
		resDepot['cleanPublishPath'] = False
		resDepot['publishCopyAll'] = False
		resDepot['publishPath'] = "%s/resource" % OUT
		resDepot['sourcePath'] = "%s/resource" % PRODIR
		resDepot['packGroups'] = []
		resDepot['unPackGroup'] = []
		for group in resJson['groups']:
			if group['name'] in PACKS:
				item = {}
				item['name'] = group['name']
				item['gap']  = 2
				item['sort'] = 0
				item['res']  = []
				files = group['keys'].split(',')
				for file in files:
					pf = file.rfind('_')
					if pf > 0:
						if file[pf:] != "_png":
							continue
						else:
							if ("%s_json" % file[:pf]) in files or ("%s_fnt" % file[:pf]) in files:
								resDepot['unPackGroup'].append({'compress': False, 'key': file})
								continue
					item['res'].append({'compress': False, 'key': file})
				resDepot["packGroups"].append(item)
		SaveJSON("%s/resource/ResDepotTmp.json" % PRODIR, resDepot, True)
		Call('"%s" -pack "%s/resource/default.res.json" "%s/resource/ResDepotTmp.json" "%s/resource"' % (ResDepot, PRODIR, PRODIR, PRODIR))
	Info("------------------moving file -----移动文件")
	prdirs = os.path.expanduser(PRODIR)
	for f in os.listdir(prdirs):
		if (not f.strip() in filter) and f.strip() != "resource":
			shutil.move(os.path.join(PRODIR, f), OUT)
			print("11"+f)
	if "ResMvDir" in Conf:
		ResMvDir = Conf["ResMvDir"]
		for f in ResMvDir:
			shutil.move(os.path.join(PRODIR, f), OUT + "/" + f)
	# #copy源文件
	jspName = "info.jsp"
	extraDir = "activityimg"
	if gl.PUBLISH_TYPE == 1:
		jspName = "game.jsp"
		extraDir = "logo"
	shutil.copyfile("%s/%s" % (SOURCE, jspName), "%s/%s" % (OUT, jspName))
	shutil.copyfile("%s/game.html" % SOURCE, "%s/game.html" % OUT)
	shutil.copyfile("%s/config.js" % SOURCE, "%s/config.js" % OUT)
	shutil.copytree("%s/%s" % (SOURCE, extraDir), "%s/%s" % (OUT, extraDir))
	shutil.copyfile("%s/resource/default.thm.json" % PRODIR, "%s/resource/default.thm.json" % OUT)
	shutil.copytree("%s/resource/rules" % PRODIR, "%s/resource/rules" % OUT)
	#拷贝buyGirl文件
	shutil.copytree("%s/buyGirl" % SOURCE, "%s/buyGirl" % OUT)
	shutil.copytree("%s/buyGirl2" % SOURCE, "%s/buyGirl2" % OUT)

	Info("remind resouce info ---修改资源信息")
	filesInfo = LoadJSON("%s/%s" % (OUT, infoFile))
	UpVer = GetTag()[0:3] != "Dev"
	print("tag------%s" % GetTag() )
	resName = "/resource/default.res.json"
	resVer = GetFileVersion(OUT, resName, filesInfo, UpVer)
	resCrc = CrcFile(OUT + resName)

	thmName = "/resource/default.thm.json"
	thmVer = GetFileVersion(OUT, thmName, filesInfo, UpVer)
	thmCrc = CrcFile(OUT + thmName)

	coreFile = "main.min.js"
	coreVer = GetFileVersion(OUT, coreFile, filesInfo, UpVer)
	mainVer = "v%d.%d.%d.%d" % ((coreVer+resVer+thmVer)/100, coreVer, resVer, thmVer)
	#with open("%s/%s" % (OUT, coreFile), "r+") as f:
	#	t = f.read()
	#	t = re.sub('VERSON_NAME="(.*?)"', 'VERSON_NAME="v%d.%d.%d.%d"' % ((coreVer+resVer+thmVer)/100, coreVer, resVer, thmVer), t)
	#	f.seek(0, 0)
	#	f.write(t)

	mainCrc = GetFileCRC32(OUT + "/" + coreFile)
	newCoreFile = "%s_%s%s" % (coreFile[:-7], mainCrc, coreFile[-3:])
	print("newMianJSName---- %s" % newCoreFile)
	Call('javascript-obfuscator "%s/%s" --output "%s/%s"' % (OUT, coreFile, OUT, newCoreFile))
	obfuscatorStr = 'javascript-obfuscator "%s/%s" --output "%s/%s"' % (OUT, coreFile, OUT, newCoreFile)
	print ("obfuscatorStr ------------%s" % obfuscatorStr)
	# 库文件
	filter = []
	fileMaps = {}
	CrcDir(OUT + "/libs", fileMaps, filter)
	CrcDir(OUT + "/library", fileMaps, filter)
	if gl.PUBLISH_TYPE == 1:
		CrcDir(OUT + "/libs-ext", fileMaps, filter)

	gameFile = "%s/manifest.json" % OUT
	with open(gameFile, "r+") as f:
		t = f.read()
		fileKeys = fileMaps.viewkeys()
		for key in fileKeys:
			t = re.sub(key, fileMaps[key], t)
		t = re.sub('"initial"', '"ver":"%s",\n\t"res":"_%s",\n\t"thm":"_%s",\n\t"initial"' % (mainVer, resCrc, thmCrc), t)
		t = re.sub('"%s"' % coreFile, '"config.js",\n\t\t"%s"' % newCoreFile, t)
		f.seek(0, 0)
		f.write(t)

	SaveJSON("%s/%s" % (OUT, infoFile), filesInfo, True)
	Info("finish --- 操作完毕 [V%d.%d.%d.%d Main:%s RES:%s THM:%s]\n%s" % ((coreVer+resVer+thmVer)/100, coreVer, resVer, thmVer, mainCrc, resCrc, thmCrc, '=' * 33))
	SaveJSON(gl.CONFFILE, Conf, True)
	if type == 2:
		CompilerExeGame(1)
		CompilerExeGame(2)
		CompilerExeGame(3)
		CompilerExeGame(4)
		CompilerExeGame(5)
		Info("---------All the games package Successed-------")

		star_dir = r'%s' % OUT
		os.system("start explorer %s" % star_dir)
# CompilerH5(2)
