#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import logging
from logging.handlers import RotatingFileHandler
from PyQt4 import QtGui
from PyQt4 import QtCore
import json

#主日志保存在log/QSoftkeyer.log
logging.root.setLevel(logging.INFO)
logging.root.propagate = 0
loghandler = RotatingFileHandler(os.path.join("log", "QSoftkeyer.log"), maxBytes=10 * 1024 * 1024, backupCount=100)
loghandler.setFormatter(logging.Formatter('%(asctime)s %(levelname)8s [%(filename)16s:%(lineno)04s] %(message)s'))
loghandler.level = logging.INFO
logging.root.addHandler(loghandler)
logger = logging.root
logger.propagate = 0


from config import windowsoptions
from effects import *
from childpages import *
from guiutil import set_skin, set_bg
import utildialog
from ping import ping
from db import userrecorddb
from db.dbutils import *
from db.user import login_db
from settings import currentuser


class MetroWindow(QtGui.QWidget):

    def __init__(self, parent=None):
        super(MetroWindow, self).__init__(parent)

        self.page_tag = windowsoptions['mainwindow']['centralwindow']['page_tag']
        self.page_tag_zh = windowsoptions['mainwindow']['centralwindow']['page_tag_zh']
        self.initUI()

    def initUI(self):
        self.pagecount = len(self.page_tag_zh)  # 页面个数
        # self.createMetroButton()
        self.pages = QtGui.QStackedWidget()  # 创建堆控件

        # self.pages.addWidget(self.navigationPage)

        self.createChildPages()  # 创建子页面

        # self.createConnections()
        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addWidget(self.pages)
        self.setLayout(mainLayout)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.faderWidget = None
        self.connect(self.pages, QtCore.SIGNAL("currentChanged(int)"), self.fadeInWidget)  # 页面切换时淡入淡出效果

    def createChildPages(self):
        '''
            创建子页面
        '''
        for buttons in self.page_tag:
            for item in buttons:
                page = item + 'Page'
                childpage = 'child' + page

                if hasattr(sys.modules[__name__], page):
                    setattr(self, page, getattr(sys.modules[__name__], page)(self))
                else:
                    setattr(self, page, getattr(sys.modules[__name__], 'BasePage')(self))
                setattr(self, childpage, ChildPage(self, getattr(self, page)))
                self.pages.addWidget(getattr(self, childpage))

    def childpageChange(self):
        '''
            页面切换响应函数
        '''
        currentpage = getattr(self, unicode('child' + self.sender().objectName()[:-6]) + 'Page')
        if hasattr(self, 'navigationPage'):
            if currentpage is self.navigationPage:
                currentpage.parent.parent().statusBar().hide()
        self.pages.setCurrentWidget(currentpage)
        self.sender().setFocus()

    @QtCore.pyqtSlot()
    def backnavigationPage(self):
        self.parent().statusBar().hide()
        self.pages.setCurrentWidget(self.navigationPage)

    @QtCore.pyqtSlot()
    def backPage(self):
        index = self.pages.currentIndex()
        if index == 1:
            self.parent().statusBar().hide()
            self.pages.setCurrentWidget(self.navigationPage)
        else:
            self.pages.setCurrentIndex(index - 1)

    @QtCore.pyqtSlot()
    def forwardnextPage(self):
        index = self.pages.currentIndex()
        if index < self.pagecount:
            self.pages.setCurrentIndex(index + 1)
        else:
            self.parent().statusBar().hide()
            self.pages.setCurrentWidget(self.navigationPage)

    def fadeInWidget(self, index):
        '''
            页面切换时槽函数实现淡入淡出效果
        '''
        self.faderWidget = FaderWidget(self.pages.widget(0.5))
        self.faderWidget.start()


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        title = windowsoptions['mainwindow']['title']
        postion = windowsoptions['mainwindow']['postion']
        minsize = windowsoptions['mainwindow']['minsize']
        size = windowsoptions['mainwindow']['size']
        windowicon = windowsoptions['mainwindow']['windowicon']
        fullscreenflag = windowsoptions['mainwindow']['fullscreenflag']
        statusbar_options = windowsoptions['mainwindow']['statusbar']
        navigation_show = windowsoptions['mainwindow']['navigation_show']

        self.setWindowIcon(QtGui.QIcon(windowicon))  # 设置程序图标
        width = QtGui.QDesktopWidget().availableGeometry().width() * 4 / 5
        height = QtGui.QDesktopWidget().availableGeometry().height() * 7 / 8
        self.setGeometry(postion[0], postion[1], width, height)  # 初始化窗口位置和大小
        self.center()  # 将窗口固定在屏幕中间
        self.setMinimumSize(minsize[0], minsize[1])
        self.setWindowTitle(title)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.fullscreenflag = fullscreenflag  # 初始化时非窗口最大话标志
        self.navigation_flag = True   # 导航标志，初始化时显示导航
        self.layout().setContentsMargins(0, 0, 0, 0)

        # self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)  # 隐藏标题栏， 可以拖动边框改变大小
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 隐藏标题栏， 无法改变大小
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMinimizeButtonHint)  # 无边框， 带系统菜单， 可以最小化
        # self.setMouseTracking(True)

        self.centeralwindow = MetroWindow(self)
        self.setCentralWidget(self.centeralwindow)

        self.statusbar = QtGui.QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage(statusbar_options['initmessage'])
        self.statusbar.setMinimumHeight(statusbar_options['minimumHeight'])
        self.statusbar.setVisible(statusbar_options['visual'])

        self.setskin()
        if self.fullscreenflag:
            self.showFullScreen()
        else:
            self.showNormal()

    def setskin(self):
        set_skin(self.centeralwindow, os.sep.join(['skin', 'qss', 'MetroNavigationPage.qss']))  # 设置导航页面样式

        for buttons in windowsoptions['mainwindow']['centralwindow']['page_tag']:
            for item in buttons:
                childpage = getattr(self.centeralwindow, 'child' + item + 'Page')
                set_skin(childpage, os.sep.join(['skin', 'qss', 'MetroNavigationBar.qss']))   # 设置导航工具条的样式

        # set_skin(self, os.sep.join(['skin', 'qss', 'MetroMainwindow.qss']))  # 设置主窗口样式

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @QtCore.pyqtSlot()
    def windowMaxNormal(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def closeEvent(self, evt):
        flag, exitflag = utildialog.exit(windowsoptions['exitdialog'])
        if flag:
            for item in exitflag:
                if item == 'minRadio' and exitflag[item]:
                    self.showMinimized()
                    evt.ignore()
                elif item == 'exitRadio' and exitflag[item]:
                    evt.accept()
                    listenserver.isalive = False
                    if listenserver.tcplistenserver:
                        listenserver.tcplistenserver.shutdown()
                elif item == 'exitsaveRadio' and exitflag[item]:
                    evt.accept()
                    listenserver.isalive = False
                    if listenserver.tcplistenserver:
                        listenserver.tcplistenserver.shutdown()
                    from db.alarmdb import db_filename, fetchby_all
                    alarmlist = fetchby_all(db_filename, 'alarmrecords')
                    alarmurl = ''.join([os.getcwd(), os.sep, 'alarm.html'])
                    alarmpage_instance = getattr(self.centeralwindow, 'AlarmPage') 
                    alarmhtml = alarmpage_instance.auto_alarmhtml(alarmlist, templateDef_relative).encode('utf-8')
                    with open(alarmurl, 'w+') as f:
                        f.write(str(alarmhtml))
                    with open(os.sep.join([os.getcwd(), 'options', 'panum.json']), 'wb') as f:
                        json.dump({'panum': windowsoptions['panum']}, f, indent=1)
                    with open(os.sep.join([os.getcwd(), 'options', 'windowsoptions.json']), 'wb') as f:
                        json.dump(windowsoptions, f, indent=1)
        else:
            evt.ignore()
        userrecorddb.saveaction2db(currentuser, u'关闭程序')

    def keyPressEvent(self, evt):
        if evt.key() == QtCore.Qt.Key_Escape:
            self.close()


from app import StatusManager
from app import QUdpClient
listenserver = StatusManager('', 6002)
udpcmdclient = QUdpClient('192.168.100.100', 6004)

def change_global_user(flag, user, password):
    currentuser['level'] = flag
    currentuser['user_name'] = user
    if flag == 1:
        currentuser['user_role'] = u"超级管理员"
    else:
        currentuser['user_role'] = u"值班员"
    currentuser['password'] = password


def main():
    mainloginoptions = windowsoptions['login_window']
    app = QtGui.QApplication(sys.argv)
    loginflag, (user, password) = utildialog.login(mainloginoptions)
    user_flag = login_db(user, password)
    if loginflag:
        change_global_user(user_flag, user, password)
        flag = False
        panuminfo = None
        if os.path.exists(os.sep.join([os.getcwd(), 'options', 'panum.json'])):
            with open(os.sep.join([os.getcwd(), 'options', 'panum.json']), 'r') as f:
                panuminfo = json.load(f)
        if panuminfo:
            flag = True
            windowsoptions['panum'] = panuminfo['panum']
        else:
            styleoptions = windowsoptions['numinputdialog']
            flag, num= utildialog.numinput(6, 2, 8, 2, styleoptions)
            windowsoptions['panum'] = num
        if flag:
            splash = QtGui.QSplashScreen(QtGui.QPixmap(windowsoptions['splashimg']))
            splash.show()
            app.processEvents()
            if flag and user_flag != 0:
                main = MainWindow()
                main.show()
                splash.finish(main)
                monitorpage_instance = getattr(main.centeralwindow, 'MonitorPage')
                alarmpage_instance = getattr(main.centeralwindow, 'AlarmPage')
                userpage_instance = getattr(main.centeralwindow, 'UserPage')
                #loginpage_instance = getattr(main.centeralwindow, 'LoginPage')
                monitorpage_instance.swicthstatused.connect(udpcmdclient.handlecmd)
                monitorpage_instance.swicthstatused.connect(userpage_instance.handlerecord)
                alarmpage_instance.recordchanged.connect(userpage_instance.handlerecord)
                #loginpage_instance.recordchanged.connect(loginpage_instance.handlerecord)
                listenserver.statuschanged.connect(monitorpage_instance.handlestatus)
                listenserver.statuschanged.connect(alarmpage_instance.handlestatus)
                # listenserver.networkbreaked.connect(monitorpage_instance.handlenetworkinfo)
                listenserver.createserver()
            else:
                msg = u"<h2>用户名或者密码错误</h2>"
                messagedialog = utildialog.MessageDialog(msg, windowsoptions['msgdialog'])
                messagedialog.show()
                splash.finish(messagedialog)
    else:
        sys.exit(0)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
