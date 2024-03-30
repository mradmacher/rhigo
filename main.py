# https://github.com/pyvisa/pyvisa-py
# https://www.rohde-schwarz.com/webhelp/smb100a_html_usermanual_1/Content/2e097e6397fa40bd.htm#d79403e12303
# https://www.rekirsch.at/user_html/1282834349/pix/a/media/RSA3030N/RSA3000_ProgrammingGuide_EN.pdf

# pip install pyvisa-py
# pip install pyusb
# pip install psutil
# pip install zeroconf

import pyvisa
import time
import re
import csv
import rhigo.instr

class Input:
    def __init__(self, freq, ampt):
        self.freq = freq
        self.ampt = ampt

def discover_rohde_schwarz_and_rigol():
    rm = pyvisa.ResourceManager('@py')
    print(rm.list_resources('?*'))

    rohde_schwarz_name = 'TCPIP::192.168.1.11::INSTR'
    rigol_name = 'TCPIP::192.168.1.14::INSTR'

    rohde_schwarz = rhigo.instr.RohdeSchwarz(rm.open_resource(rohde_schwarz_name))
    idn_result = rohde_schwarz.idn()
    print(idn_result)
    assert re.match('Rohde&Schwarz', idn_result)

    rigol = rhigo.instr.Rigol(rm.open_resource(rigol_name))
    idn_result = rigol.idn()
    print(idn_result)
    assert re.match('Rigol', idn_result)

    return (rohde_schwarz, rigol)

def read_inputs(in_filename):
    inputs = []
    with open(in_filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            inputs.append(Input(freq = int(row[0]), ampt = int(row[1])))

    return inputs

inputs = read_inputs('input.csv')
rohde_schwarz, rigol = discover_rohde_schwarz_and_rigol()

rigol.reset()
rigol.set_xy_marker()
rigol.set_auto_trace()
rigol.set_auto_readout()
rigol.set_peak_search_max()
rigol.set_marker_x_readout_freq()

rohde_schwarz.reset()
rohde_schwarz.activate_rf_output()

out_filename = "{}_out.csv".format(time.strftime("%Y-%m-%d_%H%M%S", time.localtime()))

with open(out_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, dialect='excel')

    for input in inputs:
        print('Rohde&Schwarz: {0}HZ, {1}dBm'.format(input.freq, input.ampt))
        rigol.set_center_freq(input.freq)
        rohde_schwarz.set_rf_freq(input.freq)
        rohde_schwarz.set_rf_level(input.ampt)
        time.sleep(0.5)

        rigol.search_marker_peak_max()
        freq = rigol.get_marker_x()
        ampt = rigol.get_marker_y()
        print('Rigol: {0}Hz, {1}dBm'.format(freq, ampt))

        # format(math.pi, '.2f')   # give 2 digits after the point
        writer.writerow([input.freq, input.ampt, ampt])

        time.sleep(2)

rohde_schwarz.deactivate_rf_output()
