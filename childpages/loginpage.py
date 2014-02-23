#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
import PyQt4.QtNetwork
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import QtNetwork
from PyQt4 import QtWebKit
from basepage import BasePage
from Cheetah.Template import Template
from db.dbutils import *
from db.user import *
from db import user
from utildialog import confirm
from settings import currentuser
from PyQt4.QtCore import QObject, pyqtProperty
import utildialog
from config import windowsoptions


templateDef_super = '''
#set $csspath = $os.sep.join([$os.getcwd(), 'Bootstrap Metro UI CSS'])
#set $jspath = $os.sep.join([$os.getcwd(), 'js'])
#set $modern_css=$os.sep.join([$csspath, 'modern.css'])
#set $modern_responsive_css=$os.sep.join([$csspath, 'modern-responsive.css'])
#set $site_css=$os.sep.join([$csspath, 'site.css'])
#set $prettify_css=$os.sep.join([$csspath, 'prettify.css'])
#set $jquery=$os.sep.join([$jspath, 'jquery-1.10.2.min.js'])

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
    <script type="text/javascript" src="file:///$jquery"></script>
    <title>$title</title>
    <body class="modern-ui" onload="softKey.addEditBtn();">
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
                                    <tr>
                                    <td class="text-center" style="height: 25px">$record['no']</td>
                                    <td class="text-center user_name">$record['user_name']</td>
                                    <td class="text-center">$record['role']</td>
                                    <td class="text-center">$record['password']</td>
                                    <td class="text-center"><button class="DelButton">$record['del']</button></td>
                                    <td class="text-center"><button class="EditButton">$record['edit']</button></td>
                                    </tr>
                                #end for
                            </tbody>

                            <tfoot></tfoot>
                        </table>
                        <div id="addrecordpanel" style="display: none;">
                            <label>&nbsp;&nbsp;user:</label><input type="text" class="record"><br/>
                            <label>passwd:</label><input type="text" class="record"><br/>
                            <button id="add">添加</button>
                            <button id="cancel">取消添加</button>
                        </div>
                        <button id="addrecord">添加新用户</button>
                    </div>
                </div>
            </div>
        </div>
    </body>
</html>
<script>
var softKey={
    addEditBtn:function(){
        \$('#cancel').click(softKey.hideClick);
        \$('.EditButton').click(softKey.onEditBtnClick);
        \$('.DelButton').click(softKey.onDelBtnClick);
        \$('#addrecord').click(softKey.onAddBtnClick);
        \$('#add').click(softKey.addRecord);
    },
    onEditBtnClick:function(){
        if(\$(this).text()=='编辑'){
            var trTag=\$(this).parent().parent()[0],
                tdTag=\$(trTag).children()[3],
                value=\$(tdTag).text();
            \$(tdTag).text('');
            \$(tdTag).append('<input type="text" value='+value+'>');
            \$(this).text('提交');
        }else if(\$(this).text()=='提交'){
            var trTag=\$(this).parent().parent()[0],
                tdTag=\$(trTag).children()[1],
                name=\$(tdTag).text(),
                tdTag=\$(trTag).children()[2],
                role=\$(tdTag).text(),
                tdTag=\$(trTag).children()[3],
                passwd=\$(tdTag).children('input')[0].value;
            passwd = \$.trim(passwd)
            if(passwd == "")
             {
                alert("密码不能为空");
                return;
             }
            \$(\$(tdTag).children('input')).remove();
            \$(tdTag).text(passwd);
            \$(this).text('编辑');
            python.edit(name + "|" + passwd + "|" + role)
        }
    },
    onDelBtnClick:function(){
        var trTag=\$(this).parent().parent()[0],
                tdTag=\$(trTag).children()[1],
                name=\$(tdTag).text(),
                tdTag=\$(trTag).children()[2],
                role=\$(tdTag).text();
        if(role.length > 4){
            return 
        }
        \$(trTag).remove();
        python.delete(name)
    },
    onAddBtnClick:function(){
        \$('#addrecordpanel').show();
        \$('#addrecord').hide();
    },
    addRecord:function(){
        var i=0, j=0;
        var users = [];
        var users_length = \$(".user_name").length + 1,
            trTags='<tr><td align="center">' + users_length + '</td>';
        for(j=0; j< \$(".user_name").length; j++)
        {
            users.push(\$(".user_name")[j].innerHTML);            
        }
        inputs=\$('.record');
        for(i;i<inputs.length;i++){
            if(i == 0){
            trTags += '<td class="user_name" align="center">'+inputs[i].value+'</td><td align="center">值班员</td>';
            }else{
            trTags += '<td align="center">'+inputs[i].value+'</td>';
            }
        }
        trTags+='<td align="center"><button class="DelButton">删除</button></td><td align="center"><button class="EditButton">编辑</button></td></tr>';
        userr_name = \$.trim(inputs[0].value)
        passwd = \$.trim(inputs[1].value)
        if(passwd == "" || userr_name == "")
        {
            alert("用户名或密码不能为空");
            return;
        }
        if (users.indexOf(userr_name) != -1)
        {
            alert("用户名已经存在，请输入新的用户名");
            return;
        }
        \$('tbody').append(trTags);
        \$('.EditButton').click(softKey.onEditBtnClick);
        \$('.DelButton').click(softKey.onDelBtnClick);  
        \$('#addrecordpanel').hide();
        \$('#addrecord').show();
        python.add(userr_name + "|" + passwd)
    },
    hideClick:function(){
        \$('#addrecordpanel').hide();
        \$('#addrecord').show();
    }
}
</script>
'''

