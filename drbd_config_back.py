#!/usr/bin/env python
# coding=utf-8


import os
import os.path
import json
import shutil

from exec_ansible import order_run, playbook_run


def get_remote_hostname(host_ip):
    _args = 'hostname'
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
            stderr += str(inf.get('msg', '')).strip()
            return stderr
        else:
            return str(inf.get('stdout', None))

# figure out another way
def get_remote_port(host_ip):
    _args = 'python /etc/hty/get_port.py'
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
            stderr += str(inf.get('msg', '')).strip()
            return stderr
        else:
            port = inf.get('stdout', None)
            try:
                _port = int(port)
                if _port > 0:
                    return _port
                else:
                    return "Failed: %s, no port available"
            except ValueError, e:
                return e


def init_config(host_ip):
    _args = 'python /etc/hty/init_config.py'
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
            stderr += str(inf.get('msg', '')).strip()
            return stderr
        else:
            return "Success: %s, init the configuration successful" % host_ip


def wirte_resource(host_ip, resource, hty_name, hty_disk_device, hty_ip, hty_port,
                   pub_name, pub_disk_device, pub_ip, pub_port):
    res_args = str(resource) + ' ' + str(hty_name) + ' ' + str(hty_disk_device) \
              + ' ' + str(hty_ip) + ' ' + str(hty_port) + ' ' + str(pub_name) \
              + ' ' + str(pub_disk_device) + ' ' + str(pub_ip) + ' ' + str(pub_port)
    _args = 'python /etc/hty/write_res.py ' + res_args
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
            stderr += str(inf.get('msg', '')).strip()
            return stderr
        else:
            return "Success: %s, write the resource configuration successful" % host_ip

#
# def init_config():
#     line1 = 'include "/etc/drbd.d/global_common.conf";\n'
#     with open('/etc/drbd.conf', 'w') as file_object:
#         file_object.write(line1)
#     line2 = """
# global {
#     usage-count yes;
# }
# common {
#     net {
#       protocol C;
#     }
# }
#     """
#     with open('/etc/drbd.d/global_common.conf', 'w') as file_object2:
#         file_object2.write(line2)
#
#
# def write_res(resource, host):
#     filename = "/etc/drbd.d/" + resource + ".res"
#     lines = 'resource   ' + resource + '{\n'
#     for i in range(2):
#         lines += '\ton   ' + host[i]['hostname'] + '{\n'
#         # drbd device: /dev/drbd*
#         lines += '\t\tdevice   ' + host[i]['device'] + ';\n'
#         lines += '\t\tdisk   ' + host[i]['disk'] +';\n'
#         lines += '\t\taddress   ' + host[i]['address'] + ':' + host[i]['port'] + ';\n'
#         lines += '\t\tmeta-disk   internal;\n\t}\n'
#     lines += '}\n'
#     with open(filename, 'w') as file_object:
#         file_object.write(lines)


def add_config(host_ip, resource):
    _args = 'python /etc/hty/add_config.py ' + str(resource)
    action = dict(module='command', args=_args)
    res = order_run(host_ip, action)
    if not any(res.host):
        return 'Failed:  %s no found' % host_ip
    for hostname, result in res.host.items():
        inf = result._result
        if inf.get('unreachable', 0):
            return "Failed: %s is unreachable" % host_ip
        elif inf.get('failed', 0):
            stderr = "Failed: %s, " % host_ip
            for fail_inf in inf['stdout_lines']:
                stderr = stderr + fail_inf
            return stderr
        else:
            return "Success: %s, add %s to file: drbd.conf successful " % (host_ip, resource)


#
# # put this function in remote instance
# def add_config(resource):
#     filename = '/etc/drbd.conf'
#     real_name = '/etc/drbd.d/' + resource + '.res'
#     line = 'include "' + real_name + '";\n'
#     with open(filename, 'a') as file_object:
#         file_object.write(line)
#
#
# # put this function in remote instance
# def del_config(resource):
#     res_name = '/etc/drbd.d/' + resource + '.res'
#     filename = '/etc/drbd.conf'
#     filename_tmp = filename + '.tmp'
#     with open(filename, 'r') as file_objcet:
#         with open(filename_tmp, 'w') as file_objcet_tmp:
#             for line in file_objcet.readlines():
#                 if res_name not in line:
#                     file_objcet_tmp.write(line)
#     shutil.move(filename_tmp, filename)
#     if os.path.isfile(res_name):
#         os.remove(res_name)



#tesing

#
# init_config()
# resource = 'r1'
# host0 = { 'hostname': 'hty03', 'device': '/dev/drbd1',
#               'disk': '/dev/vdb1', 'address': '10.50.50.6', 'port': '7794'}
# host1 = {'hostname': 'drbdserver', 'device': '/dev/drbd1',
#              'disk': '/dev/xvdb1', 'address': '10.168.58.128', 'port': '7788'}
# host = [host0, host1]
# write_res(resource, host)
# add_config('r1')

