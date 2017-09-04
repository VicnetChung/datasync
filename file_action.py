#!/usr/bin/env python
# coding=utf-8

import socket

from exec_ansible import order_run


def send_file(host_ip, src, dest):
    action=dict(module='copy', src=src, dest=dest)
    res = order_run(host_ip, action)
    if not any(res.host):
        return 'Failed: %s is not founded' % host_ip
    for hostname, result in res.host.items():
        inf = result._result
        if inf.get('unreachable', 0):
            return "Failed: %s is unreachable" % host_ip
        elif inf.get('failed', 0):
            stderr = "Failed: %s, " % host_ip
            stderr += str(inf.get('msg', '')).strip()
            return stderr
        else:
            return "Success: %s, send %s to %s" % (host_ip, src, dest)


def fetch_file(host_ip, src, dest):
    action = dict(module='fetch', src=src, dest=dest, fail_on_missing='yes', flat='yes')
    res = order_run(host_ip, action)
    local_host = socket.gethostname()
    if not any(res.host):
        return 'Failed:  %s no found' % host_ip
    for hostname, result in res.host.items():
        inf = result._result
        if inf.get('unreachable', 0):
            return "Failed: %s is unreachable" % host_ip
        elif inf.get('failed', 0):
            stderr = "Failed: %s, " % host_ip
            stderr += str(inf.get('msg', '')).strip()
            return stderr
        else:
            return "Success: fetch %s:%s to %s:%s" % (host_ip, src, local_host, dest)