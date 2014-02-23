#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import os
import logging

logger = logging.getLogger(__name__)


def readData(sql_filename):
    with open(sql_filename, 'r') as f:
        data = f.read()
        return data


def writeData(sql_filename, data):
    with open(sql_filename, 'w') as f:
        f.write(data)


def tableinfo(db_filename, tablename):
    keys = []
    types = []
    con = sqlite3.connect(db_filename)
    try:
        cur = con.cursor()
        cur.execute("PRAGMA table_info([%s])" % (tablename))
        for item in cur.fetchall():
            keys.append(item[1])
            types.append(item[2])
    except Exception, e:
        logger.info(e)
    finally:
        if con:
            con.close()
    return keys, types


def table_count(db_filename, tablename):
    con = sqlite3.connect(db_filename)
    try:
        cur = con.cursor()
        cur.execute("select * from %s" % (tablename))
        count = len(cur.fetchall())
    except Exception, e:
        logger.info(e)
    finally:
        if con:
            con.close()
    return count


def save2db(table_name, db_filename, record):
    try:
        con = sqlite3.connect(db_filename)
        con.text_factory = str
        cur = con.cursor()
        sql = ("INSERT INTO %s VALUES (%s)" % (table_name, ','.join([' ?'] * len(record))), record)
        # print sql
        cur.execute("INSERT INTO %s VALUES (%s)" % (table_name, ','.join([' ?'] * len(record))), record)
        con.commit()
    except Exception, e:
        logger.info(e)
    finally:
        if con:
            con.close()


def del2db(table_name, db_filename, name):
    try:
        con = sqlite3.connect(db_filename)
        con.text_factory = str
        cur = con.cursor()
        sql = 'DELETE FROM %s WHERE user_name="%s"' % (table_name, name)
        cur.execute(sql)
        # print sql
        con.commit()
    except Exception, e:
        logger.info(e)
    finally:
        if con:
            con.close()


def update2db(table_name, db_filename, record):
    del2db(table_name, db_filename, record[2])
    save2db(table_name, db_filename, record)


def delete_all(db_filename, tablename):
    flag = False
    con = sqlite3.connect(db_filename)
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM %s" % (tablename))
        con.commit()
        flag = True
    except Exception, e:
        logger.info(e)
    finally:
        if con:
            con.close()
    return flag


def fetchby_all(db_filename, tablename):
    keys, types = tableinfo(db_filename, tablename)
    records = []
    con = sqlite3.connect(db_filename)
    try:
        cur = con.cursor()
        cur.execute("select * from %s" % (tablename))
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
    return records


def test_admin(db_filename, tablename):
    keys, types = tableinfo(db_filename, tablename)
    records = []
    con = sqlite3.connect(db_filename)
    try:
        cur = con.cursor()
        cur.execute("select * from %s where level=1" % (tablename))
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
    return records


def check_user(db_filename, tablename):
    keys, types = tableinfo(db_filename, tablename)
    records = []
    con = sqlite3.connect(db_filename)
    try:
        cur = con.cursor()
        cur.execute("select * from %s where level=2" % (tablename))
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
    return records

def query_user(db_filename, tablename, user_name):
    keys, types = tableinfo(db_filename, tablename)
    records = []
    con = sqlite3.connect(db_filename)
    try:
        cur = con.cursor()
        cur.execute('select * from %s where user_name="%s"' % (tablename, user_name))
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
    return records


def fetchby_fixedlength(db_filename, tablename, length=20):
    keys, types = tableinfo(db_filename, tablename)
    records = []
    con = sqlite3.connect(db_filename)
    try:
        cur = con.cursor()
        cur.execute("select * from %s" % (tablename))
        for row in cur.fetchmany(length):
            record = {}
            for i in xrange(len(row)):
                record.update({keys[i]: row[i]})
            records.append(record)
    except Exception, e:
        logger.info(e)
    finally:
        if con:
            con.close()
    return records


def fetchby_sqlcmd_fixedlength(db_filename, tablename, sqlcmd, length=20):
    keys, types = tableinfo(db_filename, tablename)
    records = []
    con = sqlite3.connect(db_filename)
    try:
        cur = con.cursor()
        cur.execute(sqlcmd)
        for row in cur.fetchmany(length):
            record = {}
            for i in xrange(len(row)):
                record.update({keys[i]: row[i]})
            records.append(record)
    except Exception, e:
        logger.info(e)
    finally:
        if con:
            con.close()
    return records


if __name__ == '__main__':
    db_filename = "D:\sw\\trunk\\QSoftKeyer\\QSoftKeyer.db"
    table_name = "users"
    print tableinfo(db_filename, table_name)
    print fetchby_all(db_filename, table_name)
    print check_user(db_filename, table_name)
    print query_user(db_filename, table_name, 'admin1')
