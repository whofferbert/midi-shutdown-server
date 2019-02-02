# midi-shutdown-server

midi_shutdown_server.py

A python script to create a midi device, and listen for control change messages to trigger shutdown.

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

*Note about sudo*

This script requires root to run, so you need to call it with sudo if you are not the root user.

To have this work on boot, you must not have sudo require a password to work.

You can achieve this by adding a new file and rule to your sudoers config. with visudo (username modep in examples):

```bash
sudo visudo -f /etc/sudoers.d/modep
```

Once in visudo, write the sudoers rule to allow your user to run sudo without a password:

```bash
modep ALL = (ALL:ALL) NOPASSWD: ALL
```

After that, you can log out and back in or reboot, and then be able to run sudo things without a password.
