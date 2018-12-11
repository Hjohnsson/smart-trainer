#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import datetime as dt

def print_split_times():
    line_num = 0
    split = []
    file = open("/home/pi/smart-trainer/raspberry/split_times.log", "r")
    for line in file:
        if line_num%2 ==0:
            #print line,
            #print line_num
        
            f = open("/home/pi/smart-trainer/raspberry/split_times.log", "r") 
            lines = f.readlines()
            line1 = lines[line_num][28:40]
            line2 = lines[line_num+1][29:41]
        
            start_dt = dt.datetime.strptime(line1, '%H:%M:%S.%f')
            end_dt = dt.datetime.strptime(line2, '%H:%M:%S.%f')
            diff = (end_dt - start_dt)
            diff.seconds/60

            #print diff
            #print ("Tid: " + str(diff)[5:])
            split.append(str(diff)[5:])

            f.close()


        line_num += 1

    file.close()
    return split

#print_split_times()


def print_total_time():
    # Beräkning av totaltid, beräknar tiden från första "ON" till sista "OFF".
    #
    num_lines = sum(1 for line in open('/home/pi/smart-trainer/raspberry/split_times.log'))

    f = open("/home/pi/smart-trainer/raspberry/split_times.log", "r")
    lines = f.readlines()
    line1 = lines[0][28:40]
    line2 = lines[num_lines -1][29:41]

    start_dt = dt.datetime.strptime(line1, '%H:%M:%S.%f')
    end_dt = dt.datetime.strptime(line2, '%H:%M:%S.%f')
    diff = (end_dt - start_dt)
    diff.seconds/60
    #print ("Total tid: " + str(diff)[5:])

    # Alternativ beräkning av totaltid
    #
    #x = diff - dt.timedelta(seconds=10)
    #print "Total tid: " + str(x)[5:]
    return str(diff)[5:]
    f.close()



#print_total_time()

