#!/usr/bin/env python
# -*- coding: UTF8 -*-

# UDP-based app level communication protocol
import struct
import dpkt
import datetime
import logging


logger = logging.getLogger(__name__)

SET_SWITCH_CTRL_REQ = 0x0f
SET_SWITCH_CTRL_RSP = 0x1f
NOTIFY_RAW_STATUS = 0x23


class ErrorUnknownType(Exception):
    pass


class Header(dpkt.Packet):
    length = 6
    __hdr__ = (
        ('length', 'H', 0xffff),
        ('cmd', 'B', 0xff),
        ('ret', 'B', 0xff),
        ('channel', 'B', 0xff),
        ('seq', 'B', 0xff)
    )


class Empty(dpkt.Packet):
    __hdr__ = (
    )


class SwitchCtrl(dpkt.Packet):
    length = 9
    __hdr__ = (
        ('panum', 'B', 0xff),
        ('flag1', 'B', 0x01),
        ('flag2', 'B', 0x01),
        ('flag3', 'B', 0x01),
        ('flag4', 'B', 0x01),
        ('flag5', 'B', 0x01),
        ('flag6', 'B', 0x01),
        ('flag7', 'B', 0x01),
        ('flag8', 'B', 0x01)
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


class RawData(dpkt.Packet):
    __hdr__ = (
        )


bodys = {
    SET_SWITCH_CTRL_REQ: SwitchCtrl,
    SET_SWITCH_CTRL_RSP: Empty,
    NOTIFY_RAW_STATUS: Status
}


def unpack(buf):

    header = None
    body = None

    header = Header(buf[:Header.length])

    if header.cmd in bodys:
        if bodys[header.cmd]:
            body = bodys[header.cmd](buf[Header.length:])
        else:
            body = buf[Header.length:]
    else:
        raise ErrorUnknownType("unknown packet type 0x%x" % header.cmd)

    return (header, body)
