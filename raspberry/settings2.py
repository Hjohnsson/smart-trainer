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
    #print ("%s : %d" % (name,values))

    return values

def get_values_float(name):
    cur = db_connect()
    cur.execute("SELECT %s FROM settings" % name)
    values = cur.fetchone()[0]
    #print ("%s : %f" % (name,values))

    return values

def update_values(name,value):
    db = MySQLdb.connect(host="localhost",
         user = "pi",
         passwd = "herman93",
         db = "SmartTrainer")

    cur = db.cursor()
    #print ("Updating value for %s to new value: %d" % (name, value))
    cur.execute("""UPDATE settings SET %s=%d WHERE program='default'""" % (name, value))
    #cur.execute("""UPDATE settings SET nodes=2 WHERE program='default'""")

    db.commit()
    db.close()
    return



#get_values_int("nodes")
#get_values_int("rounds")
#get_values_int("distance")
#get_values_float("delay")


#update_values("nodes",3)
#get_values_int("nodes")

