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
    #print ("updating split times")
    #print (values)
    db = MySQLdb.connect(host="localhost",
         user = "pi",
         passwd = "herman93",
         db = "SmartTrainer")

    cur = db.cursor()

    x = 0
    for i in range(19):
        x += 1
        t = "T"+str(x)
        cur.execute("""UPDATE tbl_times SET %s=%s WHERE Player='Zlatan'""" % (t, 0))

    x = 0
    #for i in values[3:]:
    for i in values:
        x += 1
        t = "T"+str(x)
        cur.execute("""UPDATE tbl_times SET %s=%s WHERE Player='Zlatan'""" % (t, i))

    db.commit()
    db.close()
    return

def get_rows():
    value = []
    cur = db_connect()
    cur.execute("SELECT * FROM tbl_5105_highscore ORDER by TotalTime LIMIT 20")
    values = cur.fetchall()
    for i in values:
        value.append(i)

    return value

def update_score(name,totaltime,t1,t2,t3):
    db = MySQLdb.connect(host="localhost",
         user = "pi",
         passwd = "herman93",
         db = "SmartTrainer")

    cur = db.cursor()
    cur.execute("""INSERT INTO tbl_5105_highscore (PlayerName,TotalTime,Time_1,Time_2,Time_3) VALUES ('%s',%s,%s,%s,%s)""" % (name,totaltime,t1,t2,t3))

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


#update_score('asd',20.0,3.0,4.0,3.0)

#fetch = get_rows()

#for i in range(len(fetch)):
        #for x in range(7):
                #print (fetch[i][x])

