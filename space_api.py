# -*- coding: utf-8 -*-
"""
This Script runs on the Server and generates the SpaceAPI json file.
The run of this script is triggert by SSH.
"""



import json
import sys



def print_help():
    space_l = 40
    space_r = 40
    print '\nUsage: '
    print ('{:>'+str(space_l)+'}').format(sys.argv[0])+' '*5+'options'
    print '\n\nOptions:\n'
    print ('{:'+str(space_l)+'}').format('-s   --state')+('{:>'+str(space_r)+'}').format('[open|closed]')
    print ('{:'+str(space_l)+'}').format('-o   --outfile')+('{:>'+str(space_r)+'}').format('file (default: ./status.json)')
    exit(1)
    

outfile='status.json'

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
        'space':'Heidelberg Makerspace', 
        'logo':'https://wiki.heidelberg-makerspace.de/mediawiki/images/thumb/f/f3/Makerspace_Icon.svg/267px-Makerspace_Icon.svg.png',
        'url':'https://wiki.heidelberg-makerspace.de',
        'location':{'address':'Sofienstraße 12, 69115 Heidelberg, Germany',
                    'lon':'8.69390',
                    'lat':'49.40792'},
        'contact':{'email':'makerspace@dai-heidelberg.de',
                   'facebook':'https://www.facebook.com/heidelbergmakerspace/',
                   'twitter':'@HD_Makerspace'},
        'issue_report_channels':['email'],
        'state': {'open': str(space_is_open).lower()}
           }

if outfile==None:
    print json.dumps(data)
else:
    with open(outfile, 'w') as f:
        json.dump(data,f)
