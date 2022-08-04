#!/usr/bin/python
# -*- coding: UTF-8 -*-
from GitSync import *
from CompilerExeGame import *
import gl
import time

def CompilerH5():
    # 打zip包
    path1 = shutil.make_archive("C:\Users\Administrator\Desktop\out", "zip", "C:\Users\Administrator\Desktop\out")
    print ("-ZIP Path--" + path1)
    zipPath = "C:\Users\Administrator\Desktop\h5_out"
    # jenkPath ="C:/jenkins/workspace/PIC_ Compressed/aszipgame.zip"
    shutil.move(path1, zipPath)

    currentDate = time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime(time.time()))
    originFiel = 'C:\\Users\\Administrator\\Desktop\\h5_out'
    finalFile = currentDate + ".zip"
    print (finalFile)
    os.rename(originFiel + "\\" "out.zip", originFiel + "\\" + finalFile)
    shutil.copyfile("C:/Users/Administrator/Desktop/h5_out/%s" % finalFile, "C:/jenkins/workspace/PIC_ Compressed/aszipgame.zip")
    print ("22---" + currentDate)

    Info("git push success file name:  %s " % finalFile)

    # isNeedZipPic = True
    # if isNeedZipPic:
    #     print ("--- do ----")
    #     val = os.system('cd C:/Users/Administrator/Desktop/imageminTest')
    #     print (val);
    #     var1 = os.system('node C:/Users/Administrator/Desktop/imageminTest/index.js C:/Users/Administrator/Desktop/out/resource/  C:/Users/Administrator/Desktop/out/resource/');
    #     print var1
    # else:
    #     print ("--undo----不压缩")

CompilerH5()