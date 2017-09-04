#!/usr/bin/env python

from socket import *
import os, sys

HOST = ''
BUFSIZE = 2048

def SyncStateServ(port):

    udpSerSock = socket(AF_INET, SOCK_DGRAM)
    udpSerSock.bind((HOST, int(port)))


    while True:
        data, addr = udpSerSock.recvfrom(BUFSIZE)
        if data == 'stop':
            break
        print 'Receive from %s:%s.' % addr
        cmd = 'drbd-overview ' + str(data)
        res = os.popen(cmd, 'r').read()
        udpSerSock.sendto(res, addr)
    udpSerSock.close()

if __name__ == '__main__':
    _port = sys.argv[1]
    SyncStateServ(_port)