templateDef_user='''
<h1>普通用户没有查看修改权限</h1>
'''

class PythonJS(QObject):
    '''''供js调用'''  
    __pyqtSignals__ = ("contentChanged(const QString &)")   
    
    def __init__(self):
        super(PythonJS, self).__init__()
        self.users = check_user(db_filename, table_name)

    @pyqtSignature("QString")
    def edit(self, ed):
        name  = ed.split("|")[0]
        passwd = ed.split("|")[1]
        role = ed.split("|")[2]
        role_num = 2
        no = query_user(db_filename, table_name, name)[0][u"no"]
        if role == u"超级管理员":
            role_num = 1
            no = 1
        update2db(table_name, db_filename, (no, role_num, str(name), str(passwd)))

    @pyqtSignature("QString")
    def add(self, addstr):
        name  = addstr.split("|")[0]
        passwd = addstr.split("|")[1]
        no = table_count(db_filename, table_name) + 1
        save2db(table_name, db_filename, (no, 2, str(name), str(passwd)))
        self.users = check_user(db_filename, table_name)

    @pyqtSignature("QString")  
    def delete(self, name):
        del2db(table_name, db_filename, name)

    @pyqtSignature("QString")
    def getusers(self):
        self.users = check_user(db_filename, table_name)
        return self.users



class WebkitBasePage(QtGui.QWidget):
    def __init__(self, parent=None):
        super(WebkitBasePage, self).__init__(parent)
        self.parent = parent
        QtNetwork.QNetworkProxyFactory.setUseSystemConfiguration(True)
        QtWebKit.QWebSettings.globalSettings().setAttribute(
            QtWebKit.QWebSettings.PluginsEnabled, True)

        self.view = QtWebKit.QWebView(self)
        self.view.setFocus()

        self.setupInspector()
        self.splitter = QtGui.QSplitter(self)
        self.splitter.setOrientation(QtCore.Qt.Vertical)

        self.splitter.addWidget(self.view)
        self.splitter.addWidget(self.webInspector)

        mainlayout = QtGui.QVBoxLayout(self)
        mainlayout.addWidget(self.splitter)
        self.setLayout(mainlayout)
        self.layout().setContentsMargins(0, 0, 0, 0)

    def setupInspector(self):
        page = self.view.page()
        page.settings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
        self.webInspector = QtWebKit.QWebInspector(self)
        self.webInspector.setPage(page)

        shortcut = QtGui.QShortcut(self)
        shortcut.setKey(QtCore.Qt.Key_F11)
        shortcut.activated.connect(self.toggleInspector)
        self.webInspector.setVisible(False)

    def toggleInspector(self):
        self.webInspector.setVisible(not self.webInspector.isVisible())


class LoginPage(WebkitBasePage):
    def __init__(self, parent=None):
        super(LoginPage, self).__init__(parent)
        # 供js调用的python对象  
        pjs = PythonJS()
        # 绑定通信对象  
        self.view.page().mainFrame().addToJavaScriptWindowObject( "python" , pjs)   
        QObject.connect(pjs , SIGNAL("contentChanged(const QString &)"), self.showMessage)

        QtNetwork.QNetworkProxyFactory.setUseSystemConfiguration(True)
        self.loadfromdb()
        self.show()

    def auto_html_super(self, recordlist, template):
        nameSpace = {
            'title': "用户操作记录列表",
            'headers': [u'编号', u'用户名', u'用户角色', u'用户密码', u'删除用户', u'编辑用户'],
            'recordlist': recordlist
        }
        t = Template(template, searchList=[nameSpace])
        html = unicode(t)
        return html

    def auto_html(self, template):
        t = Template(template, searchList=None)
        html = unicode(t)
        return html

    def loadfromdb(self):
        # print currentuser
        
        if currentuser['level'] == 1:
            self.currentindex = 0
            items = self.pagination()
            if items:
                html = self.auto_html_super(items, templateDef_super)
                self.view.setHtml(html, QtCore.QUrl(os.getcwd()))
        else:
            html = self.auto_html(templateDef_user)
            self.view.setHtml(html, QtCore.QUrl(os.getcwd()))

    def pagination(self):
        items = fetchby_all(user.db_filename, user.table_name)
        recordlist = []
        for it in items:    
            it['edit'] = u'编辑'
            it['del'] = u'删除'
            if it['level'] == 1:
                it['role'] = u'超级管理员'
            else:
                it['role'] = u'值班员'
            recordlist.append(it)
        return recordlist

    def showMessage(self, msg):   
        # print "hello" * 1000
        pass
