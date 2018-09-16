#!/usr/bin/python 
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import subprocess
import time
import datetime
import random
import times2


loops = 0
total_loops = 9
num_nodes = 1
num = random.randint(1,num_nodes)

def log_split_times(state, mode):
    file = open("split_times.log",mode)
    timestamp = str(datetime.datetime.now())
    msg = "State: " + state + " " + timestamp + "\n"
    file.write(msg)
    file.close()

#def print_split_times():
    #file = open("split_times.log", "r")
    #for line in file:
        #print line,


def initiate_nodes():
    print "Start sequence initiated, starting in 5 seconds"  
    client.publish("wemos","START")
    time.sleep(7)
    print("Turning off before training starts")
    client.publish("wemos","OFF")
    #time.sleep(1)
    
 
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("wemos")
    time.sleep(1)
    print "Sending start message to: NODE %d" % num
    client.publish("wemos","NODE-%d-ON" % num)
    log_split_times("NODE-%d-ON" % num, "w")

def on_message_wemos(client, userdata, msg):
    global loops
    global num

    print(msg.topic+" "+str(msg.payload) + " received on mqtt bus")
    #print "randint: %d" % num
    #print "loops: %d" % loops

    _msg = str(msg.payload)

    if _msg == "NODE-%d-OFF" % num:
        log_split_times("NODE-%d-OFF" % num, "a")
        num = random.randint(1,num_nodes)

        time.sleep(1)

        if loops >= total_loops:
            client.disconnect()
            print "Round finished!"
            print ""
            times2.print_split_times()
            times2.print_total_time()
            exit()
        else:
            print "Sending message to: NODE %d" % num
            client.publish("wemos","NODE-%d-ON" % num)
            log_split_times("NODE-%d-ON" % num, "a")
            loops += 1


client = mqtt.Client(client_id="Main-program", clean_session=True)

client.on_connect = on_connect
client.on_message = on_message_wemos

client.connect("192.168.1.200", 1883, 60)

# Initate nodes to prepare the trainer
initiate_nodes()

client.loop_forever()
