#!/usr/bin/python

"""
This script runs on a RaspberryPi, monitors the swicht and triggers SpaceAPI changes.
"""




from __future__ import print_function
from time import sleep
import arrow
import httplib
import json
import subprocess as sp
import RPi.GPIO as GPIO


# print to STDERR
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)



#===================== Exexute a shell command ====================================
def cmd_exec(cmd,args):
    cmd_str =cmd
    for arg in args:
        cmd_str += ' ' + arg
#    print('Try executing Command "'+cmd_str+'"')
    try:
        str1 = sp.check_output([cmd]+args, stderr=sp.STDOUT)
    except sp.CalledProcessError as err:
        eprint('ERROR: Execution failed\n cmd: '+str(err.cmd)+'\n output: '+str(err.output)+'\n retunrcode: '+ str(err.returncode))
        return err.returncode
#    print('SUCCESS: executed '+cmd_str)



GPIO.setmode(GPIO.BCM)

GPIO.setup(2, GPIO.IN)
GPIO.setup(3, GPIO.OUT)
GPIO.output(3, GPIO.LOW)


state = GPIO.input(2)
error = False
first_loop = True

time_var = arrow.Arrow.now()


inet_connection = httplib.HTTPSConnection('heidelberg-makerspace.de')
inet_connection.request('GET','/status.json')
response = con.getresponse()
inet_connection.close()
status_json = response.read()
# TODO: read from https://heidelberg-makerspace/status.json
#json.get('location')

longest_open = 0

while True:
    # In case of error blick with red LED
    if error:
        GPIO.output(3, GPIO.LOW)
        sleep(.5)
        GPIO.output(3, GPIO.HIGH)
        sleep(.5)
        continue
        
    
    
    sleep(1)
    new_state = GPIO.input(2)
    
    if state != new_state or first_loop:
        print("set state to: "+ str(GPIO.input(2)))
        state = new_state
        if state == 0:
            # change state to "open"
            cmd_exec('ssh',['-i','/root/.ssh/makerspace_hb_open',
                            'spaceapi@heidelberg-makerspace.de'])
            # start time messurement
            time_var = arrow.Arrow.now()
                            
        elif state ==1: 
            # calculate current presence time
            tmp = arrow.Arrow.now() - time_var            
            tmp = tmp.days*24*60*60 + tmp.secounds
            # check for new precentce time record
            if tmp > longest_open:
                longest_open = tmp
            #TODO: cange state to closed and reset precentce time record
            cmd_exec('ssh',['-i','/root/.ssh/makerspace_hb_close',
                            'spaceapi@heidelberg-makerspace.de'])
        else:
            eprint('ERROR: Invalid state '+str(state)+'\nValid states are "0" and "1"')
            error = True
    
    first_loop = False
