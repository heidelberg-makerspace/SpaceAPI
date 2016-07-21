#!/usr/bin/python

"""
This script runs on a RaspberryPi, monitors the swicht and triggers SpaceAPI changes.
"""




from __future__ import print_function
from time import sleep
import sys
import subprocess as sp
import RPi.GPIO as GPIO


# print to STDERR
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)



#===================== Exexute a shell command ====================================
def cmd_exec(cmd,args,return_output=False):
    cmd_str =cmd
    for arg in args:
        cmd_str += ' ' + arg

    try:
        str1 = sp.check_output([cmd]+args, stderr=sp.STDOUT)
    except sp.CalledProcessError as err:
        eprint('ERROR: Execution of shell command "'+str(err.cmd)+'" failed!\n output: '+str(err.output)+'\n retunrcode: '+ str(err.returncode))
        if return_output:
            return err.returncode, ''
        else:
            return err.returncode
    if return_output:
        return 0, str1
    else:
        return 0



GPIO.setmode(GPIO.BCM)

GPIO.setup(2, GPIO.IN)
GPIO.setup(3, GPIO.OUT)
GPIO.output(3, GPIO.LOW)


state = GPIO.input(2)
error = False
first_loop = True


while True:
    # In case of error blick with red LED
    if error:
        GPIO.output(3, GPIO.LOW)
        sleep(.5)
        GPIO.output(3, GPIO.HIGH)
        sleep(.5)
        continue
    
    sleep(.5)
    new_state = GPIO.input(2)
    
    if state != new_state or first_loop:
        print("set state to: "+ str(GPIO.input(2)))
        state = new_state
        ssh_retry_count = 0
        ret = -1000
        if state == 0: # change state to "open"
            while ret != 0 and ssh_retry_count < 2:
                ssh_retry_count = ssh_retry_count + 1
                ret = cmd_exec('ssh',['-i','/root/.ssh/makerspace_hb_open',
                                      'spaceapi@heidelberg-makerspace.de'])
            if ret != 0:
                error = True
                eprint('ERROR: could not change the remote state')
                            
        elif state == 1: # change state to closed  
            ssh_retry_count = ssh_retry_count + 1
            while ret != 0 and ssh_retry_count < 2:          
                ret = cmd_exec('ssh',['-i','/root/.ssh/makerspace_hb_close',
                                      'spaceapi@heidelberg-makerspace.de'])
            if ret != 0:
                error = True
                eprint('ERROR: could not change the remote state')
        else:
            eprint('ERROR: Invalid state "'+str(state)+'"\nValid states are "0" and "1"')
            error = True
    
    first_loop = False
