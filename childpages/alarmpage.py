#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import QtNetwork
from PyQt4 import QtWebKit
from basepage import BasePage
from Cheetah.Template import Template
from db import alarmdb
from db import userrecorddb
from db.dbutils import *
from utildialog import confirm
from settings import currentuser


templateDef_absolute = '''
#set $csspath = $os.sep.join([$os.getcwd(), 'Bootstrap Metro UI CSS'])
#set $modern_css=$os.sep.join([$csspath, 'modern.css'])
#set $modern_responsive_css=$os.sep.join([$csspath, 'modern-responsive.css'])
#set $site_css=$os.sep.join([$csspath, 'site.css'])
#set $prettify_css=$os.sep.join([$csspath, 'prettify.css'])
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/html"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta charset="utf-8">
    <meta name="viewport" content="target-densitydpi=device-dpi, width=device-width, initial-scale=1.0, maximum-scale=1">
    <meta name="description" content="Metro UI CSS Alarm List">
    <meta name="author" content="dragondjf@gamil.com">
    <meta name="keywords" content="windows 8, modern style, Bootstrap,Metro UI, style, modern, css, framework">

    <link href="file:///$modern_css" rel="stylesheet" type="text/css">
    <link href="file:///$modern_responsive_css" rel="stylesheet" type="text/css">
    <link href="file:///$site_css" rel="stylesheet" type="text/css">
    <link href="file:///$prettify_css" rel="stylesheet" type="text/css">
    <title>$title</title>
    <body class="modern-ui" onload="prettyPrint()">
        <div class="page secondary" style="width: 100%">
            <div class="page-region">
                <div class="page-region-content">
                    <div class="span10" style="width: 90%">
                        <table class="hovered">
                            <thead>
                                <tr>
                                #for $header in $headers
                                <th class="text-center">$header</th>
                                #end for
                                </tr>
                            </thead>
                            <tbody>
                                #for $alarm in $alarmlist
                                    #if $alarm['status_index'] == 3
                                    <tr style="background-color: red">
                                    #elif $alarm['status_index'] == 2
                                    <tr style="background-color: yellow">
                                    #elif $alarm['status_index'] == 1
                                    <tr style="background-color: green">
                                    #elif $alarm['status_index'] == 0
                                    <tr style="background-color: lightgray">
                                    #end if
                                    <td class="text-center" style="height: 25px">$alarm['status_no']</td>
                                    <td class="text-center">$alarm['pa_no']</td>
                                    <td class="text-center">$alarm['name']</td>
                                    <td class="text-center">$alarm['status_zh']</td>
                                    <td class="text-center">$alarm['status_change_time']</td>
                                    </tr>
                                #end for
                            </tbody>
                            <tfoot></tfoot>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </body>
</html>'''

templateDef_relative = '''
#set $csspath = 'Bootstrap Metro UI CSS'
#set $modern_css=$os.sep.join([$csspath, 'modern.css'])
#set $modern_responsive_css=$os.sep.join([$csspath, 'modern-responsive.css'])
#set $site_css=$os.sep.join([$csspath, 'site.css'])
#set $prettify_css=$os.sep.join([$csspath, 'prettify.css'])
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/html"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta charset="utf-8">
    <meta name="viewport" content="target-densitydpi=device-dpi, width=device-width, initial-scale=1.0, maximum-scale=1">
    <meta name="description" content="Metro UI CSS Alarm List">
    <meta name="author" content="dragondjf@gamil.com">
    <meta name="keywords" content="windows 8, modern style, Bootstrap,Metro UI, style, modern, css, framework">

    <link href="$modern_css" rel="stylesheet" type="text/css">
    <link href="$modern_responsive_css" rel="stylesheet" type="text/css">
    <link href="$site_css" rel="stylesheet" type="text/css">
    <link href="$prettify_css" rel="stylesheet" type="text/css">
    <title>$title</title>
    <body class="modern-ui" onload="prettyPrint()">
        <div class="page secondary" style="width: 100%">
            <div class="page-region">
                <div class="page-region-content">
                    <div class="span10" style="width: 90%">
                        <table class="hovered">
                            <thead>
                                <tr>
                                #for $header in $headers
                                <th class="text-center">$header</th>
                                #end for
                                </tr>
                            </thead>
                            <tbody>
                                #for $alarm in $alarmlist
                                    #if $alarm['status_index'] == 3
                                    <tr style="background-color: red">
                                    #elif $alarm['status_index'] == 2
                                    <tr style="background-color: yellow">
                                    #elif $alarm['status_index'] == 1
                                    <tr style="background-color: green">
                                    #elif $alarm['status_index'] == 0
                                    <tr style="background-color: lightgray">
                                    #end if
                                    <td class="text-center" style="height: 25px">$alarm['status_no']</td>
                                    <td class="text-center">$alarm['pa_no']</td>
                                    <td class="text-center">$alarm['name']</td>
                                    <td class="text-center">$alarm['status_zh']</td>
                                    <td class="text-center">$alarm['status_change_time']</td>
                                    </tr>
                                #end for
                            </tbody>
                            <tfoot></tfoot>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </body>
</html>'''
# class AlarmPage1(BasePage):
#     def __init__(self, parent=None):
#         super(AlarmPage1, self).__init__(parent)
#         self.parent = parent

