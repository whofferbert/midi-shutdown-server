# midi-shutdown-server

midi_shutdown_server.py

A python script to create a midi device, and send control change messages out through it.

```python
import time
import mido
import os
import re
```

Also requires 'amidithru'

The script creates a virtual midi device (MidiShutdownServer), and listens to it for incoming midi control change messages.

Configurably, if it receives control change 64, with a value of 127, runs the shutdown command (sudo init 0).

There is logic built-in to check /proc/uptime and make sure the system has been up for at least 120 seconds (adjustable) before it will run the shutdown command.

This was done to hopefully prevent issues where, just after boot, something immediately sends the thing a signal and shuts your stuff down.

I use this as a listener to power down a Raspberry Pi running MODEP.

Generally, add an entry to your crontab to call the script on startup:
(Make sure you set your path properly)

```bash
@reboot /usr/bin/sudo /path/to/midi_shutdown_server.py &
```
