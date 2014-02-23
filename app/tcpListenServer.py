#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import threading
import logging
from PyQt4 import QtCore
import SocketServer
import time
import random
import sqlite3
import socket
from db import alarmdb
from db.dbutils import *
import packetdefine
import struct
from config import windowsoptions
import Queue


logger = logging.getLogger(__name__)


sqlcmd_fiberbreak = '''select * from alarmrecords where status_index=1'''
sqlcmd_alarm = '''select * from alarmrecords where status_index=2'''

longbreak_flag = {}  # 长期断开标识
break_flag = {}   # 长断和瞬断队列
break_count = {}  # 断开计数


class StatusManager(QtCore.QObject):

    statuschanged = QtCore.pyqtSignal(dict)
    networkbreaked = QtCore.pyqtSignal(bool)

    def __init__(self, ip, port, parent=None):
        super(StatusManager, self).__init__(parent)
        self.ip = ip
        self.port = port
        self.isalive = True
        self.tcplistenserver = None
        self.network_flag = False

    def createserver(self):
        try:
            self.tcplistenserver = TcpListenServer((self.ip, self.port), StatusHandler, self)
            t = threading.Thread(name="Status Listen Server Thread ", target=self.tcplistenserver.serve_forever)
            # t.setDaemon(True)
            t.start()
        except Exception, e:
            logger.exception(e)
        finally:
            pass


class ErrorPacket(Exception):
    pass


class ErrorConnect(Exception):
    pass


class ErrorConnectClose(Exception):
    pass


class ErrorHead(Exception):
    pass


class StatusHandler(SocketServer.BaseRequestHandler):

    HEAD_SIZE = 6
    status = ['disabled', 'connect', 'fiberbreak', 'alarm', 'break']
    status_zh = [u'禁用', u'运行', u'断纤', u'告警', u'断开']
    timeout = 5

    def setup(self):

        logger.warn("%s is connected!" % self.client_address[0])
        self.laststatus = None
        self.currentstatus = None
        self.request.settimeout(self.timeout)

    def handle(self):
        while self.server.manager.isalive:
            try:
                self.handlepacket()
            except Exception, e:
                logger.exception(e)
                break

    def handlepacket(self):

        """接收并处理一个完整的TCP应用层报文"""

        recv_head = None
        recv_body = None
        body_len = 0
        cid = 0

        try:
            #接收包头
            recv_head = ""  # zzh debug
            while len(recv_head) < self.HEAD_SIZE:
                recv_t = self.request.recv(self.HEAD_SIZE - len(recv_head))
                if not recv_t:
                    raise ErrorHead("can not recv head:" + str(recv_head))
                else:
                    recv_head = recv_head + recv_t
            if not recv_head or len(recv_head) == 0:
                raise ErrorConnectClose(self.client_address[0] + "connection is close.")
            elif len(recv_head) != self.HEAD_SIZE:
                logger.info(repr(recv_head))
                logger.info(len(recv_head))
                raise ErrorPacket("invalid head length.")
            else:
                body_len, cid = struct.unpack_from(">HB", recv_head)
                recv_body = ""

                if body_len > 4096:
                    raise ErrorConnect("recv head error:%d" % (body_len))
                elif body_len > 0:

                    #接收包体
                    while len(recv_body) < body_len:
                        recv_t = self.request.recv(body_len - len(recv_body))

                        if not recv_t:
                            raise ErrorConnect("can not recv body:" + str(recv_t))
                        else:
                            recv_body = recv_body + recv_t

                    #检查包完整性
                    if len(recv_body) != body_len:
                        raise ErrorConnect("recv body error! recv_len is %d" % len(recv_body))
                else:
                    recv_body = ""

            # 解析报文
            header, body = packetdefine.unpack(recv_head + recv_body)
            self.handlebody(header, body)

        except socket.timeout:
            raise ErrorConnect("tcp timeout: " + str(self.client_address[0]))
        except Exception, e:
            raise e

    def finish(self):
        # self.server.shutdown()
        logger.info('tcp finish begin')
        try:
            logger.info(repr(break_flag[self.client_address[0]]))
            logger.info(break_flag[self.client_address[0]].qsize())
            flag = break_flag[self.client_address[0]].get(True, self.timeout)
        except Queue.Empty:
            logger.info('long break!')
            longbreak_flag.update({self.client_address[0]: True})
            for i in xrange(1, 1 + windowsoptions['panum']):
                self.changestatus(i, 4)
            self.server.manager.network_flag = False
            self.server.manager.networkbreaked.emit(self.server.manager.network_flag)
        logger.info('tcp finish end')

    def handlebody(self, header, body):
        if windowsoptions['status_islog']:
            logger.info(repr(body))
        if self.laststatus:
            self.currentstatus = body
        else:
            self.laststatus = body
            self.currentstatus = body
            for i in xrange(1, 1 + windowsoptions['panum']):
                status_index = getattr(self.currentstatus, 'status%s' % i)
                self.changestatus(i, status_index)
            return

        if self.currentstatus != self.laststatus:
            for i in xrange(1, 1 + windowsoptions['panum']):
                status_index = getattr(self.currentstatus, 'status%s' % i)
                laststatus_index = getattr(self.laststatus, 'status%s' % i)
                if status_index != laststatus_index:
                    self.changestatus(i, status_index)
        self.laststatus = self.currentstatus

    def changestatus(self, pa_no, status_index):
        status_no = table_count(alarmdb.db_filename, 'alarmrecords') + 1
        pa_no = pa_no
        rid = 0
        did = (pa_no - 1) / 2 + 1
        pid = pa_no - (did - 1) * 2
        gno = '%d-%d-%d' % (rid, did, pid)
        name = u'防区%d' % pa_no
        index = status_index
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))).decode('UTF8')
        record = {
            'status_no': status_no,
            'pa_no': pa_no,
            'rid': rid,
            'did': did,
            'pid': pid,
            'gno': gno,
            'name': name,
            'status_index': index,
            'status': self.status[index],
            'status_zh': self.status_zh[index],
            'status_change_time': t
        }
        alarmrecord = (status_no, pa_no, rid, did, pid, gno, name, index, self.status[index], self.status_zh[index], t)
        alarmdb.save2db(alarmdb.table_name, alarmdb.db_filename, alarmrecord)
        self.server.manager.statuschanged.emit(record)


