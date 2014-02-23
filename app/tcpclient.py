#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import socket
import time
import random

sys.path.append(os.path.dirname(os.getcwd()))
import dpkt


class Header(dpkt.Packet):
    length = 6
    __hdr__ = (
        ('length', 'H', 0xffff),
        ('cmd', 'B', 0xff),
        ('ret', 'B', 0xff),
        ('channel', 'B', 0xff),
        ('seq', 'B', 0xff)
    )


class Status(dpkt.Packet):
    length = 16
    __hdr__ = (
        ('no1', 'B', 0x01),
        ('status1', 'B', 0xff),
        ('no2', 'B', 0x02),
        ('status2', 'B', 0xff),
        ('no3', 'B', 0x03),
        ('status3', 'B', 0xff),
        ('no4', 'B', 0x04),
        ('status4', 'B', 0xff),
        ('no5', 'B', 0x05),
        ('status5', 'B', 0xff),
        ('no6', 'B', 0x06),
        ('status6', 'B', 0xff),
        ('no7', 'B', 0x07),
        ('status7', 'B', 0xff),
        ('no8', 'B', 0x08),
        ('status8', 'B', 0xff)
    )


if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 6002))
    header = Header(cmd=0x23, ret=0, seq=0)
    while True:
        body = Status(
            status1=random.randrange(1, 4),
            status2=random.randrange(1, 4),
            status3=random.randrange(1, 4),
            status4=random.randrange(1, 4),
            status5=random.randrange(1, 4),
            status6=random.randrange(1, 4),
            status7=random.randrange(1, 4),
            status8=random.randrange(1, 4)
        )
        header.length = len(str(body))
        buf = str(header) + str(body)
        time.sleep(2)
        sock.send(buf)
