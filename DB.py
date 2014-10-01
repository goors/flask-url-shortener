import MySQLdb
import appconfig


class DB:

    def __init__(self):
        self.connect()

    def connect(self):
        try:
            self.conn = MySQLdb.connect(appconfig.HOST,
                                        appconfig.USER, appconfig.PASS, appconfig.DATABASE)
        except (AttributeError, MySQLdb.OperationalError), e:
            raise e

    def query(self, sql, params=()):
        try:
            cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql, params)
        except (AttributeError, MySQLdb.OperationalError) as e:
            print 'exception generated during sql connection: ', e
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql, params)
        return cursor

    def close(self):
        try:
            if self.conn:
                self.conn.close()
            else:
                print '...No Database Connection to Close.'
        except (AttributeError, MySQLdb.OperationalError) as e:
            raise e

