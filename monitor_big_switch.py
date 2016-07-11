#!/usr/bin/python

"""
This script runs on a RaspberryPi, monitors the swicht and triggers SpaceAPI changes.
"""




from __future__ import print_function
from time import sleep
import subprocess as sp
import RPi.GPIO as GPIO

#===================== Exexute a shell command ====================================
def cmd_exec(cmd,args):
    cmd_str =cmd
    for arg in args:
        cmd_str += ' ' + arg
#    print('Try executing Command "'+cmd_str+'"')
    try:
        str1 = sp.check_output([cmd]+args, stderr=sp.STDOUT)
    except sp.CalledProcessError as err:
        print('ERROR: Execution failed\n cmd: '+str(err.cmd)+'\n output: '+str(err.output)+'\n retunrcode: '+ str(err.returncode))
        return err.returncode
#    print('SUCCESS: executed '+cmd_str)



GPIO.setmode(GPIO.BCM)

GPIO.setup(2, GPIO.IN)
GPIO.setup(3, GPIO.OUT)
GPIO.output(3, GPIO.LOW)


state = GPIO.input(2)
error = False

while True:
    if error:
        GPIO.output(3, GPIO.LOW)
        sleep(1)
        GPIO.output(3, GPIO.HIGH)
        sleep(1)
        continue
        
    
    
    sleep(1)
    new_state = GPIO.input(2)
    if state != new_state:
        print("set state to: "+ str(GPIO.input(2)))
        state = new_state
        if state == 1:
            cmd_exec('ssh',['-i','/root/.ssh/makerspace_hb_open',
                            'spaceapi@heidelberg-makerspace.de'])
        elif state ==0: 
            cmd_exec('ssh',['-i','/root/.ssh/makerspace_hb_close',
                            'spaceapi@heidelberg-makerspace.de'])
        else:
            print('ERROR: Invalid state '+str(state)+'\nValid states are "0" and "1"')
            error = True
        
