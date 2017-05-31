#!/usr/bin/python

"""
This script runs on a RaspberryPi, monitors the switch and triggers SpaceAPI changes.
"""




from __future__ import print_function
from time import sleep
import sys
import httplib
import json
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


print('setup GPIO')

GPIO.setmode(GPIO.BCM)

GPIO.setup(2, GPIO.IN) # Pin for Monitoring
GPIO.setup(3, GPIO.OUT) # Status LED
GPIO.output(3, GPIO.LOW)

print('setup GPIO: DONE')

error = False



# Block till network is online
# ping google and blinck with status LED

inet_connected = False
while not inet_connected:
    print('test online status')
    if cmd_exec('ping',['-c','1','-W','1','google.com']) == 0:
        inet_connected = True
        print('online status: connected to the internet')
    else:
        print('online status: offline')
        for i in range(5):
            GPIO.output(3, GPIO.HIGH)
            sleep(.2)
            GPIO.output(3, GPIO.LOW)
            sleep(.2)     


# try to get old state from community website (https://heidelberg-makerspace.de/dai-status.json)
print('get old opening state')
for i in range(3):
    try:
        inet_connection = httplib.HTTPSConnection('www.heidelberg-makerspace.de')
        inet_connection.request('GET','/dai-status.json')
        response = inet_connection.getresponse()
        status_json = response.read()
        inet_connection.close()
        print('attempt',i,': got old opening state')
    except: 
        print('attempt',i,': failed to get old opening state')
        for i in range(3):
            GPIO.output(3, GPIO.HIGH)
            sleep(.4)
            GPIO.output(3, GPIO.LOW)
            sleep(.2)      
        continue
    break

# Try to extract old opening state
print('extracting opnening state')
try:
    status_dict = json.loads(status_json)
    if status_dict['state']['open']:
        state = 0
        print('opnening state: OPEN')
    else:
        state = 1
        print('opnening state: CLOSED')
except:
    state = 10
    print('extracting opnening state FAILED')


:laughing:#
# MONITORING LOOP FOR THE LEVER
#
print('starting monitoring loop')
while True:
    # In case of error blick with red LED
    if error:
        GPIO.output(3, GPIO.HIGH)
        sleep(.5)
        GPIO.output(3, GPIO.LOW)
        sleep(.5)
        continue
    
    sleep(.5)
    new_state = GPIO.input(2)
    
    if state != new_state:
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
                ssh_retry_count = ssh_retry_count + 1
                ret = cmd_exec('ssh',['-i','/root/.ssh/makerspace_hb_close',
                                      'spaceapi@heidelberg-makerspace.de'])
            if ret != 0:
                error = True
                eprint('ERROR: could not change the remote state')
        else:
            eprint('ERROR: Invalid state "'+str(state)+'"\nValid states are "0" and "1"')
            error = True
    
