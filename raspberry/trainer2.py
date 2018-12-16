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
import display


loops = 0  # keep track of how many rounds thats been run
#total_loops = 9
#num_nodes = 3
#delay_time = 0.5

total_loops = settings2.get_values_int("rounds") - 1
num_nodes = settings2.get_values_int("nodes")
delay_time = settings2.get_values_float("delay")
distance = settings2.get_values_int("distance")
num = random.randint(1,num_nodes)

program_1_state = ""

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
    
def on_connect_random(client, userdata, flags, rc):
    """
    Program Random - Training random
    """
    global distance
    print("Connected with result code "+str(rc))
    client.subscribe("wemos")
    time.sleep(1)
    print ("Sending start message to: NODE %d" % num)
    client.publish("wemos","NODE-%d-ON;%d" % (num, distance))
    log_split_times("NODE-%d-ON" % num, "w")


def on_connect_program_1(client, userdata, flags, rc):
    """
    Program 1 - TEST 5-10-5
    """
    global program_1_state
    print("Connected with result code "+str(rc))
    client.subscribe("wemos")
    #time.sleep(0.5)
    client.publish("wemos","NODE-1-STANDBY")
    program_1_state = "step1"


def on_connect_program_2(client, userdata, flags, rc):
    """
    Program 2 - TEST 10 meter sprint
    """
    print("Connected with result code "+str(rc))

    client.subscribe("wemos")
    #time.sleep(0.5)
    client.publish("wemos","NODE-1-STANDBY")


def on_message_random(client, userdata, msg):
    """
    Program Random - Training random
    """
    global total_loops
    global loops
    global num
    global distance

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
            display.display_time()
            #exit()
            return
        else:
            print ("Sending message to: NODE %d" % num)
            client.publish("wemos","NODE-%d-ON;%d" % (num, distance))
            log_split_times("NODE-%d-ON" % num, "a")
            loops += 1

def on_message_program_1(client, userdata, msg):
    """
    Program 1 - TEST 5-10-5
    """
    global loops
    global program_1_state
    global distance

    print(msg.topic+" "+str(msg.payload) + " received on mqtt bus")
    _msg = str(msg.payload)
    print (_msg)
    x = _msg.find("b")

    if loops == 0:
        time.sleep(3)
        client.publish("wemos","NODE-1-OFF")
        client.publish("wemos","NODE-2-ON;%d" % distance)
        log_split_times("NODE-2-ON", "w")
        loops += 1

    if _msg[x+1:] == "'NODE-2-OFF'" and program_1_state=="step1":
        log_split_times("NODE-2-OFF", "a")
        client.publish("wemos","NODE-3-ON;%d" % distance)
        log_split_times("NODE-3-ON", "a")
        program_1_state = "step2"

    elif _msg[x+1:] == "'NODE-3-OFF'" and program_1_state=="step2":
        log_split_times("NODE-3-OFF", "a")
        client.publish("wemos","NODE-1-ON;%d" % distance)
        log_split_times("NODE-1-ON", "a")
        program_1_state = "step3"

    elif _msg[x+1:] == "'NODE-1-OFF'" and program_1_state=="step3":
        log_split_times("NODE-1-OFF", "a")
        client.publish("wemos","FINISHED")
        times2.print_split_times()
        times2.print_total_time()
        program_1_state = ""
        client.disconnect()
        display.display_time()
        loops = 0
        return

def on_message_program_2(client, userdata, msg):
    """
    Program 2 - TEST 10 meter sprint
    """
    global loops
    global distance

    print(msg.topic+" "+str(msg.payload) + " received on mqtt bus")
    _msg = str(msg.payload)
    print (_msg)
    x = _msg.find("b")

    if loops == 0:
        time.sleep(3)
        client.publish("wemos","NODE-1-OFF")
        client.publish("wemos","NODE-2-ON;%d" % distance)
        log_split_times("NODE-2-ON", "w")
        loops += 1


    if _msg[x+1:] == "'NODE-2-OFF'":
        log_split_times("NODE-2-OFF", "a")
        client.publish("wemos","FINISHED")
        times2.print_split_times()
        times2.print_total_time()
        client.disconnect()
        display.display_time()
        loops = 0
        return


def read_settings():
    global total_loops
    global num_nodes
    global delay_time
    global distance
    global num

    total_loops = settings2.get_values_int("rounds") - 1
    num_nodes = settings2.get_values_int("nodes")
    delay_time = settings2.get_values_float("delay")
    distance = settings2.get_values_int("distance")
    num = random.randint(1,num_nodes)

def main(program):

    # Connect to mqtt 
    client = mqtt.Client(client_id="SmartTrainer-Main", clean_session=True)

    if program == "random":      # Training random lights
        read_settings()
        client.on_connect = on_connect_random
        client.on_message = on_message_random

    elif program == "program_1": # 5-10-5 agility test
        client.on_connect = on_connect_program_1
        client.on_message = on_message_program_1

    elif program == "program_2": # 10 meter sprint test
        client.on_connect = on_connect_program_2
        client.on_message = on_message_program_2

    client.connect("localhost", 1883, 60)

    # Initate nodes to prepare the trainer
    initiate_nodes(client)
    client.loop_forever()


#if __name__ == "__main__":
#    main("program_1")

