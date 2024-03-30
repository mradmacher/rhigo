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

class Input:
    def __init__(self, freq, ampt):
        self.freq = freq
        self.ampt = ampt

# Comments on commands are quoted from instrument manuals.
class Instrument:
    def __init__(self, resource):
        self.resource = resource
  
    def idn(self):
        return resource.query('*idn?')

class Rigol(Instrument):
    def reset(self):
        self.resource.write('*cls')
        #print(rigol.write('*rst; status:preset; *cls'))

    def measure_freq_time_ampt(self):
        '''Uses normal marker.

        It is used to measure the X (Frequency or Time) and Y (Amplitude) values of a certain point on the trace.'''
        self.resource.write('calculate:marker:mode position')
    
    def set_auto_trace(self):
        '''Enables the auto trace marking of the specified marker.'''
        self.resource.write('calculate:marker1:trace:auto on')
    
    def set_auto_readout(self):
        '''Enables the auto readout mode of the specified marker.

        When you enable the marker's auto marking trace function, the marker shifts 
        from its off state to on state, and the marker's marking trace is automatically
        determined by the instrument.'''
        self.resource.write('calculate:marker1:x:readout:auto on')

    def set_peak_search_max(self):
        ''' Sets the peak search mode.

        MAXimum: indicates maximum. If "maximum" is selected under search mode, the system will search for the maximum value on the trace.
        The command is only valid for the peak search executed by sending the :CALCulate:MARKer<n>:MAXimum[:MAX] command.'''
        self.resource.write('calculate:marker:peak:search:mode maximum')

    def set_marker_x_readout_freq(self):
          '''Sets the readout mode of the X axis of the specified marker.

        FREQuency: indicates frequency. It is the default readout mode in non-zero span mode.'''
        self.resource.write('calculate:marker1:x:readout frequency')

    def set_center_freq(self, value):
        ''' Sets the center frequency. '''
        self.resource.write('sens:frequency:center {0}'.format(value))

    def search_peak_max(self):
        '''Performs one peak search based on the search mode set by the :CALCulate:MARKer:PEAK:SEARch:MODE
        command and marks it with the specified marker.'''
        self.resource.write('calculate:marker1:maximum:max')
      
    def get_marker_x(self):
        '''Queries the X-axis value of the specified marker.  Its default unit is Hz.'''
        return float(rigol.query('calculate:marker1:x?'))
    
    def get_marker_y(self):
        '''Queries the Y-axis value of the specified marker, and its default unit is dBm.

        If the marker mode of the specified marker is Position or Fixed, the query command queries the Y value of the marker.
        If the marker mode of the specified marker is Delta, the query command queries the Y-axis difference 
        between the reference marker and the Delta marker.'''
        return float(rigol.query('calculate:marker1:y?'))

class RohdeSchwarz(Instrument):
    def reset(self):
        self.resource.write('*rst; status:preset; *cls')
        #rohde_schwarz.write('syst:disp:upd 1')

    def activate_rf_output(self):
        ''' Activates RF signal output.'''
        self.resource.write('output 1')

    def deactivate_rf_output(self):
        ''' Deactivates RF signal output.'''
        self.resource.write('output 0')

    def set_rf_freq(self, value):
        ''' Enters the RF frequency, considering the frequency offset.'''
        self.resource.write('source:frequency:cw {0}Hz'.format(value))

    def set_rf_level(self, value):
        ''' Enters the RF level, considering the level offset.'''
        self.resource.write('source:power:level:immediate:amplitude {0}dBm'.format(value))


def discover_rohde_schwarz_and_rigol():
    rm = pyvisa.ResourceManager('@py')
    print(rm.list_resources('?*'))

    rohde_schwarz_name = 'TCPIP::192.168.1.5::INSTR'
    rigol_name = 'TCPIP::192.168.1.11::INSTR'

    rigol = Rigol(rm.open_resource(rigol_name))
    print(rigol.query('*idn?'))

    rohde_schwarz = RohdeSchwarz(rm.open_resource(rohde_schwarz_name))
    idn_result = rohde_schwarz.idn()
    print(idn_result)
    assert re.match('Rohde&Schwarz', idn_result)

    rigol = Rigol(rm.open_resource(rigol_name))
    idn_result = rigol.idn()
    print(idn_result)
    assert re.match('Rigol', idn_result)

    return (rohde_schwarz, rigol)

def read_inputs(in_filename):
    with open(in_filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            inputs.append(Input(freq = row[0], ampt = row[1]))


inputs = read_inputs('input.csv')

with open(in_filename, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        inputs.append(Input(freq = row[0], ampt = row[1]))

rohde_schwarz, rigol = discover_rohde_schwarz_and_rigol()

rigol.reset()
rigol.measure_freq_time_ampt()
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
        rigol.set_center_freq(value.freq)
        rohde_schwarz.set_rf_freq(input.freq)
        rohde_schwarz.set_rf_level(input.ampt)
        time.sleep(0.5)

        rigol.search_peak_max()
        freq = rigol.get_marker_x()
        ampt = rigol.get_marker_y()
        print('Rigol: {0}Hz, {1}dBm'.format(freq, ampt))

        # format(math.pi, '.2f')   # give 2 digits after the point
        writer.writerow([input.freq, input.ampt, ampt])

        time.sleep(2)

rohde_schwarz.deactivate_rf_output()
