#!/usr/bin/python

""" Download an IR remote signal from a Rigol DS1052E and
analyze it for a NEC protocol signal.
Ken Shirriff
http://righto.com
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import sys
import time
import visa

# Get the USB device, e.g. 'USB0::0x1AB1::0x0588::DS1ED141904883'
instruments = visa.get_instruments_list()
usb = filter(lambda x: 'USB' in x, instruments)
if len(usb) != 1:
    print 'Bad instrument list', instruments
    sys.exit(-1)
scope = visa.instrument(usb[0], timeout=20, chunk_size=1024000) # bigger timeout for long mem

# Oscilloscope can get confused if too many commands arrive too fast
def scopewrite(str):
    scope.write(str)
    time.sleep(.1)

# Reset scope
#scope.write(b"*RST")

time.sleep(4)

# Enable recording
#scopewrite(":FUNC:WREC:ENAB 1")

scopewrite(":STOP")

"""""# Start recording
scopewrite(":FUNC:WREC:OPER RUN")
time.sleep(3)
# Stop recording
scopewrite(":FUNC:WREC:OPER STOP")"""

# Choose channel
scopewrite(":WAV:SOUR CHAN1")
# Choose mode
scopewrite("WAV:MODE NORM")
# Choose format
scopewrite("WAV:FORM BYTE")

# Choose start- and stopping point
scopewrite("WAV:STAR 1")
scopewrite("WAV:STOP 1200")

scopewrite("WAV:DATA?")
result = scope.read(encoding="Latin-1")
# Get data
print ':'.join(hex(ord(x))[2:] for x in result)

data = np.frombuffer(result[12:-1], 'B')
data_compounded = [(data[i] << 8) + data[i+1] for i in range(0, len(data), 2)]
plt.plot(data_compounded)
plt.show()





