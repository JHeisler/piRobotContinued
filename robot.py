from socketIO_client import SocketIO, LoggingNamespace
import sys
import time
from threading import Thread
from importlib import import_module
import os

socketIO = SocketIO('192.168.1.129', 8080)

# Import the PCA9685 module.
import Adafruit_PCA9685
sys.path

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

# Set frequency to 60hz
pwm.set_pwm_freq(60)

def forwards():
    print('Forwards')
    pwm.set_pwm(0,0,servo_max)
    pwm.set_pwm(1,0,servo_min)

def backwards():
    print('Backwards')
    pwm.set_pwm(0,0,servo_min)
    pwm.set_pwm(1,0,servo_max)

def left():
    print('Left')
    pwm.set_pwm(0,0,servo_min)
    pwm.set_pwm(1,0,servo_min)

def right():
    print('Right')
    pwm.set_pwm(0,0,servo_max)
    pwm.set_pwm(1,0,servo_max)

def stop():
    print('Stop')
    pwm.set_pwm(0,0,0)
    pwm.set_pwm(1,0,0)
    pwm.set_pwm(2,0,0)
    pwm.set_pwm(4,0,0)
    pwm.set_pwm(5,0,0)

def on_message(*args):
    #Retrieve the message from the args tuple
    print(args[0])
    data = args[0]

    if data == 'forward': # Forward
        forwards()
    elif data == 'left': # Left
        left()
    elif data == 'right': # Right
        right()
    elif data == 'backward': # Backward
        backwards()
    elif data == 'hopen': # Hand Open
        print('Hand Open')
        pwm.set_pwm(2,0,155)
        socketIO.wait(seconds=1)
        pwm.set_pwm(2,0,0)
    elif data == 'hclose': # Hand Close
        print('Hand Close')
        pwm.set_pwm(2,0,420)
        socketIO.wait(seconds=1)
        pwm.set_pwm(2,0,0)    
    elif data == 'stop': # Stop
        stop()
    elif data == 'panleft':
        print('Pan Left')
        pwm.set_pwm(5,0,550)
        socketIO.wait(seconds=1)
        pwm.set_pwm(5,0,0)

    elif data == 'panright':
        print('Pan Right')
        pwm.set_pwm(5,0,200)
        socketIO.wait(seconds=1)
        pwm.set_pwm(5,0,0)

    elif data == 'tup':
        print('Tilt Up')
        pwm.set_pwm(4,0,300)
        socketIO.wait(seconds=1)
        pwm.set_pwm(4,0,0)

    elif data == 'tdown':
        print('Tilt Down')
        pwm.set_pwm(4,0,700)
        socketIO.wait(seconds=1)
        pwm.set_pwm(4,0,0)

    elif data == 'center':
        print('Center')
        pwm.set_pwm(4,0,450)
        pwm.set_pwm(5,0,375)
        socketIO.wait(seconds=1)
        pwm.set_pwm(4,0,0)
        pwm.set_pwm(5,0,0)

socketIO.on('move', on_message)
socketIO.wait()
