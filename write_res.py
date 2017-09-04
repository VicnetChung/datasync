#!/usr/bin/env python
# coding=utf-8
# put this file in remote instance
import sys


def write_res(resource, host):
    filename = "/etc/drbd.d/" + resource + ".res"
    lines = 'resource   ' + resource + ' {\n'
    for i in range(2):
        lines += '\ton   ' + host[i]['hostname'] + ' {\n'
        # drbd device: /dev/drbd*
        lines += '\t\tdevice   ' + host[i]['device'] + ';\n'
        lines += '\t\tdisk   ' + host[i]['disk'] + ';\n'
        lines += '\t\taddress   ' + host[i]['address'] + ':' + host[i]['port'] + ';\n'
        lines += '\t\tmeta-disk   internal;\n\t}\n'
    lines += '}\n'
    with open(filename, 'w') as file_object:
        file_object.write(lines)

if __name__ == "__main__":
    resource = str(sys.argv[1])
    hty_name = str(sys.argv[2])
    drbd_device = '/dev/drbd' + str(resource).strip('r')
    hty_disk_device = str(sys.argv[3])
    hty_ip = str(sys.argv[4])
    hty_port = str(sys.argv[5])
    pub_name = str(sys.argv[6])
    pub_disk_device = str(sys.argv[7])
    pub_ip = str(sys.argv[8])
    pub_port = str(sys.argv[9])
    hty = {'hostname': hty_name, 'device': drbd_device,
             'disk': hty_disk_device, 'address': hty_ip, 'port': hty_port}
    pub = {'hostname': pub_name, 'device': drbd_device,
             'disk': pub_disk_device, 'address': pub_ip, 'port': pub_port}
    host = [hty, pub]
    write_res(resource, host)
