#!/usr/bin/python 
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import subprocess
import time
import datetime
import random
import times2
import settings2
import threading


loops = 0  # keep track of how many rounds thats been run
#total_loops = 9
#num_nodes = 3
#delay_time = 0.5

total_loops = settings2.get_values_int("rounds") - 1
num_nodes = settings2.get_values_int("nodes")
delay_time = settings2.get_values_float("delay")
num = random.randint(1,num_nodes)

def log_split_times(state, mode):
    file = open("/home/pi/smart-trainer/raspberry/split_times.log",mode)
    timestamp = str(datetime.datetime.now())
    msg = "State: " + state + " " + timestamp + "\n"
    file.write(msg)
    file.close()

def initiate_nodes(client):
    print ("Start sequence initiated, starting in 5 seconds") 
    client.publish("wemos","START")
    time.sleep(7)
    print("Turning off before training starts")
    client.publish("wemos","OFF")
    #time.sleep(1)
    
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("wemos")
    time.sleep(1)
    print ("Sending start message to: NODE %d" % num)
    client.publish("wemos","NODE-%d-ON" % num)
    log_split_times("NODE-%d-ON" % num, "w")

def on_message_wemos(client, userdata, msg):
    global total_loops
    global loops
    global num

    print(msg.topic+" "+str(msg.payload) + " received on mqtt bus")
    #print "randint: %d" % num
    #print "loops: %d" % loops

    _msg = str(msg.payload)
    print (_msg)
    x = _msg.find("b")


    #if _msg == "NODE-%d-OFF" % num:
    if _msg[x+1:] == "'NODE-%d-OFF'" % num:
        log_split_times("NODE-%d-OFF" % num, "a")
        num = random.randint(1,num_nodes)

        time.sleep(delay_time/1000)

        if loops >= total_loops:
            print ("")
            print ("Round finished!")
            client.publish("wemos","FINISHED")
            print ("")
            times2.print_split_times()
            times2.print_total_time()
            loops = 0
            client.disconnect()
            #exit()
            return
        else:
            print ("Sending message to: NODE %d" % num)
            client.publish("wemos","NODE-%d-ON" % num)
            log_split_times("NODE-%d-ON" % num, "a")
            loops += 1


def read_settings():
    global total_loops
    global num_nodes
    global delay_time
    global num

    total_loops = settings2.get_values_int("rounds") - 1
    num_nodes = settings2.get_values_int("nodes")
    delay_time = settings2.get_values_float("delay")
    num = random.randint(1,num_nodes)

def main():
    #total_loops = settings2.get_values_int("rounds") - 1
    #num_nodes = settings2.get_values_int("nodes")
    #delay_time = settings2.get_values_float("delay")
    #num = random.randint(1,num_nodes)
    read_settings()

    client = mqtt.Client(client_id="Main-program", clean_session=True)

    client.on_connect = on_connect
    client.on_message = on_message_wemos
    client.connect("localhost", 1883, 60)

    # Initate nodes to prepare the trainer
    initiate_nodes(client)

    client.loop_forever()


#if __name__ == "__main__":
#    main()


