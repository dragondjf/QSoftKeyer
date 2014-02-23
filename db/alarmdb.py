#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import os
import logging
from dbutils import *


logger = logging.getLogger(__name__)

db_name = 'QSoftKeyer'
table_name = "alarmrecords"
db_filename = os.sep.join([os.getcwd(), '%s.db' % db_name])
db_is_new = not os.path.exists(db_filename)

alarmrecords_keys = ['status_no', 'pa_no', 'rid', 'did', 'pid', 'gno', 'name', 'status_index', 'status', 'status_zh', 'status_change_time']

# 创建alarmrecords Table
sqlcmd_create_table = "create table %s(\
            status_no int, \
            pa_no int, \
            rid int, \
            did int, \
            pid int, \
            gno text, \
            name text, \
            status_index int, \
            status text, \
            status_zh text, \
            status_change_time text \
            )" % table_name

try:
    con = sqlite3.connect(db_filename)
    cur = con.cursor()
    cur.execute(sqlcmd_create_table)
except Exception, e:
    logger.info(e)
finally:
    if con:
        con.close()


# if __name__ == '__main__':
#     sqlcmd_fiberbreak = '''select * from alarmrecords where status_index=2'''
#     sqlcmd_alarm = '''select * from alarmrecords where status_index=1'''
#     keys, types = tableinfo(db_filename, 'alarmrecords')
#     print tabel_count(db_filename, 'alarmrecords')
#     # print fetchby_fixedlength(db_filename, 'alarmrecords')
#     # print len(fetchby_sqlcmd_fixedlength(db_filename, 'alarmrecords', sqlcmd_fiberbreak, 1000))
#     # fetchby_sqlcmd_fixedlength(db_filename, 'alarmrecords', sqlcmd_alarm, 1000))
#     print keys
#     print types
