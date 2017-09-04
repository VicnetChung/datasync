#!/usr/bin/env python
#coding=utf-8
import os, sys
from extend_partition import extend_partition
#点击数据盘
# 扩容云硬盘
# 扩大分区
#写drbd配置文件
# 创建drbd资源（写入元数据）
#启动drbd
#远程创建云盘，并挂载到drbdserver
#新建分区
#创建drbd资源
#启动drbd

def CreateDatasync():
    #在恒天云控制节点上执行硬盘扩容命令

    #扩大分区

    extend_partition()

if __name__=='__main__':
    CreateDatasync()

