import time
import sys
import threading

import device_library as dl
"""
THIS SCRIPT IS THE MAIN THREAD COMMAND SHELL THAT I WILL USE TO INTERACT WITH MY CONTROL PROGRAM

STEPS:
1. LOAD & INITIALIZE DEVICES IN MAIN THREAD
--LOOP--
2. POLL DEVICES FOR STATUS & LOCAL PARAMETERS
3. IF DATA LOGGING THEN LOG DATA
4. CHECK ALARM LOGIC
5. PERFORM CONTOL ACTIONS
--LOOP--
6. OTHER THREAD WAITS FOR INPUT

"""

isrun = True

def do_stop():
    global isrun
    isrun = False

def parseline(line):
    line = line.split()
    if not line:
        return None, None, line
    elif line[0] == '?':
        line = 'help ' + line[1:]
    elif line[0] == '!':
        if hasattr(self, 'do_shell'):
            line = 'shell ' + line[1:]
        else:
            return None, None, line
    i, n = 0, len(line)
    while i < n and line[i] in self.identchars: i = i+1
    cmd, arg = line[:i], line[i:].strip()
    return cmd, args



def handle(userinput):
    print()
    x, args = parseline(userinput)
    if x == '': print('No user input specified');
    if x == '?' or x == 'help': pass
    if x == 'stop': do_stop();
    if x == 'listdevices': pass #dl.listdevices()
    if x == 'editattr': pass #dl.editattr()
    if x == 'echo': pass #dl.echo()
    if x == 'startdevice': pass

    print()

def _printlist(list_title, mylist):
    print(str(list_title))
    for i,x in enumerate(mylist):
        print()

print("Start")

while isrun:
    handle(input('<BusNet>~$ '))