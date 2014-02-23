#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import os
import time
import logging
from dbutils import table_count, save2db

logger = logging.getLogger(__name__)

db_name = 'QSoftKeyer'
table_name = "userrecords"
db_filename = os.sep.join([os.getcwd(), '%s.db' % db_name])
db_is_new = not os.path.exists(db_filename)

# 创建UserRecords Table
sqlcmd_create_table = "create table %s(\
            no int, \
            level int, \
            user_name text, \
            user_role text, \
            user_action text, \
            action_time text \
            )" % table_name

try:
    con = sqlite3.connect(db_filename)
    cur = con.cursor()
    cur.execute(sqlcmd_create_table)
    con.commit()
except Exception, e:
    logger.info(e)
finally:
    if con:
        con.close()


def saveaction2db(currentuser, action):
    global table_name, db_filename
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))).decode('UTF8')
    no = table_count(db_filename, table_name) + 1
    record = (no, currentuser['level'], currentuser['user_name'], currentuser['user_role'], action, t)
    # print "99999999999999"
    # print record
    # print table_name
    # print db_filename
    # print "88888888888"
    save2db(table_name, db_filename, record)
