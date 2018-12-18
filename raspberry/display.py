import RPi.GPIO as GPIO
import tm1637
import time
import trainer2
import times2
import threading


GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(4, GPIO.RISING, callback=lambda x: start_button(), bouncetime=1000)
GPIO.add_event_detect(17, GPIO.RISING, callback=lambda x: stop_button(), bouncetime=300)
GPIO.add_event_detect(27, GPIO.RISING, callback=lambda x: change_button(), bouncetime=300)

program = 0

# Setup display variables
Display = tm1637.TM1637(23,24,tm1637.BRIGHT_TYPICAL)
Display.Clear()
Display.SetBrightnes(7)

disp = [0,0,0,0]
Display.Show(disp)

def start_button():
    print("Start button")
    x = GPIO.input(4)
    print (x)
    Display.Clear()

    if program == 0 and x == 1:
        print ("Starting program: Random")
        #trainer2.main("random")
        th1 = threading.Thread(target=trainer2.main("random"))
        th1.daemon = True
        th1.start()
        #t1.join()
    elif program == 1 and x == 1:
        print ("Starting program: 5-10-5")
        #trainer2.main("program_1")
        th2 = threading.Thread(target=trainer2.main("program_1"))
        th2.daemon = True
        th2.start()
        #t2.join()
    elif program == 2 and x == 1:
        print ("Starting program: Sprint 10 meter")
        #trainer2.main("program_2")
        th3 = threading.Thread(target=trainer2.main("program_2"))
        th3.daemon = True
        th3.start()

        #t3.join()

    display_time()

def stop_button():
    print("Stop button")
    Display.Clear()

    


def change_button():
    global program
    print("Change button")
    
    program += 1

    if program > 2:
        program = 0

    disp = [0,0,0,program]
    Display.Show(disp)


def display_time():
    tid = times2.print_total_time()
    print (tid)

    t1 = int(tid[0])
    t2 = int(tid[1])
    t3 = int(tid[3])
    t4 = int(tid[4])

    display = [ t1, t2, t3, t4 ]
    Display.Show(display)
    Display.ShowDoublepoint(1)


#while True:
    #time.sleep(0.01)

    #GPIO.add_event_callback(4, start_button())
    #GPIO.add_event_callback(17, stop_button())
    #GPIO.add_event_callback(27, change_button())







