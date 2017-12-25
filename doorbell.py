#!/usr/bin/python
import os
import signal
import subprocess
import sys
import time
import urllib2
import requests
from subprocess import call

# Ignore SIGCHLD
# This will prevent zombies
signal.signal(signal.SIGCHLD, signal.SIG_IGN)

# After ringing, how many seconds before we allow ourselves to ring again
DEBOUNCE_INTERVAL = 7

# IFTTT event name
ifttt_event_name='pepp_pizza_delivery_apt'

# IFTTT key
ifttt_key='cvHIWtdruduUcPKi2huKwh'

# IFTTT URL to call
ifttt_url='https://maker.ifttt.com/trigger/' + ifttt_event_name + '/with/key/' + ifttt_key

# The token to look for in tcpdump's output
# This should be your unique network SSID
#SSID_TOKENS = sys.argv[1] if len(sys.argv) > 1 else 'Free Public Wifi'

#This file holds a list of SSID's to look for
#each SSID is delineated by a new line
f = open("dash_ssids")
lines = f.readlines()
f.close()

SSID_TOKENS = []
for line in lines:
    SSID_TOKENS.append(line.strip())

# This file holds a list of actions to take
# NOTE: This must be in the same order as the SSID's in dash_ssids
f = open("ssid_actions")
actions = f.readlines()
f.close()

SSID_ACTIONS = []
for action in actions:
    SSID_ACTIONS.append(action.strip())

DEVNULL = open(os.devnull, 'wb')
def do_ring():
    """ Play the doorbell.wav file. Don't wait for it to finish. """
    cmd = 'alsaplayer -o alsa --quiet ./doorbell.wav'
    soundproc = subprocess.Popen(cmd.split(), close_fds=True,
                                 stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL)

cmd = 'tcpdump -l -K -q -i DoorbellMonitor -n -s 256'
proc = subprocess.Popen(cmd.split(), close_fds=True,
                        bufsize=0, stdout=subprocess.PIPE)
last_played = 0

print "List length:"
print len(SSID_TOKENS)

print "SSID_TOKENS is/are:"
for SSID_TOKEN_PRINT in SSID_TOKENS:
    print SSID_TOKEN_PRINT

while True:
    line = proc.stdout.readline()
    if not line:
        print "tcpdump exited"
        break
    for INDEX,SSID_TOKEN in enumerate(SSID_TOKENS):
        if SSID_TOKEN in line:
            now = time.time()
            if now - last_played > DEBOUNCE_INTERVAL:
		if INDEX is 0:
		    print "INDEX IS 0."
		    os.system('echo HELLO Glad!')
		    os.system('python testing_json_POST_doorbell.py')
		    os.system('echo Called python.')
		elif INDEX is 1:
		    print "INDEX IS 1."
		elif INDEX is 3:
		    print "INDEX IS 3."
		elif INDEX is 2:
		    print "INDEX IS 2."
		    print "Called IFTTT to order Domino's delivery to apt via Twitter. Result: " + requests.get(ifttt_url).text
                last_played = now
                sys.stdout.write(line)
                sys.stdout.flush()
                #do_ring()