#         hheaders = [u'采集器', u'DC编号', u'PA编号', u'发生时间', u'是否确认', u'告警复核', u'确认备注', u'确认时间', u'操作员', u'全选']
#         vheaders = [str(i) for i in range(10)]
#         self.hheaders_width = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
#         contents = []
#         for i in range(len(vheaders)):
#             alarm = []
#             for j in range(len(hheaders)):
#                 alarm.append(str((i + 1) * (j + 1)))
#             contents.append(alarm)

#         self.table = CumstomTable(hheaders, vheaders, contents, self)

#         mainlayout = QtGui.QVBoxLayout()
#         mainlayout.addWidget(self.table)
#         self.setLayout(mainlayout)

#     def resizeEvent(self, event):
#         width = self.parent.width()
#         if hasattr(self, 'table'):
#             for i in range(len(self.hheaders_width)):
#                 self.table.setColumnWidth(i, self.hheaders_width[i] * width)


# class CumstomTable(QtGui.QTableWidget):
#     def __init__(self, hheaders, vheaders, contents, parent=None):
#         super(CumstomTable, self).__init__(len(vheaders), len(hheaders), parent)
#         self.parent = parent
#         self.hheaders = hheaders
#         self.vheaders = vheaders
#         self.contents = contents

#         self.setupHeaders()
#         self.setupContents()

#     def setupHeaders(self):
#         width = self.parent.parent.parent().width() * 2
#         for key in self.hheaders:
#             index = self.hheaders.index(key)
#             self.setHorizontalHeaderItem(index, QtGui.QTableWidgetItem(key))

#         for key in self.vheaders:
#             index = self.vheaders.index(key)
#             self.setVerticalHeaderItem(index, QtGui.QTableWidgetItem(key))

#         titleFont = self.font()
#         for x in range(self.columnCount()):
#             headItem = self.horizontalHeaderItem(x)   # 获得水平方向表头的Item对象
#             headItem.setFont(titleFont)                      # 设置字体
#             headItem.setBackgroundColor(QtGui.QColor(0, 60, 10))      # 设置单元格背景颜色
#             headItem.setTextColor(QtGui.QColor(200, 111, 30))         # 设置文字颜色

#         for x in range(self.rowCount()):
#             headItem = self.verticalHeaderItem(x)   # 获得水平方向表头的Item对象
#             headItem.setFont(titleFont)   # 设置字体
#             headItem.setBackgroundColor(QtGui.QColor(0, 60, 10))      # 设置单元格背景颜色
#             headItem.setTextColor(QtGui.QColor(200, 111, 30))         # 设置文字颜色

#     def setupContents(self):
#         for alarm in self.contents:
#             rowindex = self.contents.index(alarm)
#             for con in alarm:
#                 colindex = alarm.index(con)
#                 self.setItem(colindex, rowindex, QtGui.QTableWidgetItem(con))


