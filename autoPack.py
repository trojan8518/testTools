#!/usr/bin/python
# -*- coding: UTF-8 -*-
from GitSync import *
from CompilerExeGame import *
import gl
import time

def CompilerH5(type,isNeed,version,branchName):
    print ("type = %ld" % type)
    print ("isNeed = %ld" % isNeed)
    print ("v" + version)
    print ("branch =" + branchName)
    # 配置文件
    if type == 4:
         gl.Conf = LoadJSON(gl.CONFFILE_redBag)
         Conf = gl.Conf
         Info("-------coming-----build- redBag---")
    else:
        gl.Conf = LoadJSON(gl.CONFFILE)
        Conf = gl.Conf
        Info("---------coming---build- hall---")

    if Conf["Model"] == "aggameh5":

        gl.PUBLISH_TYPE = 0
    elif Conf["Model"] == "asgame":

        gl.PUBLISH_TYPE = 1
    elif Conf["Model"] == "aggame":

        gl.PUBLISH_TYPE = 2
    elif Conf["Model"] == "kenogame":

        gl.PUBLISH_TYPE = 3
    else:
        os._exit(-2)

    SOURCE = Conf["SOURCE"]
    OUT = Conf["C_OUT"]
    PACKS = Conf["PACKS"]

    ResDepot = Conf["ResDepot"]
    infoFile = "FilesInfo.json"
    Info("Git pull 拉代码")
    # GitPull(SOURCE)
    Info("------------build----编译程序")
    Call("egret publish --version h5 \"%s\"" % SOURCE)

    # Info("----------delete resource --清空以前的包")
    PRODIR = "%s/bin-release/web/h5" % SOURCE.replace('\\', '/')
    # filter = [infoFile]
    # EmptyTree(OUT, filter)
    Info("----------merge pics --打包图集--")
    # 合图

    Info("%s/resource/default.res.json" % PRODIR)
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
        Call('"%s" -pack "%s/resource/default.res.json" "%s/resource/ResDepotTmp.json" "%s/resource"' % (
        ResDepot, PRODIR, PRODIR, PRODIR))
        Info("------------------moving file -----移动文件")
    prdirs = os.path.expanduser(PRODIR)
    for f in os.listdir(prdirs):
        if (not f.strip() in filter) and f.strip() != "resource":
            shutil.move(os.path.join(PRODIR, f), OUT)
            print("11---" + f)
    if "ResMvDir" in Conf:
        ResMvDir = Conf["ResMvDir"]
        for f in ResMvDir:
            shutil.move(os.path.join(PRODIR, f), OUT + "/" + f)
            print("22---" + f)
    # #copy源文件
    jspName = "info.jsp"
    extraDir = "activityimg"
    if gl.PUBLISH_TYPE == 1:
        jspName = "game.jsp"
        extraDir = "logo"
    if os.path.exists("%s/%s" % (SOURCE ,jspName)):
        shutil.copyfile("%s/%s" % (SOURCE, jspName), "%s/%s" % (OUT, jspName))
    if os.path.exists("%s/game.html" % SOURCE):
        shutil.copyfile("%s/game.html" % SOURCE, "%s/game.html" % OUT)
    if os.path.exists("%s/config.js" % SOURCE):
        shutil.copyfile("%s/config.js" % SOURCE, "%s/config.js" % OUT)
    if os.path.exists("%s/as_preload.js" % SOURCE):
        shutil.copyfile("%s/as_preload.js" % SOURCE, "%s/as_preload.js" % OUT)
    if os.path.exists("%s/%s" % (SOURCE, extraDir)):
        pubpath = "C:/Users/Administrator/Desktop/asgame/PUB"
        if os.path.exists(pubpath):
            shutil.copytree("%s/%s" % (pubpath, extraDir), "%s/%s" % (OUT, extraDir))
        else:
            shutil.copytree("%s/%s" % (SOURCE, extraDir), "%s/%s" % (OUT, extraDir))
    if os.path.exists("%s/resource/default.thm.json" % PRODIR):
        shutil.copyfile("%s/resource/default.thm.json" % PRODIR, "%s/resource/default.thm.json" % OUT)
    my_files = "%s/resource/rules" % OUT
    share_rules="%s/resource/share/rules" % OUT
    #rules 不能加密
    if os.path.exists(share_rules):
        shutil.rmtree(share_rules);
    if os.path.exists("%s/resource/share/rules" % PRODIR):
        shutil.copytree("%s/resource/share/rules" % PRODIR, "%s/resource/share/rules" % OUT)

    if os.path.exists(my_files):
        print ("have rules foler ,Need to delete")
        shutil.rmtree(my_files)
        # print ("no rules foler ,Need to copy it ...")
    if os.path.exists("%s/resource/rules" % PRODIR):
        shutil.copytree("%s/resource/rules" % PRODIR, "%s/resource/rules" % OUT)
    # 拷贝buyGirl文件
    # if os.path.exists("%s/buyGirl" % SOURCE):
    #     shutil.copytree("%s/buyGirl" % SOURCE, "%s/buyGirl" % OUT)
    if os.path.exists("%s/buyGirl2" % SOURCE):
        shutil.copytree("%s/buyGirl2" % SOURCE, "%s/buyGirl2" % OUT)
    if os.path.exists("%s/htmls" % SOURCE):
        pubpath = "C:/Users/Administrator/Desktop/asgame/PUB/htmls"
        if os.path.exists(pubpath):
            # 从三方库拷贝最新的
            shutil.copytree("%s/htmls" % pubpath, "%s/htmls" % OUT)
        else:
            shutil.copytree("%s/htmls" % SOURCE, "%s/htmls" % OUT)

    versionFile = "%s/version.json" % SOURCE
    if os.path.exists(versionFile):
        shutil.copyfile("%s/version.json" % SOURCE, "%s/version.json" % OUT)
        jsonFile = "%s/version.json" % OUT;
        dict = LoadJSON(jsonFile)
        dict["version"] = "v" + version ;
        SaveJSON(jsonFile,dict,True);

    Info("remind resouce info ---修改资源信息")
    filesInfo = LoadJSON("%s/%s" % (OUT, infoFile))
    UpVer = False
    # GetTag()[0:3] != "Dev"
    # print("tag------%s" % GetTag())
    resName = "/resource/default.res.json"
    resVer = GetFileVersion(OUT, resName, filesInfo, UpVer)
    resCrc = CrcFile(OUT + resName)

    thmName = "/resource/default.thm.json"
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
    Call('javascript-obfuscator "%s/%s" --output "%s/%s"' % (OUT, coreFile, OUT, newCoreFile))
    print("newMianJSName---- %s" % newCoreFile)
    obfuscatorStr = 'javascript-obfuscator "%s/%s" --output "%s/%s"' % (OUT, coreFile, OUT, newCoreFile)
    print ("obfuscatorStr ------------%s" % obfuscatorStr)
    # 库文件
    filter = []
    fileMaps = {}
    if os.path.exists(OUT + "/libs"):
        CrcDir(OUT + "/libs", fileMaps, filter)
    if os.path.exists(OUT + "/library"):
        CrcDir(OUT + "/library", fileMaps, filter)
    if gl.PUBLISH_TYPE == 1:
        if os.path.exists(OUT + "/libs-ext"):
             CrcDir(OUT + "/libs-ext", fileMaps, filter)
    gameFile = "%s/manifest.json" % OUT
    with open(gameFile, "r+") as f:
        t = f.read()
        fileKeys = fileMaps.viewkeys()
        for key in fileKeys:
            t = re.sub(key, fileMaps[key], t)
        t = re.sub('"initial"', '"ver":"%s",\n\t"res":"_%s",\n\t"thm":"_%s",\n\t"initial"' % (mainVer, resCrc, thmCrc),
                   t)
        t = re.sub('"%s"' % coreFile, '"config.js",\n\t\t"%s"' % newCoreFile, t)
        f.seek(0, 0)
        f.write(t)

    SaveJSON("%s/%s" % (OUT, infoFile), filesInfo, True)

    Info("finish --- 操作完毕 [V%d.%d.%d.%d Main:%s RES:%s THM:%s]\n%s" % (
    (coreVer + resVer + thmVer) / 100, coreVer, resVer, thmVer, mainCrc, resCrc, thmCrc, '=' * 33))

    #修改manifest.json文件
    jsonFile = "%s/manifest.json" % OUT ;
    if os.path.exists(jsonFile) and os.path.exists("%s/htmls" % OUT):
        jsonFile = "%s/manifest.json" % OUT;
        dict = LoadJSON(jsonFile);
        list = dict["initial"];
        gmesList = dict["game"];
        firstConfig = gmesList[0];
        if firstConfig == "config.js":
            gmesList.remove(firstConfig);
        dict["ver"] = "v"+version
        if any(list) :
            isHaveWpMin = False
            NewArr = [];
            for obj in list:
                if obj.find("wp.min") >=0:
                    isHaveWpMin = True
                if type == 2 :#大厅保留benGame/slotGame/goldshark/redBlack
                    if obj.find("benzGame") >=0 or obj.find("redblack")>=0  or obj.find("goldshark")>=0 or obj.find("slotGame")>=0 :
                        NewArr.append(obj);

            del list[:]  # 清空数组
            for obj in NewArr:
                list.append(obj);
            if os.path.exists("%s/htmls/js/asgame.min.js" % OUT):
                list.insert(0, "htmls/js/asgame.min.js");
            if isHaveWpMin and type == 2:
                list.insert(0, "htmls/js/agwp.min_v1.js");
            list.insert(0, "htmls/js/thr_all.min_v1.js");
            list.insert(0, "htmls/js/egret_all.min_v1.js");

            SaveJSON(jsonFile, dict, True)

    #保存config.json 配置文件
    if type == 4:
         SaveJSON(gl.CONFFILE_redBag, Conf, True)
    else:
        SaveJSON(gl.CONFFILE, Conf, True)
    #森林舞会单游戏打包
    if type == 1:
        CompilerExeGame(4)
    if type == 2:
        # CompilerExeGame(1)
        # CompilerExeGame(2)
        # CompilerExeGame(3)
        # CompilerExeGame(4)
        # CompilerExeGame(5)
        Info("---------All the games package Successed-------")
    #noede 压缩图片
    isNeedZipPic=isNeed
    if isNeedZipPic :
        print ("---do compressed--------------");
        val = os.system('cd C:/Users/Administrator/Desktop/imageminTest')
        print (val);
        if os.path.exists("C:/Users/Administrator/Desktop/out/resource/"):
            val1 = os.system(
            'node C:/Users/Administrator/Desktop/imageminTest/index.js C:/Users/Administrator/Desktop/out/resource/  C:/Users/Administrator/Desktop/out/resource/');
            print (val1)
        if os.path.exists("C:/Users/Administrator/Desktop/out/resource_ext/"):
            val2 = os.system(
                'node C:/Users/Administrator/Desktop/imageminTest/index.js C:/Users/Administrator/Desktop/out/resource_ext/  C:/Users/Administrator/Desktop/out/resource_ext/');
            print (val2)
    else:
        print ("---undo uncompressed--------------");


    # 打zip包
    path1 = shutil.make_archive("C:\Users\Administrator\Desktop\out", "zip", "C:\Users\Administrator\Desktop\out")
    print ("-ZIP Path--" + path1)
    zipPath = "C:\Users\Administrator\Desktop\h5_out"
    shutil.move(path1, zipPath)

    path2 = shutil.make_archive("C:\Users\Administarator\Desktop\out","zip","root_dir","base_dir")
    print("Path2 - Zip ")
    zipPath2 = "C:\Users\Administrator\Desktop\h5_out"
    shutil.move(path2,zipPath2)

    currentDate = time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime(time.time()))
    originFiel = 'C:\\Users\\Administrator\\Desktop\\h5_out'
    finalFile = currentDate + ".zip"
    print (finalFile)
    os.rename(originFiel + "\\" "out.zip", originFiel + "\\" + finalFile)
    if branchName == "":
        shutil.copyfile("C:/Users/Administrator/Desktop/h5_out/%s" % finalFile, "C:/jenkins/workspace/H5_game/asgame.zip")
    else:
        shutil.copyfile("C:/Users/Administrator/Desktop/h5_out/%s" % finalFile, "C:/jenkins/workspace/mutPackGames/%s.zip" % branchName)
    print ("22---" + currentDate)
    # GitCommit(zipPath, "outPut")
    # res = GitPush(zipPath)
    # print (res)
    Info("git push success file name:  %s " % finalFile)


def main(argv):
    print ("comming ----------")
    para=""
    para2=""
    para3="1.0.0.0"
    para4=""
    type=3
    isNeed=False
    for i in range(1, len(sys.argv)):
        if(i == 1) :
            para = sys.argv[i]
        elif(i == 2) :
            para2 = sys.argv[i]
        elif (i == 3):
            para3 = sys.argv[i]
        elif (i == 4):
            para4 = sys.argv[i]
    print (para + "---" + para2 + "---" + para3)

    if(para == "hall"):
        type=2
    elif para == "game_forest":
        type=1
    elif para == "game":
        type=3
    elif para == "game_redBag":
        type=4

    print (1)

    if (para2 == "un_need"):
        isNeed=False
    elif para2 == "need":
        isNeed=True
    CompilerH5(type,isNeed,para3,para4)
if __name__ == "__main__":
   main(sys.argv[1:])