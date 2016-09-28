import MySQLdb


class mysql:
    def __init__(self):
        try:
            self.conn = MySQLdb.connect(host='115.159.122.133', user='root', passwd='802329')
            self.cursor = self.conn.cursor()
            try:
                self.cursor.execute("""create database if not exists torrent""")
            except MySQLdb.Error, e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            self.cursor.execute("""use torrent""")
            self.cursor.execute("""use torrent""")
            self.cursor.execute(
                """create table if not exists to_tb(id bigint not null primary key auto_increment, magnet varchar(50) not null)""")

            self.conn.commit()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def add_data(self, infohash):
        try:
            self.cursor.execute("""insert into to_tb (magnet) values ('magnet:?xt = urn:btih:%s')""" % infohash)

            self.conn.commit()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def close_sql(self):
        self.cursor.close()
        self.conn.close()
