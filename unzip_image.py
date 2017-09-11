#coding=utf-8
import os
import zipfile
import sys
#import tarfile

#解压zip文件
def unzip_dir():
    srcname=sys.argv[1]
    dstPath=sys.argv[2]

    zipHandle=zipfile.ZipFile(srcname,"r")
    #for filename in zipHandle.namelist():
        #print filename
    zipHandle.extractall(dstPath) #解压到指定目录

    zipHandle.close()