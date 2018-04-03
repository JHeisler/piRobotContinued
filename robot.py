from socketIO_client import SocketIO, LoggingNamespace
import sys
import time
from threading import Thread
from importlib import import_module
import os

socketIO = SocketIO('localhost', 8080, LoggingNamespace)

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
    print(args[0][14:17])
    data = args[0][14:17]

    if data == 'for': # Forward
        forwards()
    elif data == 'lef': # Left
        left()
    elif data == 'rig': # Right
        right()
    elif data == 'bac': # Backward
        backwards()
    elif data == 'hop': # Hand Open
        print('Hand Open')
        pwm.set_pwm(2,0,155)
        socketIO.wait(seconds=1)
        pwm.set_pwm(2,0,0)
    elif data == 'hcl': # Hand Close
        print('Hand Close')
        pwm.set_pwm(2,0,420)
        socketIO.wait(seconds=1)
        pwm.set_pwm(2,0,0)    
    elif data == 'sto': # Stop
        stop()
    elif data == 'plf':
        print('Pan Left')
        pwm.set_pwm(5,0,550)
        socketIO.wait(seconds=1)
        pwm.set_pwm(5,0,0)

    elif data == 'prt':
        print('Pan Right')
        pwm.set_pwm(5,0,200)
        socketIO.wait(seconds=1)
        pwm.set_pwm(5,0,0)

    elif data == 'tup':
        print('Tilt Up')
        pwm.set_pwm(4,0,300)
        socketIO.wait(seconds=1)
        pwm.set_pwm(4,0,0)

    elif data == 'tdw':
        print('Tilt Down')
        pwm.set_pwm(4,0,700)
        socketIO.wait(seconds=1)
        pwm.set_pwm(4,0,0)

    elif data == 'cen':
        print('Center')
        pwm.set_pwm(4,0,450)
        pwm.set_pwm(5,0,375)
        socketIO.wait(seconds=1)
        pwm.set_pwm(4,0,0)
        pwm.set_pwm(5,0,0)
    else: # Otherwise Stop
        stop()


def listen():
    while True:
        socketIO.on('message', on_message)
        socketIO.wait()
        socketIO.off('message')

t = Thread(target=listen)
t.start()