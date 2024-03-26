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
]

rohde_schwarz_name = 'TCPIP::192.168.1.5::INSTR'
rigol_name = 'TCPIP::192.168.1.11::INSTR'
rohde_schwarz = rm.open_resource(rohde_schwarz_name)
idn_result = rohde_schwarz.query('*idn?')
print(idn_result)
assert re.match('Rohde&Schwarz', idn_result)

rigol = rm.open_resource(rigol_name)
idn_result = rigol.query('*idn?')
print(idn_result)
assert re.match('Rigol', idn_result)

rohde_schwarz.write('*rst; status:preset; *cls')
#rigol.write('status:preset')
#print(rigol.write('*rst; status:preset; *cls'))
time.sleep(5)

rohde_schwarz.write('syst:disp:upd 1')

rohde_schwarz.write('outp 1')
rigol.write('calculate:marker:peak:search:mode maximum')
for step in steps:
    print('Rohde&Schwarz: {0}HZ, {1}dBm'.format(step[0], step[1]))
    rigol.write('sens:freq:cent {0}'.format(step[0]))
    rohde_schwarz.write('freq:cw {0}Hz'.format(step[0]))
    rohde_schwarz.write('sour:pow:lev:imm:ampl {0}dBm'.format(step[1]))
    time.sleep(3)
    rigol.write('calculate:marker1:maximum:max')
    print('Rigol: {0}'.format('?'))
    print(rigol.query('calculate:marker1:fcount:x?'))
    print(rigol.query('calculate:marker1:x?'))
    print(rigol.query('calculate:marker1:y?'))
    #print(rigol.query('calc:mark:peak:sear:mode?'))
    #print(rigol.query('calc:mark:peak:exc?'))
    #print(rigol.query('calc:mark1:max?'))
    #print(rigol.query('configure?'))

    time.sleep(3)

rohde_schwarz.write('outp 0')
rohde_schwarz.write('*rst; status:preset; *cls')