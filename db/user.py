#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import os
import time
import logging
from dbutils import *

logger = logging.getLogger(__name__)

db_name = 'QSoftKeyer'
table_name = "users"
db_filename = os.sep.join([os.getcwd(), '%s.db' % db_name])
db_is_new = not os.path.exists(db_filename)

# 创建UserRecords Table
sqlcmd_create_table = "create table %s(\
            no int,\
            level int, \
            user_name text, \
            password text \
            )" % table_name

try:
    con = sqlite3.connect(db_filename)
    cur = con.cursor()
    cur.execute(sqlcmd_create_table)
    cur.execute("INSERT INTO %s VALUES (1, %d, %s, %s)" % (table_name, 1, 'admin', 'admin'))
    con.commit()
except Exception, e:
    logger.info(e)
    try:
        sql = "select * from users where level=1"
        if len(test_admin(db_filename, table_name)) == 0:
            sql = "INSERT INTO %s VALUES (1, %d, %s, %s)" % (table_name, 1, '"admin"', '"admin"')
            cur.execute(sql)
            con.commit()
    except Exception, e:
        logger.info(e)
finally:
    if con:
        con.close()

def login_db(user, password):
    sql = "select * from users where user_name='%s' and password='%s'" % (user, password);
    # print sql
    keys, types = tableinfo(db_filename, table_name)
    records = []
    con = sqlite3.connect(db_filename)
    try:
        cur = con.cursor()
        cur.execute(sql)
        for row in cur.fetchall():
            record = {}
            for i in xrange(len(row)):
                record.update({keys[i]: row[i]})
            records.append(record)
    except Exception, e:
        logger.info(e)
    finally:
        if con:
            con.close()
    if len(records) == 1:
        return records[0]['level']
    return 0


def saveaction2db(currentuser, action):
    pass
    #print action
    #global db_name, db_filename
    #t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))).decode('UTF8')
    #no = table_count(db_filename, db_name) + 1
    #record = (no, currentuser['level'], currentuser['user_name'], currentuser['password'])
    #save2db(db_name, db_filename, record)
