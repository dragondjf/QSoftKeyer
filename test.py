#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from utildialog import *

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    styleoptions = {
        'title': u'登录',
        'windowicon': os.sep.join(['skin', 'images', 'bg.jpg']),
        'minsize': (400, 300),
        'size': (400, 300),
        'logo_title': u'智能光纤云终端管理平台',
        'logo_img_url': os.sep.join(['skin', 'images', 'config8.png'])
    }
    print login(styleoptions)
    sys.exit(app.exec_())
