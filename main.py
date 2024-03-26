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

steps = [
  ('300000', '8dBm'),
  ('350000', '9dBm'),
  ('400000', '10dBm'),
]

print(rm.list_resources('?*'))
rohde_schwarz_name = 'TCPIP::192.168.1.5::INSTR'
rigol_name = 'TCPIP::192.168.1.11::INSTR'
rohde_schwarz = rm.open_resource(rohde_schwarz_name)
# instr.read_termination = '\n'
# instr.write_termination = '\n'
# instr.baud_rate = 9600
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
rigol.write('cal:mark:peak:sear:mode max')

print('Start')
for step in steps:
    rohde_schwarz.write('freq:cw {0}Hz'.format(step[0]))
    rohde_schwarz.write('sour:pow:lev:imm:ampl {0}'.format(step[1]))
    rigol.write('sens:freq:cent {0}'.format(step[0]))
    rohde_schwarz.write('outp 1')
    time.sleep(5)
    print(rigol.query('fetc:harm:amp:all?'))
    rohde_schwarz.write('outp 0')
rohde_schwarz.write('*rst; status:preset; *cls')