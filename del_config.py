#!/usr/bin/env python
# coding=utf-8
# put this function in remote instance


import os
import sys
import os.path
import shutil

def del_config(resource):
    res_name = '/etc/drbd.d/' + resource + '.res'
    filename = '/etc/drbd.conf'
    filename_tmp = filename + '.tmp'
    with open(filename, 'r') as file_objcet:
        with open(filename_tmp, 'w') as file_objcet_tmp:
            for line in file_objcet.readlines():
                if res_name not in line:
                    file_objcet_tmp.write(line)
    shutil.move(filename_tmp, filename)
    if os.path.isfile(res_name):
        os.remove(res_name)

if __name__ == "__main__":
    del_config(sys.argv[1])