class AlarmPage(BasePage):

    recordchanged = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(AlarmPage, self).__init__(parent)
        self.parent = parent

        self.pageLabel = QtGui.QLabel()

        upButton = QtGui.QPushButton(u'上一页')
        upButton.setObjectName('BackButton')
        upButton.setToolTip(u'上一页')
        self.upButton = upButton

        downButton = QtGui.QPushButton(u'下一页')
        downButton.setObjectName('ForwardButton')
        downButton.setToolTip(u'下一页')
        self.downButton = downButton

        clearrecordsButton = QtGui.QPushButton(u'清除记录')
        clearrecordsButton.setObjectName('ClearrecordsButton')
        clearrecordsButton.setToolTip(u'清除所有记录')
        self.clearrecordsButton = clearrecordsButton

        downloadButton = QtGui.QPushButton(u'导出记录')
        downloadButton.setObjectName('DownloadButton')
        downloadButton.setToolTip(u'导出告警记录')

        downloadButton.clicked.connect(self.download_alarm2html)
        upButton.clicked.connect(self.up_alarmpage)
        downButton.clicked.connect(self.down_alarmpage)
        clearrecordsButton.clicked.connect(self.clearrecords)

        alarmtool = QtGui.QWidget()
        alarmtool_layout = QtGui.QGridLayout()
        n = 15
        for i in xrange(n-5):
            alarmtool_layout.addWidget(QtGui.QLabel(), 0, i)
        alarmtool_layout.addWidget(self.pageLabel, 0, n-5)
        alarmtool_layout.addWidget(upButton, 0, n-4)
        alarmtool_layout.addWidget(downButton, 0, n-3)
        alarmtool_layout.addWidget(clearrecordsButton, 0, n-2)
        alarmtool_layout.addWidget(downloadButton, 0, n-1)
        alarmtool_layout.addWidget(QtGui.QLabel(), 0, n)
        alarmtool.setLayout(alarmtool_layout)
        alarmtool_layout.setContentsMargins(0, 0, 0, 0)
        alarmtool.setMaximumHeight(50)

        QtNetwork.QNetworkProxyFactory.setUseSystemConfiguration(True)
        self.view = QtWebKit.QWebView(self)
        self.view.setFocus()

        mainlayout = QtGui.QVBoxLayout()
        mainlayout.addWidget(alarmtool)
        mainlayout.addWidget(self.view)
        self.setLayout(mainlayout)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.loadfromdb()

    def auto_alarmhtml(self, alarmhistory, template):
        nameSpace = {
            'title': "告警列表",
            'headers': [u'告警编号', u'防区编号', u'防区名字', u'告警类型', u'告警时间'],
            'alarmlist': alarmhistory
        }
        t = Template(template, searchList=[nameSpace])
        alarmhtml = unicode(t)
        return alarmhtml

    def loadfromdb(self):
        self.currentindex = 0
        alarmpages = self.pagination()
        if alarmpages:
            self.currentpage = self.pagination()[0]
            self.downButton.setDisabled(False)
            self.upButton.setDisabled(True)
            alarmhtml = self.auto_alarmhtml(self.currentpage, templateDef_absolute)
            self.view.setHtml(alarmhtml, QtCore.QUrl(os.getcwd()))
        self.updatecurrentpage(len(alarmpages))

    @QtCore.pyqtSlot(dict)
    def handlestatus(self, statusinfo):
        alarmpages = self.pagination()
        if alarmpages:
            self.currentpage = alarmpages[0]
            self.currentindex = 0
            if len(alarmpages) > 1:
                self.downButton.setDisabled(False)
            alarmhtml = self.auto_alarmhtml(self.currentpage, templateDef_absolute)
            self.view.setHtml(alarmhtml, QtCore.QUrl(os.getcwd()))
        self.updatecurrentpage(len(alarmpages))

    def pagination(self, length_page=20):
        alarms = fetchby_all(alarmdb.db_filename, alarmdb.table_name)
        import copy
        alarms_new = copy.deepcopy(alarms)
        alarms_new.reverse()
        alarmpages = [alarms_new[i:i + length_page] for i in xrange(0, len(alarms_new), length_page)]
        return alarmpages

    def changepage(self, index):
        alarmpages = self.pagination()
        if alarmpages:
            self.currentpage = alarmpages[index]
            self.currentindex = index
            alarmhtml = self.auto_alarmhtml(self.currentpage, templateDef_absolute)
            self.view.setHtml(alarmhtml, QtCore.QUrl(os.getcwd()))
        self.updatecurrentpage(len(alarmpages))

    def updatecurrentpage(self, page_num):
        if self.currentindex < 1:
            self.upButton.setDisabled(True)
        self.pageLabel.setText(u"<h2>第%s页(共%s页)</h2>" % (self.currentindex + 1, page_num))

    def up_alarmpage(self):
        alarmpages = self.pagination()
        if alarmpages:
            self.downButton.setDisabled(False)
            self.currentindex -= 1
            if self.currentindex == 0:
                self.upButton.setDisabled(True)
                self.currentpage = alarmpages[0]
            self.currentpage = alarmpages[self.currentindex]
            alarmhtml = self.auto_alarmhtml(self.currentpage, templateDef_absolute)
            self.view.setHtml(alarmhtml, QtCore.QUrl(os.getcwd()))
        self.updatecurrentpage(len(alarmpages))

    def down_alarmpage(self):
        alarmpages = self.pagination()
        if alarmpages:
            self.upButton.setDisabled(False)
            self.currentindex += 1
            if self.currentindex == len(alarmpages) - 1:
                self.downButton.setDisabled(True)
                self.currentpage = alarmpages[self.currentindex]
            self.currentpage = alarmpages[self.currentindex]
            alarmhtml = self.auto_alarmhtml(self.currentpage, templateDef_absolute)
            self.view.setHtml(alarmhtml, QtCore.QUrl(os.getcwd()))
        self.updatecurrentpage(len(alarmpages))

    def clearrecords(self):
        from config import windowsoptions
        if confirm(u'<h1>确定删除所有告警记录?</h1>', windowsoptions['confirmdialog']):
            flag = delete_all(alarmdb.db_filename, 'alarmrecords')
            if flag:
                userrecorddb.saveaction2db(currentuser, u'清除所有告警记录')
                self.recordchanged.emit()
                self.view.setHtml(u'', QtCore.QUrl(os.getcwd()))
                self.upButton.setDisabled(True)
                self.downButton.setDisabled(True)
                alarmpages = self.pagination()
                self.updatecurrentpage(len(alarmpages))

    def download_alarm2html(self):
        import shutil
        alarmurl = unicode(self.setSaveFileName())
        if alarmurl:
            alarmlist = fetchby_all(alarmdb.db_filename, 'alarmrecords')
            alarmhtml = self.auto_alarmhtml(alarmlist, templateDef_relative).encode('utf-8')
            with open(alarmurl, 'w+') as f:
                f.write(str(alarmhtml))
        dirname = os.path.dirname(alarmurl)
        if os.path.exists(dirname):
            alarmfloder = dirname + os.sep + u'告警记录'
            if os.path.exists(alarmfloder):
                shutil.rmtree(alarmfloder)
                os.mkdir(alarmfloder)
            else:
                os.mkdir(alarmfloder)
            shutil.copyfile(alarmurl, alarmfloder + os.sep + os.path.basename(alarmurl))
            for item in ['Bootstrap Metro UI CSS']:
                shutil.copytree(os.getcwd() + os.sep + item, alarmfloder + os.sep + item)
            os.remove(alarmurl)
        userrecorddb.saveaction2db(currentuser, u'导出所有告警记录')
        self.recordchanged.emit()
        # else:
        #     if os.getcwd() == os.path.abspath(os.path.dirname(__file__)):
        #         alarmurl = ''.join([os.path.dirname(os.getcwd()), os.sep, 'autoalarm.html'])
        #     else:
        #         alarmurl = ''.join([os.getcwd(), os.sep, 'autoalarm.html'])

    def setSaveFileName(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self,
                u"保存告警历史记录",
                u'告警记录',
                "Html Files (*.html)")
        return fileName


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    d = AlarmPage()
    d.show()
    sys.exit(app.exec_())
