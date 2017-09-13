#!/usr/bin/env python
# coding=utf-8


from exec_ansible import order_run
import time

def get_remote_hostname(host_ip):
    """

    :param host_ip:
    :return:
    """
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


def get_remote_port(host_ip):
    """
    the remote port from 8000 to 8100 by default
    :param host_ip:
    :return:
    """
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

def set_resource_name():
    """
    to avoid use the same resource name, we use the  current time in seconds
     since the Epoch as the resource name
    :return:
    """
    num = int(time.time())
    name = 'r' + str(num)
    return  name

def init_config(host_ip):
    """
    1.to run the remote python script
    2.you can change global common configuration
    by change the remote python script init_config.py
    :param host_ip:
    :return:
    """
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
                   pub_name, pub_disk_device, pub_ip, pub_port, hty_partition=1, pub_partition=1):
    """

    :param host_ip:
    :param resource:
    :param hty_name:
    :param hty_disk_device:
    :param hty_ip:
    :param hty_port:
    :param pub_name:
    :param pub_disk_device:
    :param pub_ip:
    :param pub_port:
    :return:
    """
    res_args = str(resource) + ' ' + str(hty_name) + ' ' + str(hty_disk_device) +str(hty_partition) \
              + ' ' + str(hty_ip) + ' ' + str(hty_port) + ' ' + str(pub_name) \
              + ' ' + str(pub_disk_device) + str(pub_partition) + ' ' + str(pub_ip) + ' ' + str(pub_port)
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


def add_resource(host_ip, resource):
    """

    :param host_ip:
    :param resource:
    :return:
    """
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
        
        
        
def del_resource(host_ip, resource):
    """

    :param host_ip:
    :param resource:
    :return:
    """
    _args = 'python /etc/hty/del_resource.py ' + str(resource)
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
            return "Success: %s, delete %s to file: drbd.conf successful " % (host_ip, resource)

