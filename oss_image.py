#!/usr/bin/env python
# coding=utf-8

from exec_ansible import order_run
import os
import sys
import json

def oss_download(host_ip, access_key_id, access_secret, end_point, bucket, remote_zip_file, local_zip_file):

    _args ='python /etc/hty/oss_download.py '+str(access_key_id) + ' ' + str(access_secret) + ' ' + \
           str(end_point) + ' ' + str(bucket) + ' ' + str(remote_zip_file) + ' ' + str(local_zip_file)
    action = dict(module='command', args=_args)
    res = order_run(host_ip, action)
    if not any(res.host):
        return 'Failed: %s is not founded' % host_ip
    for hostname, result in res.host.items():
        inf = result._result
        if inf.get('unreachable', 0):
            return "Failed: %s is unreachable" % host_ip
        elif inf.get('failed', 0):
            stderr = "Failed: %s, " % host_ip
            stderr = stderr + str(inf.get('stdout', None)).strip()
            return stderr
        else:
            return "Success"


def unzip_image(host_ip, local_zip_file, local_unzip_file):

    _args ='python /etc/hty/unzip_image.py ' + str(local_zip_file) + str(local_unzip_file)
    action = dict(module='command', args=_args)
    res = order_run(host_ip, action)
    if not any(res.host):
        return 'Failed: %s is not founded' % host_ip
    for hostname, result in res.host.items():
        inf = result._result
        if inf.get('unreachable', 0):
            return "Failed: %s is unreachable" % host_ip
        elif inf.get('failed', 0):
            stderr = "Failed: %s, " % host_ip
            stderr = stderr + str(inf.get('stdout', None)).strip()
            return stderr
        else:
            return "Success"



def oss_slice_upload(host_ip, access_key_id, access_secret, end_point, bucket, local_unzip_file, remote_unzip_file):

    _args ='python /etc/hty/oss_slice_upload.py '+str(access_key_id)+' '+str(access_secret)+' '+\
         str(end_point)+' '+str(bucket)+' '+str(local_unzip_file)+' '+str(remote_unzip_file)
    action = dict(module='command', args=_args)
    res = order_run(host_ip, action)
    if not any(res.host):
        return 'Failed: %s is not founded' % host_ip
    for hostname, result in res.host.items():
        inf = result._result
        if inf.get('unreachable', 0):
            return "Failed: %s is unreachable" % host_ip
        elif inf.get('failed', 0):
            stderr = "Failed: %s, " % host_ip
            stderr = stderr + str(inf.get('stdout', None)).strip()
            return stderr
        else:
            return "Success"

