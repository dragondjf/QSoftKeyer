#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4 import QtCore
from config import windowsoptions
from settings import currentuser

class ChildPage(QtGui.QWidget):
    """docstring for childPage"""
    def __init__(self, parent=None, child=None):
        super(ChildPage, self).__init__(parent)
        self.parent = parent
        self.child = child
        self.createNavigationByPage()

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.navigation)
        mainLayout.addWidget(self.child)
        self.setLayout(mainLayout)
        self.layout().setContentsMargins(0, 0, 0, 0)


    def createNavigationByPage(self):
        # navbutton = windowsoptions['mainwindow']['centralwindow']['page_tag'][0] + ['CurrentUser', 'Min', 'Close']
        navbutton = windowsoptions['mainwindow']['centralwindow']['page_tag'][0] + ['Min', 'Close']
        navbutton_zh = windowsoptions['mainwindow']['centralwindow']['page_tag_zh']
        self.navigation = QtGui.QWidget()
        navigationLayout = QtGui.QHBoxLayout()

        for item in navbutton:
            button = item + 'Button'
            if item not in ['CurrentUser', 'Min','Close']:
                _zh = navbutton_zh[item]
                if _zh == "login":
                    _zh = u"当前用户:" + currentuser['user_name']
                setattr(self, button, QtGui.QPushButton(_zh))
                getattr(self,  button).clicked.connect(self.parent.childpageChange)
            elif item in ['Min','Close']:
                setattr(self, button, QtGui.QPushButton())
            #elif item in ['CurrentUser']:
            #    setattr(self, button, QtGui.QPushButton(u'用户名：%s\n用户角色：%s'%(currentuser['user_name'], currentuser['user_role'])))
            #    if currentuser['level'] != 1:
            #        getattr(self, button).setDisabled(True)

            getattr(self, button).setObjectName(button)
            navigationLayout.addWidget(getattr(self, button))
        self.navigation.setLayout(navigationLayout)
        self.navigation.setMaximumHeight(80)
        self.navigation.setContentsMargins(0, 0, 0, 0)

        QtCore.QObject.connect(getattr(self, 'Min' + 'Button'), QtCore.SIGNAL('clicked()'), self.parent.parent(), QtCore.SLOT('showMinimized()'))
        # QtCore.QObject.connect(getattr(self, 'Max' + 'Button'), QtCore.SIGNAL('clicked()'), self.parent.parent(), QtCore.SLOT('windowMaxNormal()'))
        QtCore.QObject.connect(getattr(self, 'Close' + 'Button'), QtCore.SIGNAL('clicked()'), self.parent.parent(), QtCore.SLOT('close()'))
