# Comments on commands are quoted from instrument manuals.
class Instrument:
    def __init__(self, resource):
        self.resource = resource
  
    def idn(self):
        return self.resource.query('*idn?')

class Rigol(Instrument):
    def reset(self):
        self.resource.write('*cls')
        #self.resource.write('*rst; status:preset; *cls')

    def set_xy_marker(self):
        '''Uses normal marker.

        It is used to measure the X (Frequency or Time) and Y (Amplitude) values of a certain point on the trace.'''
        self.resource.write('calculate:marker1:mode position')
    
    def set_marker_trace_auto(self):
        '''Enables the auto trace marking of the specified marker.'''
        self.resource.write('calculate:marker1:trace:auto on')
        self.resource.write('calculate:marker1:cpsearch:state on')
    
    def set_marker_readout_auto(self):
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
    
    def set_reference_level(self, value):
        '''Sets the reference level.'''
        self.resource.write('display:window:trace:y:scale:rlevel {0}'.format(value))

    def search_marker_peak_max(self):
        '''Performs one peak search based on the search mode set by the :CALCulate:MARKer:PEAK:SEARch:MODE
        command and marks it with the specified marker.'''
        self.resource.write('calculate:marker1:maximum:max')
      
    def get_marker_x(self):
        '''Queries the X-axis value of the specified marker.  Its default unit is Hz.'''
        return float(self.resource.query('calculate:marker1:x?'))
    
    def get_marker_y(self):
        '''Queries the Y-axis value of the specified marker, and its default unit is dBm.

        If the marker mode of the specified marker is Position or Fixed, the query command queries the Y value of the marker.
        If the marker mode of the specified marker is Delta, the query command queries the Y-axis difference 
        between the reference marker and the Delta marker.'''
        return float(self.resource.query('calculate:marker1:y?'))

class RohdeSchwarz(Instrument):
    def reset(self):
        self.resource.write('*rst; status:preset; *cls')
        #rohde_schwarz.write('syst:disp:upd 0')

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

__version__ = '0.1'