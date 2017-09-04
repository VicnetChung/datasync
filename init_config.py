#!/usr/bin/env python
# coding=utf-8


def init_config():
    line1 = 'include "/etc/drbd.d/global_common.conf";\n'
    with open('/etc/drbd.conf', 'w') as file_object:
        file_object.write(line1)
    line2 = """
global {
    usage-count yes;
}
common {
    net {
        protocol C;
    }
    startup {

         wfc-timeout 5;
    }
}    
    """
    with open('/etc/drbd.d/global_common.conf', 'w') as file_object2:
        file_object2.write(line2)

if __name__ == "__main__":
    init_config()