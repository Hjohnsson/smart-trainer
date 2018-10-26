#!/usr/bin/python
import MySQLdb

def db_connect():
    db = MySQLdb.connect(host="localhost",
         user = "pi",
         passwd = "herman93",
         db = "SmartTrainer")

    cur = db.cursor()
    return cur

def get_values_int(name):
    cur = db_connect()
    cur.execute("SELECT %s FROM settings" % name)
    values = cur.fetchone()[0]

    return values

def get_values_float(name):
    cur = db_connect()
    cur.execute("SELECT %s FROM settings" % name)
    values = cur.fetchone()[0]

    return values

def update_values(name,value):
    db = MySQLdb.connect(host="localhost",
         user = "pi",
         passwd = "herman93",
         db = "SmartTrainer")

    cur = db.cursor()
    cur.execute("""UPDATE settings SET %s=%d WHERE program='default'""" % (name, value))

    db.commit()
    db.close()
    return

def update_times(values):
    db = MySQLdb.connect(host="localhost",
         user = "pi",
         passwd = "herman93",
         db = "SmartTrainer")

    cur = db.cursor()
    x = 0
    for i in values[3:]:
        x += 1
        t = "T"+str(x)
        cur.execute("""UPDATE tbl_times SET %s=%s WHERE Player='Zlatan'""" % (t, i))

    db.commit()
    db.close()
    return


def get_times():
    value = [] 
    cur = db_connect()
    cur.execute("SELECT * FROM tbl_times")
    values = cur.fetchall()
    for i in values:
        for x in i: 
            value.append(x)
    return value

#get_values_int("nodes")
#get_values_int("rounds")
#get_values_int("distance")
#get_values_float("delay")


#update_values("nodes",3)
#get_values_int("nodes")


