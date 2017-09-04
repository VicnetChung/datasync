#!/usr/bin/env python
# coding=utf-8
from exec_ansible import order_run, playbook_run, add_ansible_host
from partition import *
from drbd_config import *
import os
from drbd_action import*

# 以下参数通过调用恒天云/阿里云api获得，或者由用户填入
host_ip='172.16.19.6'
password='hengtian'
user='root'
device='/dev/vdb'
size=15
disk_id='21cf094d-c77c-4d38-80ec-d610acd9745a'
resource = 'r1'

# step0: 容灾云主机镜像要求：制作一份新的ubuntu镜像包含以下内容
# drbd kernel :1. sudo apt-get update
#              2. https://serverfault.com/questions/371783/drbd-not-starting-on-fresh-aws-64-bit-ubuntu-11-10
#              3. 重启云主机， 运行 modprobe drbd
# expect: sudo apt-get update  sudo apt-get install expect
# 导入部分文件：1.mkdir /etc/hty 2. get_port.py
# 控制节点要求：
# 安装 ansible 软件, 在host文件中添加[hty]组


# step1:用户点击 “创建容灾” 后， 建立控制节点到hty云主机和aliyun drbdserver的连接.
#       要求以root用户执行add_pub_key.sh
# cmd_add_key='/home/wenfengzhong/projects/datasync/shell/add_pub_key.sh ' + host_ip + ' ' + password
# os.popen(cmd_add_key,'r')

# step2:添加本地主机到 ansible hosts文件
#       已root用户执行
#add_ansible_host(host_ip,user,password)

# step3:调用hty api接口， 将云硬盘大小扩大5G。 磁盘的卸载和挂载最好在云主机关机状态下执行，否则
# 磁盘的device名将出错,恒天云界面显示 /dev/vdb， 实际为/dev/vdc

# step4:扩展分区, size 为云硬盘扩展后的大小
extend_partition(host_ip, device, size)

# step5: 从hty 云主机  aliyun drbdserver 以下信息
# step5.1: 通过恒天云api获得磁盘id 作为 资源名 drbd device名
# resource='r' + disk_id
# drbd_device='/dev/drbd'+disk_id
# host_name= get_remote_hostname(host_ip)
# print host_name

# 配置问题继续研究。初步决定在远程写

#写drbd metadata
init_metadata(host_ip,resource)