#!/usr/bin/python
# -*- coding: UTF-8 -*-

from CompilerExeGame import *
import sys
import gl
import time


def handleAssetsFile(source,destion):

    sourceSrcDir = source
    dstSrcDir = destion

    # 复制目录，olddir和newdir都只能是目录，且newdir必须不存在

    if os.path.exists(dstSrcDir):
        print dstSrcDir, 'already exist -delet first'
        # filter = []
        # EmptyTree(dstSrcDir, filter)
        shutil.rmtree(dstSrcDir)

    print 'copy begin ...'
    # shutil.copytree(sourceSrcDir, dstSrcDir)
    shutil.copytree("%s" % sourceSrcDir, "%s" % dstSrcDir)
    print 'copy end  ！\n'


def replaceFiles(sourceFile,desFile):
    sourceSrcDir = sourceFile
    dstSrcDir = desFile

    if os.path.isfile(desFile):
        print dstSrcDir, 'already exist -delet first'
        os.remove(desFile)
    print 'copy config.js begin ...'
    shutil.copyfile(sourceSrcDir,desFile)
    print 'copy config.js end  ！\n'


def moveFiel(source,des):
    handleAssetsFile(source,des)

def CompilerH5( channel, channelType ,environment):
    print (channel)
    print (channelType)
    h5_soure_path="C:/Users/Administrator/Desktop/out"

    #  ios  eg 路径: "C:/Users/Administrator/Desktop/IOS/web_test01/ProductFile/Localizable_E99/trunk"
    ios_app_path= "C:/Users/Administrator/Desktop/IOS/web_test01/ProductFile"

    # android eg路径: "C:/Users/Administrator/Desktop/Android/app/src/E99/assets/as"
    android_app_path = "C:/Users/Administrator/Desktop/Android/app/src"

    # 配置文件路径  "C:/Users/Administrator/Desktop/h5config/E99/config.js"
    as_config="C:/Users/Administrator/Desktop/h5config"

    as_environment = channel
    if(environment == "online"):
        as_environment= channel + "_online"
    elif(environment == "uat"):
        as_environment=channel + "_uat"
    else:
        as_environment = channel

    if (channelType == "iOS"):

        org_path="%s/%s/config.js" % (as_config, as_environment)
        des_path="%s/Localizable_%s/trunk/config.js" % (ios_app_path, channel)
        bund_path="%s/Localizable_%s/trunk" % (ios_app_path, channel)
        print ("ios+++++++++++++++++++++++++" + org_path + "-------" + des_path + "-------" + bund_path)
        moveFiel(h5_soure_path,bund_path)
        replaceFiles(org_path, des_path)

    elif (channelType == "android"):
        org_path = "%s/%s/config.js" % (as_config, as_environment)
        des_path = "%s/%s/assets/as/config.js" % (android_app_path, channel)
        bundle_path = "%s/%s/assets/as" % (android_app_path, channel)
        print ("Andorid+++++++++++++++++++++++++" + org_path + "-------" + des_path + "-------" + bundle_path)
        moveFiel(h5_soure_path, bundle_path)
        replaceFiles(org_path, des_path)
    else:
        print ("！！！！！！！！！！！！！！！！！！！！！！---waring:not support this platform ,please contact Fisker ")




def main(argv):
    print ("comming ----------")
    chanl="ios_A61"
    environment="test"
    type=""
    for i in range(1, len(sys.argv)):
        if(i == 1) :
            chanl = sys.argv[i]

        elif(i == 2) :
            environment = sys.argv[i];
     # print ("%s %s" % (i ,sys.argv[i]))

    print (chanl)
    print (type)
    print (environment)

    if(chanl[0:3] == "ios"):
        type= "iOS"
    elif chanl[0:3] == "and":
        type= "android"


    chanl = chanl[4:]
    print ("chan = %s" % chanl)
    print ("type = %s" % type)
    CompilerH5(chanl,type,environment)
if __name__ == "__main__":
   main(sys.argv[1:])









