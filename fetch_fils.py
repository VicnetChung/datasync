#!/usr/bin/env python
#coding=utf-8
from exec_ansible import Order_Run
import json

def Fetch_File(host, src, dest):
    action=dict(module='fetch', src=src, dest=dest, fail_on_missing='yes', flat='yes')
    res = Order_Run(host, action)
    for hostname, result in res.host.items():
        inf = result._result
        #delete
        print json.dumps({hostname: inf}, indent=4)
        #there is no specific return item like 'success', therefore I choose the item 'dest'
        # to judge whether action is successful or not
        if inf.get('dest', 0):
            #delete
            print "success"
            return True
        elif inf.get('unreachable', 0):
            print "failed, unreachable"
            return False
        else:
            #delete
            print "failed"
            return False

_host = '172.16.19.3'
_src = '/tmp/tes='
_dest = '/tmp/'
Fetch_File(_host, _src, _dest)
