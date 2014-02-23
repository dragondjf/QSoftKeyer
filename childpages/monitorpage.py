#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
import logging
import urllib2
import base64
import time
import random
from PyQt4 import QtGui
from PyQt4 import QtCore

from basepage import BasePage
from utildialog import numinput
from config import windowsoptions
from settings import currentuser
from db import userrecorddb


logger = logging.getLogger(__name__)


class MonitorPage(BasePage):

    swicthstatused = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super(MonitorPage, self).__init__(parent)
        self.parent = parent
        self.panum = windowsoptions['panum']
        self.labels_pos, self.switch_pos, self.note_ballpos, self.note_textpos, \
        self.note_labels, self.note_index= self.positationcalculate(self.panum, self.width(), self.height())
        self.paint_flag = 1
        self.paStatusLabels = {}
        self.swicthLabels = {}

        pix_red = os.sep.join([os.getcwd(), 'skin', 'images', 'colorball3', 'red.png'])
        pix_green = os.sep.join([os.getcwd(), 'skin', 'images', 'colorball3', 'green.png'])
        pix_yellow = os.sep.join([os.getcwd(), 'skin', 'images', 'colorball3', 'yellow.png'])
        pix_gray = os.sep.join([os.getcwd(), 'skin', 'images', 'colorball3', 'gray.png'])
        self.pixmap_red = QtGui.QPixmap(pix_red)
        self.pixmap_green = QtGui.QPixmap(pix_green)
        self.pixmap_yellow = QtGui.QPixmap(pix_yellow)
        self.pixmap_gray = QtGui.QPixmap(pix_gray)

        pixmap_path_on = os.sep.join([os.getcwd(), 'skin', 'images', 'on off', 'on3.png'])
        pixmap_path_off = os.sep.join([os.getcwd(), 'skin', 'images', 'on off', 'off3.png'])
        self.pixmap_on = QtGui.QPixmap(pixmap_path_on)
        self.pixmap_off = QtGui.QPixmap(pixmap_path_off)

        self.switchpixmaps = [self.pixmap_on, self.pixmap_off]
        self.pixmaps = [self.pixmap_green, self.pixmap_yellow, self.pixmap_red, self.pixmap_gray]
        self.mainswitch_flag = True

        self.text = [u'运行', u'断纤', u'告警', u'禁用']
        self.tiptext = [u'运行', u'断纤', u'告警', u'开关']
        self.painter = QtGui.QPainter()
        self.bg = os.sep.join([os.getcwd(), 'skin', 'images', 'bg2.jpg'])

    def paintEvent(self, event):
        # self.labels_pos, self.switch_pos, self.note_ballpos, self.note_textpos, \
        # self.note_labels, self.note_index= self.positationcalculate(self.panum, self.width(), self.height())
        self.painter.begin(self)
        # self.painter.drawPixmap(0, 0, self.width(), self.height(), QtGui.QPixmap(self.bg))
        if self.paint_flag == 1:
            self.initPALabel(self.painter, self.panum)
        elif self.paint_flag == 2:
            self.swicthstatus()
        elif self.paint_flag == 3:
            self.updatestatus()
        self.painter.end()

    def drawBackground(self, painter):
        painter.drawPixmap(0, 0, self.width(), self.height(), QtGui.QPixmap(self.bg))

    def createContextMenu(self):
        '''
        创建右键菜单
        '''
        # 必须将ContextMenuPolicy设置为Qt.CustomContextMenu
        # 否则无法使用customContextMenuRequested信号
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

        # 创建QMenu
        self.contextMenu = QtGui.QMenu()
        style_QMenu1 = "QMenu {background-color: #ABABAB; border: 1px solid black;}"
        style_QMenu2 = "QMenu::item {background-color: transparent;}"
        style_QMenu3 = "QMenu::item:selected { /* when user selects item using mouse or keyboard */background-color: #654321;}"
        style_QMenu = QtCore.QString(style_QMenu1 + style_QMenu2 + style_QMenu3)
        self.contextMenu.setStyleSheet(style_QMenu)

        self.action_addPAs = self.contextMenu.addAction(u'增加防区(Add PA)')
        self.action_clearPAs = self.contextMenu.addAction(u'清除防区(Clear PA)')

        self.action_addPAs.triggered.connect(self.addPAs)
        self.action_clearPAs.triggered.connect(self.clearPAs)

    def showContextMenu(self, pos):
        '''
        右键点击时调用的函数
        '''
        # 菜单显示前，将它移动到鼠标点击的位置
        coursePoint = QtGui.QCursor.pos()  # 获取当前光标的位置
        self.contextMenu.move(coursePoint)
        self.contextMenu.show()

    def addPAs(self):
        styleoptions = windowsoptions['numinputdialog']
        flag, num = numinput(styleoptions)
        self.panum = int(num)
        self.paint_flag = 1
        self.update()

    def clearPAs(self):
        self.paint_flag = 2
        self.paStatusLabels = {}
        self.swicthLabels = {}
        self.update()

    def initPALabel(self, painter, num):
        self.labels_pos, self.switch_pos, self.note_ballpos, self.note_textpos, \
        self.note_labels, self.note_index= self.positationcalculate(self.panum, self.width(), self.height())

        for paitem in self.labels_pos:
            index = self.labels_pos.index(paitem) + 1
            statuslabel = QStatusItem(index, paitem, painter)
            self.paStatusLabels.update({index: statuslabel})
            statuslabel.updatestatus()
        for item in self.switch_pos:
            index = self.switch_pos.index(item) + 1
            switchlabel = QSwitchItem(index, item, painter)
            self.swicthLabels.update({index: switchlabel})
            switchlabel.updatestatus()

        self.drawNote()
        self.drawmainswitch()

    def drawmainswitch(self):
        mainswitch_label_pos = (self.note_ballpos[0][0] - 15, self.note_ballpos[0][1] - 150, 111, 78)
        mainswitch_pos = (self.note_ballpos[0][0] - 15, self.note_ballpos[0][1] - 100, 111, 78)
        x, y, w, h = mainswitch_label_pos
        rect = QtCore.QRect(x, y, w, h)
        self.mainswitch_label_rect = rect
        self.painter.drawText(self.mainswitch_label_rect, QtCore.Qt.AlignCenter, u'总开关')
        x, y, w, h = mainswitch_pos
        rect = QtCore.QRect(x, y, w, h)
        self.mainswitch_rect = rect
        if self.mainswitch_flag:
            self.painter.drawPixmap(self.mainswitch_rect, QtGui.QPixmap(self.pixmap_on))
        else:
            self.painter.drawPixmap(self.mainswitch_rect, QtGui.QPixmap(self.pixmap_off))

    def drawNote(self):
        newFont = self.font()
        newFont.setPointSize(15)
        self.setFont(newFont)
        for item in self.note_ballpos:
            index = self.note_ballpos.index(item)
            x, y, w, h = item
            rect = QtCore.QRect(x, y, w, h)
            self.painter.drawPixmap(rect, QtGui.QPixmap(self.pixmaps[index]))

        for item in self.note_textpos:
            index = self.note_textpos.index(item)
            x, y, w, h = item
            rect = QtCore.QRect(x, y, w, h)
            self.painter.drawText(rect, QtCore.Qt.AlignCenter, self.text[index])

        for item in self.note_labels :
            index = self.note_labels.index(item)
            x, y, w, h = item
            rect = QtCore.QRect(x, y, w, h)
            self.painter.drawText(rect, QtCore.Qt.AlignCenter, self.tiptext[index])

        for item in self.note_index :
            index = self.note_index.index(item)
            x, y, w, h = item
            rect = QtCore.QRect(x, y, w, h)
            self.painter.drawText(rect, QtCore.Qt.AlignCenter, QtCore.QString('%d' % (index + 1)))

    def positationcalculate(self, panum, width, height):

        '''
        labels_pos 所有球的位置
        swicth_pos 所有开关的位置
        note_ballpos 所有指示球的位置
        note_textpos 所有指示球标识的位置
        note_labels 提示栏位置
        note_index 序号位置
        '''
        labels_pos = []
        swicth_pos = []
        note_index = []
        note_labels = []

        startX = 100
        startY = 40
        ballarea_w = width - startX * 2
        ballarea_h = height - startY - 250
        ball_diameter = min(ballarea_w / panum, ballarea_h / 3)

        for i in xrange(panum):
            pos = []
            x = startX + ballarea_w * (2 * i + 1) / (2 * panum) - ball_diameter/2
            for j in xrange(4):
                y = startY + ballarea_h * (2 * j + 1) / (2 * 3) - ball_diameter/2
                if j < 3:
                    pos.append((x, y, ball_diameter, ball_diameter))
                else:
                    swicth_pos.append((x, y, ball_diameter, 200))
            labels_pos.append(pos)
            note_index.append((x + ball_diameter / 2 - 10, 10, 20, 20))

        for j in xrange(4):
            y = startY + ballarea_h * (2 * j + 1) / (2 * 3) - ball_diameter/2
            note_labels.append((40, y + ball_diameter/2 - 20, 40, 40))

        note_x = startX + ballarea_w
        note_y = startY + ballarea_h
        notearea_w = width - note_x
        notearea_h = height - note_y
        d = max(notearea_w / 4, notearea_h / 4)

        note_ballpos = []
        note_textpos = []

        for i in xrange(2):
            x = note_x + (2 * i + 1) * notearea_w / 4 - d / 2
            for j in xrange(4):
                y = note_y + (2 * j + 1) * notearea_h / 8 - d / 2 - 18
                if i == 0:
                    note_ballpos.append((x, y, d, d))
                else:
                    note_textpos.append((x, y, d, d))

        return labels_pos, swicth_pos, note_ballpos, note_textpos, note_labels, note_index

    def swicthstatus(self):
        for index in self.swicthLabels:
            self.swicthLabels[index].updatestatus()
            self.paStatusLabels[index].updatestatus()
        self.drawNote()
        self.drawmainswitch()

    def updatestatus(self):
        for index in self.swicthLabels:
            self.swicthLabels[index].updatestatus()
            self.paStatusLabels[index].updatestatus()
        self.drawNote()
        self.drawmainswitch()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            for item in self.switch_pos:
                index = self.switch_pos.index(item) + 1
                if self.swicthLabels:
                    if self.swicthLabels[index].isContainPoint(event.pos()):
                        if self.swicthLabels[index].flag:
                            self.swicthLabels[index].flag= False
                            userrecorddb.saveaction2db(currentuser, u'禁用 %d 防区' % index)
                        else:
                            self.swicthLabels[index].flag= True
                            userrecorddb.saveaction2db(currentuser, u'启用 %d 防区' % index)
                        flags = []
                        for i in self.swicthLabels:
                            flags.append(self.swicthLabels[i].flag)
                        self.swicthstatused.emit(flags)
                self.paint_flag = 2
                self.update()
            if event.pos() in self.mainswitch_rect:
                self.mainswitch_flag = not self.mainswitch_flag
                if self.mainswitch_flag:
                    userrecorddb.saveaction2db(currentuser, u'启用所有防区')
                else:
                    userrecorddb.saveaction2db(currentuser, u'禁用所有防区')

                for index in self.swicthLabels:
                    self.swicthLabels[index].flag = self.mainswitch_flag
                flags = []
                for i in self.swicthLabels:
                    flags.append(self.swicthLabels[i].flag)
                self.swicthstatused.emit(flags)

    @QtCore.pyqtSlot(dict)
    def handlestatus(self, statusinfo):
        if self.paStatusLabels:
            logger.info((statusinfo['pa_no'], statusinfo['status']))
            self.paStatusLabels[statusinfo['pa_no']].pastatus = statusinfo['status']
        self.paint_flag = 3
        self.update()

    @QtCore.pyqtSlot(bool)
    def handlenetworkinfo(self, flag):
        flags = []
        for index in self.swicthLabels:
            self.paStatusLabels[index].flag = flag
            flags.append(flag)
        self.swicthstatused.emit(flags)
        self.paint_flag = 3
        self.update()


