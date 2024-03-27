# https://www.rohde-schwarz.com/webhelp/smb100a_html_usermanual_1/Content/2e097e6397fa40bd.htm#d79403e12303
# https://github.com/pyvisa/pyvisa-py
# pip install pyvisa-py
# pip install pyusb
# pip install psutil
# pip install zeroconf

import pyvisa
import time
import re

rm = pyvisa.ResourceManager('@py')
print(rm.list_resources('?*'))

steps = [
  ('300000', '9'),
  ('350000', '10'),
  ('400000', '11'),
  ('1000000', '-20'),
  ('1500000', '-20'),
]

rohde_schwarz_name = 'TCPIP::192.168.1.5::INSTR'
rigol_name = 'TCPIP::192.168.1.11::INSTR'

rigol = rm.open_resource(rigol_name)
print(rigol.query('*idn?'))

rohde_schwarz = rm.open_resource(rohde_schwarz_name)
idn_result = rohde_schwarz.query('*idn?')
print(idn_result)
assert re.match('Rohde&Schwarz', idn_result)

rigol = rm.open_resource(rigol_name)
idn_result = rigol.query('*idn?')
print(idn_result)
assert re.match('Rigol', idn_result)

# Comments on commands are quoted from instrument manuals.
rigol.write('*cls')
#print(rigol.write('*rst; status:preset; *cls'))
# RIGOL
# Normal marker
# It is used to measure the X (Frequency or Time) and Y (Amplitude) values of a certain point on the trace.
rigol.write('calculate:marker:mode position')
# Enables the auto trace marking of the specified marker
rigol.write('calculate:marker1:trace:auto on')
# Enables the auto readout mode of the specified marker.
# When you enable the marker's auto marking trace function, the marker shifts 
# from its off state to on state, and the marker's marking trace is automatically
# determined by the instrument.
rigol.write('calculate:marker1:x:readout:auto on')

# Sets the peak search mode.
# MAXimum: indicates maximum. If "maximum" is selected under search mode, the system will search for the maximum value on the trace.
# The command is only valid for the peak search executed by sending the :CALCulate:MARKer<n>:MAXimum[:MAX] command.
rigol.write('calculate:marker:peak:search:mode maximum')

# Sets the readout mode of the X axis of the specified marker.
# FREQuency: indicates frequency. It is the default readout mode in non-zero span mode.
rigol.write('calculate:marker1:x:readout frequency')

#rohde_schwarz.write('syst:disp:upd 1')

# Activates RF signal output.
rohde_schwarz.write('output 1')

for step in steps:
    print('Rohde&Schwarz: {0}HZ, {1}dBm'.format(step[0], step[1]))
    # Sets the center frequency. 
    rigol.write('sens:frequency:center {0}'.format(step[0]))
    # Enters the RF frequency, considering the frequency offset.
    rohde_schwarz.write('source:frequency:cw {0}Hz'.format(step[0]))
    # Enters the RF level, considering the level offset.
    rohde_schwarz.write('source:power:level:immediate:amplitude {0}dBm'.format(step[1]))
    time.sleep(0.5)
    # Performs one peak search based on the search mode set by the :CALCulate:MARKer:PEAK:SEARch:MODE
    # command and marks it with the specified marker.
    rigol.write('calculate:marker1:maximum:max')
    freq = rigol.query('calculate:marker1:x?')
    ampt = rigol.query('calculate:marker1:y?')
    print('Rigol: {0}Hz, {1}dBm'.format(freq, ampt))

    time.sleep(2)

# Deactivates RF signal output.
rohde_schwarz.write('outp 0')
rohde_schwarz.write('*rst; status:preset; *cls')
