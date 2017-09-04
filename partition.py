#!/usr/bin/env python
# -*- coding: utf-8 -*-
# more: if you want more return message, you could add 'print json.dumps({hostname: inf}, indent=4)'
# in the next line of 'inf = result._result'
from exec_ansible import order_run
import json


def extend_partition(host_ip, device, size, partition=1):
    """
    extend a partition for writing drbd metadata
    :param host_ip:string
    :param device: string, like '/dev/vdb'
    :param size: int,
    :param partition:default 1
    :return: string, judge the action whether success or not, by detecting 'Failed' or 'Success' in return string
    """
    _args = 'parted ' + str(device) + ' resizepart ' + str(partition) + ' ' + str(size) + 'GB'
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
            return "Success: %s, %s%s has been extended to %dGB" % (host_ip, device, partition, size)


def create_partition(host_ip, device):
    """
    create a partition
    default: one disk create one partition and partition number will be 1. please, do not
     create more than one partition
    :param host_ip:string
    :param device:string
    :return:
    """
    action = dict(module='parted', device=device, number=1, state='present')
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
        elif inf.get('changed', 0) == 'true':
            return "Success: %s, create %s1 successful" % (host_ip, device)
        else:
            return "Failed: %s, %s1 already exist " % (host_ip, device)


def get_filesystem_type(host_ip, device):
    """
    get file system tpye of partition 1
    :param host_ip: string
    :param device: string
    :return:
    """
    action = dict(module='parted', device=device, state='info')
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
            return inf['partitions'][0]['fstype']


def mount(host_ip, src, path, partition=1):
    """

    :param host_ip:string
    :param src: string, disk device name without partition number
    :param path: string
    :param partition: default partition 1
    :return:
    """
    fstype = get_filesystem_type(host_ip, src)
    #
    _src = src + str(partition)
    action = dict(module='mount', src=_src, path=path,fstype=fstype, state='mounted')
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
            return "Success: %s, %s is mounted on %s" % (host_ip, src, path)


def umount(host_ip, src, path, partition=1):
    """

    :param host_ip:string
    :param src: string
    :param path: string
    :param partition: partition number, default 1
    :return:
    """
    _src = src + str(partition)
    action = dict(module='mount', path=path, state='unmounted')
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
            return "Success: %s, %s is unmounted from %s" % (host_ip, _src, path)


# device uuid
