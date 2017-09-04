#!/usr/bin/env python
# coding=utf-8
import json
from exec_ansible import *


def init_metadata(host_ip):
    free_form = ' /home/wenfengzhong/projects/datasync/shell/ls.sh --some-arguments test'
    action = dict(module='script', free_form=free_form)
    res = order_run(host_ip, action)
    if not any(res.host):
        return 'Failed:  %s no found' % host_ip
    for hostname, result in res.host.items():
        inf = result._result
        print json.dumps({hostname: inf}, indent=4)
        if inf.get('unreachable', 0):
            return "Failed: %s is unreachable" % host_ip
        elif inf.get('failed', 0):
            stderr = "Failed: %s, " % host_ip
            return stderr
        else:
            return "Success: "

if __name__ == '__main__':
    init_metadata('172.16.19.10')