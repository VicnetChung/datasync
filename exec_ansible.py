#!/bin/env python
# coding=utf-8

import os
from collections import namedtuple

from ansible import constants
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.plugins.callback import CallbackBase
from ansible.vars import VariableManager

OPT_LIST = ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection', 'module_path', 'forks',
            'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args',
            'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity',
            'check']
Options = namedtuple('Options', OPT_LIST)
options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh',
                  module_path=None, forks=100, remote_user='root', private_key_file=None, ssh_common_args=None,
                  ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=True,
                  become_method='sudo', become_user='root', verbosity=None, check=False)


def playbook_run(playbook_path, playbook_vars):
    """
    run an ansible playbook
    :param playbook_path:
    :param playbook_vars:
    :return:
    """
    variable_manager = VariableManager()
    variable_manager.extra_vars = playbook_vars
    loader = DataLoader()
    inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list='/etc/ansible/hosts')

    passwords = {}
    pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager,
                            loader=loader, options=options, passwords=passwords)
    result = pbex.run()
    return result


class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in
       """

    def __init__(self, *args, **kwargs):
        self.host = {}

    def v2_runner_on_unreachable(self, result):
        self.host[result._host.get_name()] = result

    def v2_runner_on_ok(self, result):
        self.host[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host[result._host.get_name()] = result


def order_run(host, action):
    """
    run an ansible order
    :param host: string
    :param action: dict
    :return: return an object ResultCallback
    """
    variable_manager = VariableManager()
    loader = DataLoader()
    inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list='/etc/ansible/hosts')
    passwords = {}

    play_source = dict(
        name="Ansible Play",
        hosts=host,
        gather_facts='no',
        tasks=[dict(action=action)]
    )
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

    tqm = None
    callback = ResultCallback()
    try:
        tqm = TaskQueueManager(
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            options=options,
            passwords=passwords,
            stdout_callback=callback,
            run_additional_callbacks=constants.DEFAULT_LOAD_CALLBACK_PLUGINS,
            run_tree=False,
        )

        tqm.run(play)

    finally:
        if tqm is not None:
            tqm.cleanup()
    return callback


def add_ansible_host(host_ip, user, password):
    """
    add a host in /etc/ansible/hosts
    :param host_ip: string
    :param user: string
    :param password: string
    :return:
    """
    _user = "\'" + str(user) + "\'"
    _password="\'" + str(password) + "\'"
    add_host = str(host_ip) + ' ansible_ssh_user=' + _user + ' ansible_ssh_pass=' + _password + '\n'
    before_ungrouped = 'Ungrouped hosts'
    before_hty = 'hty'
    file_path = '/etc/ansible/hosts'
    tmp_file_path = file_path + ".tmp"
    with open(file_path,'r')as file_obj:
        lines = file_obj.readlines()
        with open(tmp_file_path,'w') as tmp_file_obj:
            for line in lines:
                tmp_file_obj.write(line)
                if before_ungrouped in line:
                    tmp_file_obj.write(add_host)
                if before_hty in line:
                    tmp_file_obj.write(add_host)

    os.remove(file_path)
    os.rename(tmp_file_path, file_path)