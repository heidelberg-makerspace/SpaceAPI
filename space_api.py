#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This Script runs on the Server and generates the SpaceAPI json file.
The run of this script is triggert by SSH.
"""


from __future__ import print_function
import json
import sys
import time

# print to STDERR
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def print_help():
    space_l = 40
    space_r = 40
    eprint( '\nUsage: ')
    eprint( ('{:>'+str(space_l)+'}').format(sys.argv[0])+' '*5+'options')
    eprint( '\n\nOptions:\n')
    eprint( ('{:'+str(space_l)+'}').format('-s   --state')+('{:>'+str(space_r)+'}').format('[open|closed]'))
    eprint( ('{:'+str(space_l)+'}').format('-o   --outfile')+('{:>'+str(space_r)+'}').format('file (default: ./status.json)'))
    exit(1)
    

outfile='dai-status.json'

if len(sys.argv) < 3:
    print_help()


for i in range(1,len(sys.argv)-1):
    if sys.argv[i]=='-s' or sys.argv[i]=='--state':
        if sys.argv[i+1] == 'open':
            space_is_open = True
        elif sys.argv[i+1] == 'closed':
            space_is_open = False
        else:
            print_help()
            
    elif sys.argv[i]=='-o' or sys.argv[i]=='--outfile':
        if sys.argv[i+1] == '-':
            outfile = None
        else:
            outfile = sys.argv[i+1]

try:
    space_is_open
except NameError:
    print_help()          
        

data = {'api':'0.13',
        'space':'DAI Makerspace', 
        'logo':'https://www.i-share-economy.org/kos/picture-cache/679/pic-factory/0_225_500_300_dim_not-set_pics_-1000177710_no_crop.jpg',
        'url':'https://dai-heidelberg.de/de/bibliothek-usa-information/makerspace/',
        'location':{'address':'Sofienstraße 12, 69115 Heidelberg, Germany',
                    'lon':8.69390,
                    'lat':49.40792},
        'contact':{'email':'makerspace@dai-heidelberg.de',
                   'facebook':'https://www.facebook.com/daimakerspace/'},
        'issue_report_channels':['email'],
        'state': {'open': space_is_open, 'lastchange': int(time.time())}
        }

if outfile==None:
    print( json.dumps(data) )
else:
    with open(outfile, 'w') as f:
        json.dump(data,f)
