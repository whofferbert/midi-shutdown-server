#!/usr/bin/python3
# by William Hofferbert
# Midi Shutdown Server
# creates a virtual midi device via amidithru,
# then listens for a control change message
# on that device, running a shutdown command
# via os.system when it gets that command.

import time
import mido
import os
import re

# midi device naming
name = "MidiShutdownServer"

# shutdown command
shutdown_cmd = "sudo init 0 &"

# listen for 
shutdown_cc_num = 64
shutdown_cc_val = 127

# prevent shutdown command from running unless uptime is > secs
shutdown_abort_uptime_secs = 120;

#
# Logic below
#

# set up backend
mido.set_backend('mido.backends.rtmidi')

# system command to set up the midi thru port
# TODO would be nice to do this in python, but
# rtmidi has issues seeing ports it has created
runCmd = "amidithru '" + name + "' &"
os.system(runCmd)

# regex to match on rtmidi port name convention
nameRegex = "(" + name + ":" + name + "\s+\d+:\d+)"
matcher = re.compile(nameRegex)
newList = list(filter(matcher.match, mido.get_input_names()))
input_name = newList[0]

inport = mido.open_input(input_name)

def uptime():  
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        return uptime_seconds

# keep running and watch for cmd
while True:
  time.sleep(.1)
  while inport.pending():
    msg = inport.receive()
    if msg.type == "control_change":
      if ( msg.control == shutdown_cc_num and msg.value == shutdown_cc_val ):
        if ( uptime() > shutdown_abort_uptime_secs):
          os.system(shutdown_cmd)
