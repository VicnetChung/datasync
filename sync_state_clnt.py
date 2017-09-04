#!/usr/bin/env python
from socket import *
import time
BUFSIZE = 1024
FREQUENTCE = 10

def SyncStateClnt(host, port, resource):
    udpcliSock = socket(AF_INET, SOCK_DGRAM)
    addr = (str(host), int(port))
    _resource = str(resource)
    while True:
        udpcliSock.sendto(_resource, addr)
        states, addr = udpcliSock.recvfrom(BUFSIZE)
        print states
        time.sleep(FREQUENTCE)

if __name__ == '__main__':
    SyncStateClnt('116.62.189.188', 45896, 'all')
