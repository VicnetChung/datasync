#!/usr/bin/env python
# return an available port
# put this file in hengtianyun mirror /etc/hty
import socket

START = 8000
END = 8100
IP = '127.0.0.1'


def is_open(port):
    s = socket.socket()
    try:
        s.bind((IP,int(port)))
        s.close()
        return port
    except:
        s.close()
        return -1


def get_port():
    for port in range(START, END):
        r = is_open(port)
        if r > 0:
            print int(port)
            return 0
    return -1

if __name__ == '__main__':
    get_port()
