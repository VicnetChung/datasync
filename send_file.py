#!/usr/bin/env python
#coding=utf-8
from exec_ansible import order_run
import json

def send_file(host_ip, src, dest):
    action=dict(module='copy', src=src, dest=dest)
    res = order_run(host_ip, action)
    for hostname, result in res.host.items():
        inf = result._result
        #delete
        print json.dumps({hostname: inf}, indent=4)
        #there is no specific return item like 'success', therefore I choose the item 'size'
        # to judge whether action is successful or not
        if inf.get('size', 0) :
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
