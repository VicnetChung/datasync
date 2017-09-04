from partition import *
from drbd_config import get_remote_port, get_remote_hostname
from add_ansible_host import add_ansible_host
#print extend_partition('172.16.19.5','/dev/vdb',27)
#print create_partition('172.16.19.2','/dev/vdc')
#print umount('172.16.19.2','/dev/vdb1','/mnt')
#print get_filesystem_type('172.16.19.3','/dev/vdb')
from drbd_config import *
#        print json.dumps({hostname: inf}, indent=4)
#
# from exec_ansible import *
# host='172.16.19.2'
# # _args = 'python drbd_config.py'
# # action = dict(module='command', args=_args, chdir='/etc/hty')
# # res = order_run(host, action)
#
# _args = 'sudo drbdadm create-md r1'
# action = dict(module='command', args=_args)
# res = order_run(host, action)
host_ip = '172.16.19.10'
user = 'root'
password = 'hengtian'
resource = 'r1'
hty_name = 'hty04'
hty_disk_device = '/dev/vdb'
hty_ip='10.50.50.11'
hty_port= '7791'
pub_name = 'ali01'
pub_disk_device = '/dev/xvdb'
pub_ip = '163.5.3.5'
pub_port = '7791'
wirte_resource(host_ip=host_ip, resource=resource, hty_name=hty_name,
               hty_disk_device=hty_disk_device, hty_ip=hty_ip, hty_port=hty_port,
               pub_name=pub_name, pub_disk_device=pub_disk_device, pub_ip=pub_ip,
               pub_port=pub_port)
# add_ansible_host(host_ip,user, password)