#!/usr/bin/env python
# coding=utf-8

# put this function in remote instance

import sys

def add_config(resource):
    filename = '/etc/drbd.conf'
    resource_name = '/etc/drbd.d/' + resource + '.res'
    line = 'include "' + resource_name + '";\n'
    with open(filename, 'a') as file_object:
        file_object.write(line)

if __name__ == "__main__":
    add_config(sys.argv[1])