class QSwitchItem(QtCore.QObject):

    def __init__(self, index, rect, painter, parent=None):
        super(QSwitchItem, self).__init__()
        self.index = index
        self.rect = rect
        self.painter = painter
        self.parent = parent
        self.x, self.y, self.width, self.height = rect
        self.rect = QtCore.QRect(self.x, self.y, self.width, self.height)
        pixmap_path_on = os.sep.join([os.getcwd(), 'skin', 'images', 'on off', 'on.png'])
        pixmap_path_off = os.sep.join([os.getcwd(), 'skin', 'images', 'on off', 'off.png'])
        self.pixmap_on = QtGui.QPixmap(pixmap_path_on)
        self.pixmap_off = QtGui.QPixmap(pixmap_path_off)
        self.flag = True

    def isContainPoint(self, point):
        if point in self.rect:
            return True
        else:
            return False

    def updatestatus(self):
        if self.flag:
            self.painter.drawPixmap(self.rect, QtGui.QPixmap(self.pixmap_on))
        else:
            self.painter.drawPixmap(self.rect, QtGui.QPixmap(self.pixmap_off))


class QStatusItem(QtCore.QObject):

    status = ['connect', 'fiberbreak', 'alarm', 'disabled']

    def __init__(self, index, rects, painter, parent=None):
        super(QStatusItem, self).__init__(parent)
        self.index = index
        self.rects = rects
        self.painter = painter
        self.parent = parent
        for rect in rects:
            index = rects.index(rect)
            x, y , width, height = rect
            setattr(self, self.status[index] + 'LabelRect', QtCore.QRect(x, y, width, height))

        pix_red = os.sep.join([os.getcwd(), 'skin', 'images', 'colorball3', 'red.png'])
        pix_green = os.sep.join([os.getcwd(), 'skin', 'images', 'colorball3', 'green.png'])
        pix_yellow = os.sep.join([os.getcwd(), 'skin', 'images', 'colorball3', 'yellow.png'])
        pix_gray = os.sep.join([os.getcwd(), 'skin', 'images', 'colorball3', 'gray.png'])
        self.pixmap_red = QtGui.QPixmap(pix_red)
        self.pixmap_green = QtGui.QPixmap(pix_green)
        self.pixmap_yellow = QtGui.QPixmap(pix_yellow)
        self.pixmap_gray = QtGui.QPixmap(pix_gray)

        self.pastatus = 'disabled'

    def isContainPoint(self, point):
        if point in self.rect:
            return True
        else:
            return False

    def updatestatus(self):
        status = self.pastatus
        if status == 'connect':
            for item in ['connect']:
                self.painter.drawPixmap(getattr(self, item + 'LabelRect'), QtGui.QPixmap(self.pixmap_green))
            for item in ['fiberbreak', 'alarm']:
                self.painter.drawPixmap(getattr(self, item + 'LabelRect'), QtGui.QPixmap(self.pixmap_gray))
        elif status == 'fiberbreak':
            self.painter.drawPixmap(getattr(self, 'connect' + 'LabelRect'), QtGui.QPixmap(self.pixmap_green))
            self.painter.drawPixmap(getattr(self, 'fiberbreak' + 'LabelRect'), QtGui.QPixmap(self.pixmap_yellow))
            self.painter.drawPixmap(getattr(self, 'alarm' + 'LabelRect'), QtGui.QPixmap(self.pixmap_gray))
        elif status == 'alarm':
            self.painter.drawPixmap(getattr(self, 'connect' + 'LabelRect'), QtGui.QPixmap(self.pixmap_green))
            self.painter.drawPixmap(getattr(self, 'fiberbreak' + 'LabelRect'), QtGui.QPixmap(self.pixmap_gray))
            self.painter.drawPixmap(getattr(self, 'alarm' + 'LabelRect'), QtGui.QPixmap(self.pixmap_red))
        else:
            for item in ['connect', 'fiberbreak', 'alarm']:
                self.painter.drawPixmap(getattr(self, item + 'LabelRect'), QtGui.QPixmap(self.pixmap_gray))


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    d = MonitorPage()
    d.show()
    sys.exit(app.exec_())