class TcpListenServer(SocketServer.ThreadingTCPServer):

    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass, manager):
        self.manager = manager
        SocketServer.ThreadingTCPServer.__init__(self, server_address, RequestHandlerClass)

    def verify_request(self, request, client_address):
        '''
            每个客户端ip对应一个队列break_flag[ip]，队列为空表示tcp链接长断，队列不为空表示tcp链接瞬间断开；
            下一次链接到来时判断长断标识longbreak_flag[ip]:
                如果长断标识longbreak_flag[ip]为True,表示经历过一次长期断开, 保持队列break_flag[ip]为空, longbreak_flag[ip]置为False；
                如果长断标识longbreak_flag[ip]为False, 表示从未长期断开, 向队列break_flag[ip]中put一个数据，保持队列不为空；
        '''
        self.manager.network_flag = True
        ip = client_address[0]

        if ip in break_flag:
            if longbreak_flag[ip]:
                longbreak_flag.update({ip: False})
            else:
                fqueue = break_flag[ip]
                fqueue.put_nowait(1)
                break_flag.update({ip: fqueue})
        else:
            fqueue = Queue.Queue()
            break_flag.update({ip: fqueue})

        if ip not in longbreak_flag:
            longbreak_flag.update({ip: False})

        if ip in break_count:
            break_count.update({ip: break_count[ip] + 1})
        else:
            break_count.update({ip: 0})
        logger.info('break count: %d' % break_count[ip])
        return True


if __name__ == '__main__':
    
    try:
        tcplistenserver = TcpListenServer(('', 6002), StatusHandler, '')
        t = threading.Thread(name="Status Listen Server Thread ", target=tcplistenserver.serve_forever)
        t.setDaemon(True)
        t.start()
        while True:
            time.sleep(1)
    except Exception, e:
        print e
    finally:
        pass
