#!/usr/bin/python
# -*- coding: UTF-8 -*-
from GitSync import *
import gl
import  os
import time
from CompilerExeGame import *
import shutil


def CompilerH5(para):
    # ===========================测试混编命令=============================================================================
    # cmd = 'javascript-obfuscator "C:/Users/Administrator/Desktop/out/main.min.js" --output "C:/Users/Administrator/Desktop/out/main_8fffd424.js"'
    # Call(cmd)
    # ===========================打zip包=============================================================================
    # path1 = shutil.make_archive("C:\Users\Administrator\Desktop\out", "zip", "C:\Users\Administrator\Desktop\out")
    # print ("-ZIP Path--" + path1)
    # zipPath = "C:\Users\Administrator\Desktop\h5_out"
    # shutil.move(path1, zipPath)
    #
    # currentDate = time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime(time.time()))
    # originFiel = 'C:\\Users\\Administrator\\Desktop\\h5_out'
    # finalFile = currentDate + ".zip"
    # print (finalFile)
    # os.rename(originFiel + "\\" "out.zip", originFiel + "\\"+ finalFile)
    #
    # print ("22---"+ currentDate)
    # GitCommit(zipPath, "outPut")
    # res = GitPush(zipPath)
    # print (res)
    # Info("git push success %s " % finalFile)

    # 配置文件
    gl.Conf = LoadJSON(gl.CONFFILE)
    Conf = gl.Conf
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
    Info("Git pull 拉去代码")
    # GitPull(SOURCE)
    Info("---------build----------")
    # CompilerExeGame(5)
    PRODIR = "%s/bin-release/web/h5" % SOURCE.replace('\\', '/')
    my_files = "%s/resource/rules" % OUT
    # isHave = os.path.exists(my_files)
    # print (isHave)

    # 修改manifest.json文件
    type = 2;
    jsonFile = "%s/manifest.json" % OUT;
    if os.path.exists(jsonFile) and os.path.exists("%s/htmls" % OUT):
        jsonFile = "%s/manifest.json" % OUT;
        dict = LoadJSON(jsonFile);
        list = dict["initial"];
        gmesList = dict["game"];
        firstConfig = gmesList[0];
        if firstConfig == "config.js":
            gmesList.remove(firstConfig);
        dict["ver"] = "v" + "1.0.2.3"
        if any(list):
            isHaveWpMin = False
            NewArr = [];
            for obj in list:
                if obj.find("wp.min") >= 0:
                    isHaveWpMin = True
                if type == 2:  # 大厅保留benGame/slotGame/goldshark/redBlack
                    if obj.find("benzGame") >= 0 or obj.find("redblack") >= 0 or obj.find("goldshark") >= 0 or obj.find(
                            "slotGame") >= 0:
                        NewArr.append(obj);

            del list[:]  #清空数组
            for obj in NewArr :
                list.append(obj);

            if isHaveWpMin:
                list.insert(0, "htmls/js/agwp.min_v1.js");
            list.insert(0, "htmls/js/thr_all.min_v1.js");
            list.insert(0, "htmls/js/egret_all.min_v1.js");

            SaveJSON(jsonFile, dict, True)
    #
    # jsonFile = "%s/manifest.json" % OUT ;
    # if os.path.exists(jsonFile):
    #     fileName = LoadJSON(jsonFile)
    #     for key,value in fileName.items():
    #         print ("name = " + key + " and " + value);


    # isNeedZipPic = True;
    # if isNeedZipPic:
    #     print ("压缩")
    #     # Call('"%s" -pack "%s/resource/default.res.json" "%s/resource/ResDepotTmp.json" "%s/resource"' % (
    #     #     ResDepot, PRODIR, PRODIR, PRODIR))
    #     Call("cd C:/Users/Administrator/Desktop/imageminTest");
    #     resource_path = "./assets/"; #"C:/Users/Administrator/Desktop/out/resource";
    #     # Call("node C:/Users/Administrator/Desktop/imageminTest/index.js %s %s" % (resource_path,resource_path));
    #     Call("node C:/Users/Administrator/Desktop/imageminTest/index.js");
    # else:
    #     print ("不压缩")




    # if os.path.exists(my_files)
    #     shutil.rmtree(my_files)
    #     print ("have+++++++++++++++++")
    # shutil.copytree("%s/resource/rules" % PRODIR, "%s/resource/rules" % OUT)

    # PRODIR = "C:/Users/Administrator/Desktop/33/OdinWand-Dev/bin-release/web/h5"
    # OUT = "C:/Users/Administrator/Desktop/out"
    # shutil.copytree("%s/resource/rules" % PRODIR, "%s/resource/rules" % OUT)

    # filter = [infoFile]
    # PRODIR = "C:/Users/Administrator/Desktop/Git/bin-release/web/h5"
    # # "%s/bin-release/web/h5" % SOURCE.replace('\\', '/')
    # Info("------------------moving file -----移动文件")
    # prdirs = os.path.expanduser(PRODIR)
    # for f in os.listdir(prdirs):
    #     if (not f.strip() in filter) and f.strip() != "resource":
    #         shutil.move(os.path.join(PRODIR, f), OUT)
    #         print("11++" + f)
    # if "ResMvDir" in Conf:
    #     ResMvDir = Conf["ResMvDir"]
    #     for f in ResMvDir:
    #         shutil.move(os.path.join(PRODIR, f), OUT + "/" + f)

    print(para);

    # try:
    #     Out = 'D:\Fisker\egretPackage\egretOut'
    #     star_dir = r'%s' % Out
    #     os.system("start explorer %s" % star_dir)
    #
    # except Exception as e:
    #     print (e)
    # CrcDir(OUT + "/libs", fileMaps, filter)
    # CrcDir(OUT + "/library", fileMaps, filter)
CompilerH5("testttttt--")
# "PACKS": [
#      "slotGame"
#          ],