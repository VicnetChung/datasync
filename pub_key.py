#!/usr/bin/env python
# expired
import os, sys

cmd1 = 'ssh-copy-id -i /root/.ssh/id_rsa.pub ' + str(sys.argv[1])
cmd2 = str(sys.argv[2])
kobj = os.popen(cmd1, 'w')
kobj.write(cmd2)
kobj.close()