#!/usr/bin/env python
# -*- coding: UTF8 -*-

# UDP-based app level communication protocol
import socket
import packetdefine
import logging
from PyQt4 import QtCore
from config import windowsoptions
from utildialog import msg

logger = logging.getLogger(__name__)


class Error(Exception):
    pass


class QUdpClient(QtCore.QObject):

    def __init__(self, host, port, parent=None):
        super(QUdpClient, self).__init__(parent)
        self.host = host
        self.port = port

    def deal(self, header, body=None):

        s = None
        body_str = ''

        if body:
            body_str = str(body)
            header.length = len(body_str)
        else:
            header.length = 0

        sendbuf = str(header) + body_str

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((self.host, self.port))
            s.settimeout(3)
            logger.info('send to ' + self.host + ': ' + repr((header, body)))
            s.send(sendbuf)
            recvbuf = s.recv(1024)
            rsp = packetdefine.unpack(recvbuf)
            logger.info('recv from ' + self.host + ': ' + repr(rsp))
            return rsp
        except Exception, e:
            logging.exception(e)
            msg(u'链接超时，请检查网络链接', windowsoptions['msgdialog'])
        finally:
            if s:
                s.close()

    @QtCore.pyqtSlot(list)
    def handlecmd(self, flags):
        kwargs = {}
        for i in xrange(1, windowsoptions['panum'] + 1):
                kwargs.update({'flag%s' % i: int(flags[i - 1])})
        header = packetdefine.Header(cmd=packetdefine.SET_SWITCH_CTRL_REQ, ret=0, seq=0)
        body = packetdefine.SwitchCtrl(
                panum = windowsoptions['panum'] / 2,
                **kwargs
            )
        self.deal(header, body)
