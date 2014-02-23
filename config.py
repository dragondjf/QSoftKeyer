#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
import logging

logger = logging.getLogger(__name__)

logo_ico = os.sep.join([os.getcwd(), 'skin', 'images', 'logo3.png'])
logo_img_url = os.sep.join([os.getcwd(), 'skin', 'images', 'ov-orange-green.png'])
logo_title = u''

try:
    with open(os.sep.join([os.getcwd(), 'options', 'windowsoptions.json']), 'r') as f:
        windowsoptions = json.load(f)
        logger.info('Load windowsoptions from file')
except Exception, e:
    logger.exception(e)
    logger.info('Load windowsoptions from local')
    windowsoptions = {
        'login_window': {
                'title': u'登陆',
                'windowicon': logo_ico,
                'minsize': (400, 300),
                'size': (400, 300),
                'logo_title': logo_title,
                'logo_img_url': logo_img_url
            },
        'webseverlogin_window': {
                'title': u'WebService登陆',
                'windowicon': logo_ico,
                'minsize': (400, 300),
                'size': (400, 300),
                'logo_title': u'加载来自WebService的防区',
                'logo_img_url': logo_img_url
            },
        'mainwindow': {
                'title': logo_title,
                'postion': (300, 300),
                'minsize': (800, 600),
                'size': (800, 600),
                'windowicon': logo_ico,
                'fullscreenflag': True,
                'centralwindow': {
                    'page_tag': [['Monitor', 'Alarm', 'User', 'About', 'Login']],
                    'page_tag_zh': {
                        'Monitor': u'监控管理(Monitor)',
                        'Alarm': u'告警管理(Alarm)',
                        'User': u'用户操作管理(User)',
                        # 'Waveform': u'波形管理(Waveform)',
                        # 'System': u'系统管理(System)',
                        # 'Help': u'帮助(Help)',
                        'About': u'关于(About)',
                        'Login': u'login',
                        # 'Add': u''
                    }
                },
                'statusbar': {
                    'initmessage': u'Ready',
                    'minimumHeight': 30,
                    'visual': False
                },
                'navigation_show': True
            },
        'exitdialog': {
            'title': u'登陆',
            'windowicon': logo_ico,
            'minsize': (400, 300),
            'size': (400, 300),
            'logo_title': logo_title,
            'logo_img_url': logo_img_url
        },
        'adddcdialog': {
            'title': u'增加采集器',
            'windowicon': logo_ico,
            'minsize': (400, 300),
            'size': (400, 300),
            'logo_title': logo_title,
            'logo_img_url': logo_img_url
        },
        'msgdialog': {
            'title': u'消息提示',
            'windowicon': logo_ico,
            'minsize': (400, 300),
            'size': (400, 300),
            'logo_title': logo_title,
            'logo_img_url': logo_img_url
        },
        'confirmdialog': {
            'title': u'消息提示',
            'windowicon': logo_ico,
            'minsize': (400, 300),
            'size': (400, 300),
            'logo_title': logo_title,
            'logo_img_url': logo_img_url
        },
        'urldialog': {
            'title': u'输入访问的url',
            'windowicon': logo_ico,
            'minsize': (400, 300),
            'size': (400, 300),
            'logo_title': logo_title,
            'logo_img_url': logo_img_url
        },
        'ipaddressdialog': {
            'title': u'输入访问的url',
            'windowicon': logo_ico,
            'minsize': (400, 300),
            'size': (400, 300),
            'logo_title': logo_title,
            'logo_img_url': logo_img_url
        },
        'numinputdialog': {
            'title': u'输入整数',
            'windowicon': logo_ico,
            'minsize': (400, 300),
            'size': (400, 300),
            'logo_title': logo_title,
            'logo_img_url': logo_img_url
        },
        'splashimg': os.sep.join([os.getcwd(), 'skin', 'images', 'splash.png']),
        'monitorpage': {
            'backgroundimg': logo_img_url
        },
        'maxpanum': 128,
        'panum': 6,
        'status_islog': False
    }
