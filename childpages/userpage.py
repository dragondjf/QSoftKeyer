#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import QtNetwork
from PyQt4 import QtWebKit
from basepage import BasePage
from Cheetah.Template import Template
from db.dbutils import *
from db import userrecorddb
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
    <meta name="description" content="Metro UI CSS UserRecord List">
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
                                #for $record in $recordlist
                                    <td class="text-center" style="height: 25px">$record['no']</td>
                                    <td class="text-center">$record['level']</td>
                                    <td class="text-center">$record['user_name']</td>
                                    <td class="text-center">$record['user_role']</td>
                                    <td class="text-center">$record['user_action']</td>
                                    <td class="text-center">$record['action_time']</td>
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
    <meta name="description" content="Metro UI CSS user List">
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
                                #for $record in $recordlist
                                    <td class="text-center" style="height: 25px">$record['no']</td>
                                    <td class="text-center">$record['level']</td>
                                    <td class="text-center">$record['user_name']</td>
                                    <td class="text-center">$record['user_role']</td>
                                    <td class="text-center">$record['user_action']</td>
                                    <td class="text-center">$record['action_time']</td>
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


class UserPage(BasePage):
    def __init__(self, parent=None):
        super(UserPage, self).__init__(parent)
        self.parent = parent
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
        clearrecordsButton.setToolTip(u'清除所有操作记录')
        self.clearrecordsButton = clearrecordsButton

        downloadButton = QtGui.QPushButton(u'导出记录')
        downloadButton.setObjectName('DownloadButton')
        downloadButton.setToolTip(u'导出所有操作记录')

        downloadButton.clicked.connect(self.download_html)
        upButton.clicked.connect(self.up_page)
        downButton.clicked.connect(self.down_page)
        clearrecordsButton.clicked.connect(self.clearrecords)

        usertool = QtGui.QWidget()
        usertool_layout = QtGui.QGridLayout()
        n = 15
        for i in xrange(n-5):
            usertool_layout.addWidget(QtGui.QLabel(), 0, i)
        usertool_layout.addWidget(self.pageLabel, 0, n-5)
        usertool_layout.addWidget(upButton, 0, n-4)
        usertool_layout.addWidget(downButton, 0, n-3)
        usertool_layout.addWidget(clearrecordsButton, 0, n-2)
        usertool_layout.addWidget(downloadButton, 0, n-1)
        usertool_layout.addWidget(QtGui.QLabel(), 0, n)
        usertool.setLayout(usertool_layout)
        usertool_layout.setContentsMargins(0, 0, 0, 0)
        usertool.setMaximumHeight(50)

        QtNetwork.QNetworkProxyFactory.setUseSystemConfiguration(True)
        self.view = QtWebKit.QWebView(self)
        self.view.setFocus()

        mainlayout = QtGui.QVBoxLayout()
        mainlayout.addWidget(usertool)
        mainlayout.addWidget(self.view)
        self.setLayout(mainlayout)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.loadfromdb()

    def auto_html(self, recordlist, template):
        nameSpace = {
            'title': "用户操作记录列表",
            'headers': [u'记录编号', u'操作员编号', u'操作员名字', u'操作员角色', u'操作动作', u'操作时间'],
            'recordlist': recordlist
        }
        t = Template(template, searchList=[nameSpace])
        html = unicode(t)
        return html

    def loadfromdb(self):
        self.currentindex = 0
        pages = self.pagination()
        if pages:
            self.currentpage = self.pagination()[0]
            self.downButton.setDisabled(False)
            self.upButton.setDisabled(True)
            html = self.auto_html(self.currentpage, templateDef_absolute)
            self.view.setHtml(html, QtCore.QUrl(os.getcwd()))
        self.updatecurrentpage(len(pages))

    def pagination(self, length_page=20):
        items = fetchby_all(userrecorddb.db_filename, userrecorddb.table_name)
        import copy
        items_new = copy.deepcopy(items)
        items_new.reverse()
        pages = [items_new[i:i + length_page] for i in xrange(0, len(items_new), length_page)]
        return pages

    def updatecurrentpage(self, page_num):
        self.pageLabel.setText(u"<h2>第%s页(共%s页)</h2>" % (self.currentindex + 1, page_num))

    @QtCore.pyqtSlot()
    def handlerecord(self):
        pages = self.pagination()
        if pages:
            self.currentpage = pages[0]
            self.currentindex = 0
            if len(pages) > 1:
                self.downButton.setDisabled(False)
            html = self.auto_html(self.currentpage, templateDef_absolute)
            self.view.setHtml(html, QtCore.QUrl(os.getcwd()))
        self.updatecurrentpage(len(pages))

    def up_page(self):
        pages = self.pagination()
        if pages:
            self.downButton.setDisabled(False)
            self.currentindex -= 1
            if self.currentindex == 0:
                self.upButton.setDisabled(True)
                self.currentpage = pages[0]
            self.currentpage = pages[self.currentindex]
            html = self.auto_html(self.currentpage, templateDef_absolute)
            self.view.setHtml(html, QtCore.QUrl(os.getcwd()))
        self.updatecurrentpage(len(pages))

    def down_page(self):
        pages = self.pagination()
        self.upButton.setDisabled(False)
        if pages:
            self.currentindex += 1
            if self.currentindex == len(pages) - 1:
                self.downButton.setDisabled(True)
                self.currentpage = pages[self.currentindex]
            self.currentpage = pages[self.currentindex]
            html = self.auto_html(self.currentpage, templateDef_absolute)
            self.view.setHtml(html, QtCore.QUrl(os.getcwd()))
        self.updatecurrentpage(len(pages))

    def clearrecords(self):
        from config import windowsoptions
        if confirm(u'<h1>确定删除所有用户操作记录?</h1>', windowsoptions['confirmdialog']):
            flag = delete_all(userrecorddb.db_filename, userrecorddb.table_name)
            if flag:
                self.view.setHtml(u'', QtCore.QUrl(os.getcwd()))
                self.upButton.setDisabled(True)
                self.downButton.setDisabled(True)
                userrecorddb.saveaction2db(currentuser, u'清除所有操作记录')
                self.handlerecord()
                alarmpages = self.pagination()
                self.updatecurrentpage(len(alarmpages))

    def download_html(self):
        import shutil
        url = unicode(self.setSaveFileName())
        if url:
            UserRecordlist = fetchby_all(userrecorddb.db_filename, userrecorddb.table_name)
            UserRecordhtml = self.auto_html(UserRecordlist, templateDef_relative).encode('utf-8')
            with open(url, 'w+') as f:
                f.write(str(UserRecordhtml))
        dirname = os.path.dirname(url)
        if os.path.exists(dirname):
            floder = dirname + os.sep + u'用户操作记录'
            if os.path.exists(floder):
                shutil.rmtree(floder)
                os.mkdir(floder)
            else:
                os.mkdir(floder)
            shutil.copyfile(url, floder + os.sep + os.path.basename(url))
            for item in ['Bootstrap Metro UI CSS']:
                shutil.copytree(os.getcwd() + os.sep + item, floder + os.sep + item)
            os.remove(url)

        userrecorddb.saveaction2db(currentuser, u'导出所有操作记录')
        self.handlerecord()

    def setSaveFileName(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self,
                u"保存用户操作记录",
                u'用户操作记录',
                "Html Files (*.html)")
        return fileName

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    w = UserPage()
    w.show()
    sys.exit(app.exec_())
