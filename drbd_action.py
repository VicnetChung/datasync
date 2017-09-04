#!/usr/bin/env python
# coding=utf-8
# please make a file name /etc/hty before

from exec_ansible import order_run
import json


def init_metadata(host_ip, resource):
    """
    init drbd metadata when the disk device has filesystem before
    :param host_ip: string
    :param resource: string
    :return:
    """
    _args = '/etc/hty/init_metadata.sh ' + str(resource)
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
            return "Success: %s, metadata of %s create successful" % (host_ip, resource)


# if execing this function just in one vm, the drbd resource won't start properly
def start_drbd(host_ip):
    """

    :param host_ip:string
    :return:
    """
    action = dict(module='service', name='drbd', state='started')
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
            for fail_inf in inf['stdout_lines']:
                stderr = stderr + fail_inf
            return stderr
        else:
            return "Success: %s, service drbd start" % host_ip


def stop_drbd(host_ip):
    """

    :param host_ip:
    :return:
    """
    action = dict(module='service', name='drbd', state='stopped')
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
            print "Success: %s, service drbd stopped" % host_ip


def continue_resource(host_ip, resource):
    """

    :param host_ip:string
    :param resource: string
    :return:
    """
    _args = 'drbdadm up ' + str(resource)
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
            return "Success: the data sync of %s in %s is continuing now" % (resource, host_ip)


def suspend_resource(host_ip, resource):
    """

    :param host_ip: string
    :param resource: string
    :return:
    """
    _args = 'drbdadm down ' + str(resource)
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
            return "Success: the data sync of %s in %s is suspended" % (resource, host_ip)


def init_primary(host_ip, resource):
    """
    when set primary for the first time, you must exec this function,
    other than set_primary
    if exec this function failed, it may because drbd wait the counterpart resource,
    you can exec function continue_resource to fix it, and then run init_primary again
    :param host_ip:
    :param resource:
    :return:
    """
    _args = 'drbdadm -- --overwrite-data-of-peer primary ' + str(resource)
    action = dict(module='command', args=_args)
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
            for fail_inf in inf['stdout_lines']:
                stderr = stderr + fail_inf
            return stderr
        else:
            return "Success: %s, init the %s primary successfully" % (host_ip, resource)


def set_primary(host_ip, resource):
    """
    1.if set_primary for the first time, please use function init_primary
    2.if the counterpart vm has been set primary before, exec this function would
    fail
    :param host_ip:
    :param resource:
    :return:
    """
    _args = 'drbdadm primary ' + str(resource)
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
            return "Success: %s, set the %s primary successfully" % (host_ip, resource)


def set_secondary(host_ip, resource):
    """

    :param host_ip:
    :param resource:
    :return:
    """
    _args = 'drbdadm secondary ' + str(resource)
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
            return "Success: %s, set the %s secondary successfully" % (host_ip, resource)


def get_resources_state(host_ip):
    """
    1. you can exec this function every ten second to get an real-time monitor
    :param host_ip:
    :return:
    """
    _args = 'drbd-overview '
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
            return inf.get('stdout_lines', None)


