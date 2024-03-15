# https://github.com/pyvisa/pyvisa-py
# pip install pyvisa-py
# pip install pyusb
# pip install psutil
# pip install zeroconf

import pyvisa

rm = pyvisa.ResourceManager('@py')

print(rm.list_resources())
# ('USB0::0x1AB1::0x0588::DS1K00005888::INSTR')
# inst = rm.open_resource('USB0::0x1AB1::0x0588::DS1K00005888::INSTR')
# print(inst.query("*IDN?"))



# python-vxi11
# import vxi11
# import numpy as np
# inst = vxi11.Instrument('TCPIP0::192.168.0.254::INSTR')
# print(inst.ask('*IDN?'))
# inst.write('SYST:LANG "SCPI"') 
