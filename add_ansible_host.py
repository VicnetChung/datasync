#!/usr/bin/env python
#add a line before detect_line
#modify the config of ansible

import os


def add_ansible_host(host_ip, user, password):
    add_host = str(host_ip) + ' ansible_ssh_user=\'' + str(user) +  '\' ansible_ssh_pass=\'' + str(password) + '\'\n'
    before_ungrouped = 'Ungrouped hosts'
    file_path = '/etc/ansible/hosts'
    tmp_file_path = file_path + ".tmp"
    with open(file_path,'r') as file_obj:
        lines = file_obj.readlines()
        with open(tmp_file_path,'w') as tmp_file_obj:
            for line in lines:
                tmp_file_obj.write(line)
                if before_ungrouped in line:
                    tmp_file_obj.write(add_host)

    os.remove(file_path)
    os.rename(tmp_file_path, file_path)
