# -*- coding: utf-8 -*-
import requests
import drivers
from time import sleep
from datetime import datetime
import RPi.GPIO as GPIO
import time
from time import gmtime, strftime
import os
import threading
import Adafruit_DHT


# LCD Display
display = drivers.Lcd()
display.lcd_display_string("Connecting...", 2)
e = (time.strftime("%m/%d    %-I:%M:%S"))
display.lcd_display_extended_string(e, 1)
# Alarm
GPIO.setmode( GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
# DHT Sensor
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4




prog_done = False
beeping = False
menu = 0
def beep():
    GPIO.output(11, True)
    sleep(0.15)
    GPIO.output(11, False)
def beepLed():
    GPIO.output(15, True)
    sleep(0.15)
    GPIO.output(15, False)
beepLed();
def getPing():
    req_buzzer = requests.get('https://beeper.manuthecoder.repl.co/status.json')
    req_buzzer = req_buzzer.json()
    # print(str(req_buzzer) + " | " + str(beeping))
    if(req_buzzer['call'] == 1):
        GPIO.output(11, True);
        GPIO.output(15, True)
        beeping = True;
    elif(req_buzzer['call'] == 0):
        GPIO.output(11, False);
        GPIO.output(15, False);
        beeping = False;
    time.sleep(2);
    # print(str(req_buzzer) + " | " + str(beeping))
def getWeather():
        r = requests.get('https://api.openweathermap.org/data/2.5/find?q=Irvine,%20California&units=imperial&appid=ac2ce56330b5f2d5d6ebd17ff2cebc1d')
        r = r.json()
def setInterval(func, sec):
    def func_wrapper():
        setInterval(func, sec)
        if(prog_done == False): func()
    t = threading.Timer(sec, func_wrapper)
    if(prog_done == False): t.start()
    return t
beeping = False
try:
    setInterval(getPing, 2)
    setInterval(getWeather, 10)
    while os.system('iwgetid') != False:
        e = (time.strftime("%m/%d    %-I:%M:%S"))
        display.lcd_display_extended_string(e, 1)
        print("No internet!")
      
    r = requests.get('https://api.openweathermap.org/data/2.5/find?q=Irvine,%20California&units=imperial&appid=ac2ce56330b5f2d5d6ebd17ff2cebc1d')
    r = r.json()
    requests.get('https://beeper.manuthecoder.repl.co/on_off.php?s=true')
    temperature = str(r['list'][0]['main']['temp'])
    
    print(temperature)
    
    beep()
    
    while True:
        e = (time.strftime("%m/%d    %-I:%M:%S"))
        display.lcd_display_extended_string(e, 1)
        if(menu == 0): display.lcd_display_string(temperature + " F           ", 2)
        if (GPIO.input(10) == GPIO.HIGH and beeping == True):
            xe = requests.get('https://beeper.manuthecoder.repl.co/acknowledge.php')
            print("Acknowledged!")
            
            time.sleep(1)
            

        elif (GPIO.input(10) == GPIO.HIGH and beeping == False):
            beep();
            x = requests.get('https://beeper.manuthecoder.repl.co/acknowledge.php')
            menu = 1
            print("Green Button was pushed!")
            sleep(.2)
            r = requests.get('https://api.openweathermap.org/data/2.5/find?q=Irvine,%20California&units=imperial&appid=ac2ce56330b5f2d5d6ebd17ff2cebc1d')
            r = r.json()
            sleep(.2)
            display.lcd_clear()
            display.lcd_display_string((r['list'][0]['weather'][0]['description']).capitalize(), 1) 
            display.lcd_display_string(str(r['list'][0]['main']['temp_min']) + " - "+ str(r['list'][0]['main']['temp_max']) + " F", 2)
            sleep(3)
            menu = 0
            display.lcd_clear()
        elif (GPIO.input(12) == GPIO.HIGH):
            beep()
            menu = 1
            res = requests.get('https://hackerdashboard.manuthecoder.repl.co/status.php')
            res = res.json();
            print("Blue Button was pushed!")
            sleep(.2)
            display.lcd_clear()
            display.lcd_display_string("Smartlist: " + ( "UP" if res['data'][0]['attributes']['status'] == "up" else "DOWN"), 1) 
            display.lcd_display_string("Music server: " + ( "UP" if res['data'][3]['attributes']['status'] == "up" else "DOWN"), 2)
            
            sleep(1)
            display.lcd_clear()
            display.lcd_display_string("Alfred: " + ( "UP" if res['data'][4]['attributes']['status'] == "up" else "DOWN"), 1) 
            display.lcd_display_string("78.31.66.142: " + ( "UP" if res['data'][5]['attributes']['status'] == "up" else "DOWN"), 2)
            
            sleep(1)
            display.lcd_clear()
            display.lcd_display_string("ChatServer1: " + ( "UP" if res['data'][6]['attributes']['status'] == "up" else "DOWN"), 1) 
            display.lcd_display_string("78.31.66.142: " + ( "UP" if res['data'][7]['attributes']['status'] == "up" else "DOWN"), 2)
            
            sleep(1)
            display.lcd_clear()
            display.lcd_display_string("EdPoll: " + ( "UP" if res['data'][8]['attributes']['status'] == "up" else "DOWN"), 1) 
            display.lcd_display_string("(end of list) ", 2)

            sleep(2)
            menu = 0
            display.lcd_clear()
            
        elif (GPIO.input(13) == GPIO.HIGH):
            beep()
            menu = 1
            res = requests.get('https://hackerdashboard.manuthecoder.repl.co/status.php')
            res = res.json();
            print("Yellow Button was pushed!")
            sleep(.2)
            display.lcd_clear()
            display.lcd_display_string("Settings", 1) 
            display.lcd_display_string("Sound     >", 2) 

            sleep(3)
            menu = 0
            display.lcd_clear()
            
except KeyboardInterrupt:
    print("Cleaning up!")
    display.lcd_clear()
    requests.get('https://beeper.manuthecoder.repl.co/on_off.php?s=false')

    prog_done = True
    GPIO.cleanup()
