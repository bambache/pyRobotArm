import os
import serial
import time
import threading
import sys
from bottle import route, run, template

servo_positions = [90,90,90,90,90];

PORT = "loop://logging=debug"
#PORT = "/dev/ttyACM0"
TIMEOUT = 1

@route('/:val')
@route('/hello/:val')
def hello(val=1):
    return template('sliders', values=servo_positions)


host=os.environ['IP']
port=os.environ['PORT']
run(host=host, port=port)
