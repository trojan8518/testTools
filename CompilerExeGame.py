#!/usr/bin/python
# -*- coding: UTF-8 -*-
from GitSync import *
import gl


def CompilerExeGame(gameID):
    # 1:1024 2:caishen 3:EXT 4 : forest 5:goladShark
    if gameID == 1:
         gl.Conf = LoadJSON(gl.CONFFILE_1024)
         Conf = gl.Conf
         Info("------------build- 1024---")
    elif gameID == 2:
        gl.Conf = LoadJSON(gl.CONFFILE_caishen)
        Conf = gl.Conf
        Info("------------build- caishen---")
    elif gameID == 3:
        gl.Conf = LoadJSON(gl.CONFFILE_EXT)
        Conf = gl.Conf
        Info("------------build- EXT---")
    elif gameID == 4:
        gl.Conf = LoadJSON(gl.CONFFILE_forest)
        Conf = gl.Conf
        Info("------------build- forest---")
    elif gameID == 5:
        gl.Conf = LoadJSON(gl.CONFFILE_goldshark)
        Conf = gl.Conf
        Info("------------build- goldshark---")



    SOURCE = Conf["SOURCE"]
    OUT = Conf["C_OUT"]
    PACKS = Conf["PACKS"]
    ResDepot = Conf["ResDepot"]
    RES_NAME = Conf["RES_NAME"]
    M_OUT = Conf["M_OUT"]
    infoFile = "FilesInfo.json"

    Info("Git 拉代码")
    # GitPull(SOURCE)

    Info("----build--begin -- 编译程序")
    Call("egret publish --version h5 --runtime html5 \"%s\"" % SOURCE)

    Info("-----merge resouce ----整合资源")
    PRODIR = "%s/bin-release/web/h5" % SOURCE.replace('\\', '/')
    filter = [infoFile]
    EmptyTree(OUT, filter)
    # 合图
    with open("%s/resource/%s.res.json" % (PRODIR, RES_NAME)) as jsonfile:
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
                item['gap'] = 2
                item['sort'] = 0
                item['res'] = []
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
        Call('"%s" -pack "%s/resource/%s.res.json" "%s/resource/ResDepotTmp.json" "%s/resource"' % (
        ResDepot, PRODIR, RES_NAME, PRODIR, PRODIR))
    Info("----moving file ----移动文件")
    prdirs = os.path.expanduser(PRODIR)
    for f in os.listdir(prdirs):
        if (not f.strip() in filter) and f.strip() != "resource":
            shutil.move(os.path.join(PRODIR, f), OUT)
    # jspName = "info.jsp"
    # extraDir = "activityimg"
    # if gl.PUBLISH_TYPE == 1:
    #	jspName = "game.jsp"
    #	extraDir = "logo"
    # shutil.copyfile("%s/%s" % (SOURCE, jspName), "%s/%s" % (OUT, jspName))
    # shutil.copyfile("%s/game.html" % SOURCE, "%s/game.html" % OUT)
    # shutil.copyfile("%s/config.js" % SOURCE, "%s/config.js" % OUT)
    # shutil.copytree("%s/%s" % (SOURCE, extraDir), "%s/%s" % (OUT, extraDir))
    shutil.copyfile("%s/resource/%s.thm.json" % (PRODIR, RES_NAME), "%s/resource/%s.thm.json" % (OUT, RES_NAME))
    # shutil.copytree("%s/resource/rules" % PRODIR, "%s/resource/rules" % OUT)

    Info("--remind--resouce-----修改资源信息")
    filesInfo = LoadJSON("%s/%s" % (OUT, infoFile))
    UpVer = False
    # GetTag()[0:3] != "Dev"

    resName = "/resource/%s.res.json" % RES_NAME
    resVer = GetFileVersion(OUT, resName, filesInfo, UpVer)
    resCrc = CrcFile(OUT + resName)

    thmName = "/resource/%s.thm.json" % RES_NAME
    thmVer = GetFileVersion(OUT, thmName, filesInfo, UpVer)
    thmCrc = CrcFile(OUT + thmName)

    coreFile = "main.min.js"
    coreVer = GetFileVersion(OUT, coreFile, filesInfo, UpVer)
    mainVer = "v%d.%d.%d.%d" % ((coreVer + resVer + thmVer) / 100, coreVer, resVer, thmVer)
    # with open("%s/%s" % (OUT, coreFile), "r+") as f:
    #	t = f.read()
    #	t = re.sub('VERSON_NAME="(.*?)"', 'VERSON_NAME="v%d.%d.%d.%d"' % ((coreVer+resVer+thmVer)/100, coreVer, resVer, thmVer), t)
    #	f.seek(0, 0)
    #	f.write(t)

    mainCrc = GetFileCRC32(OUT + "/" + coreFile)
    newCoreFile = "%s_%s%s" % (coreFile[:-7], mainCrc, coreFile[-3:])
    # Call('javascript-obfuscator "%s/%s" --output "%s/%s"' % (OUT, coreFile, OUT, newCoreFile))

    shutil.copytree("%s/resource" % OUT, "%s/resource_ext/%s" % (M_OUT, RES_NAME))

    # 库文件
    # filter = []
    # fileMaps = {}
    # CrcDir(OUT + "/libs", fileMaps, filter)
    # CrcDir(OUT + "/library", fileMaps, filter)

    gameFile = "%s/manifest.json" % M_OUT
    manifest = LoadJSON(gameFile)
    manifest["res_" + RES_NAME] = "_" + resCrc
    manifest["thm_" + RES_NAME] = "_" + thmCrc
    SaveJSON(gameFile, manifest, True)

    # with open(gameFile, "r+") as f:
    #	t = f.read()
    #	fileKeys = fileMaps.viewkeys()
    #	for key in fileKeys:
    #		t = re.sub(key, fileMaps[key], t)
    #	t = re.sub('"initial"', '"ver":"%s",\n\t"res":"_%s",\n\t"thm":"_%s",\n\t"initial"' % (mainVer, resCrc, thmCrc), t)
    #	t = re.sub('"%s"' % coreFile, '"config.js",\n\t\t"%s"' % newCoreFile, t)
    #	f.seek(0, 0)
    #	f.write(t)

    SaveJSON("%s/%s" % (OUT, infoFile), filesInfo, True)
    Info("---finish---操作完毕 [V%d.%d.%d.%d Main:%s RES:%s THM:%s]\n%s" % (
    (coreVer + resVer + thmVer) / 100, coreVer, resVer, thmVer, mainCrc, resCrc, thmCrc, '=' * 33))
# SaveJSON(gl.CONFFILE, Conf, True)
