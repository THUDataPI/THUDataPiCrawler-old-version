# -*- coding: utf-8 -*-
import pymysql



class MysqlConnection:
    def __init__(self, db, host=u'localhost', port=3306, user=u'root', passwd=u'123456', charset=u'utf8'):
        self.connection = pymysql.connect(db=db, host=host, port=port, user=user, passwd=passwd, charset=charset)
        self.cur = self.connection.cursor()

    def execute_single(self, sql, args=None):
        self.cur.execute(sql, args)
        self.connection.commit()

    def execute_many(self, sql, args):
        self.cur.executemany(sql, args)
        self.connection.commit()

    def select_query(self, sql):
        result = []
        self.cur.execute(sql)
        for item in self.cur:
            result.append(item)
        return result

    def exist(self, sql):
        return self.cur.execute(sql)

    def close(self):
        self.cur.close()
        self.connection.close()

