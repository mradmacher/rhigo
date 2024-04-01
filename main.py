import time
import csv
import rhigo.instr

class Input:
    def __init__(self, freq, ampt):
        self.freq = freq
        self.ampt = ampt

def read_inputs(in_filename):
    inputs = []
    with open(in_filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            inputs.append(Input(freq = int(row[0]), ampt = int(row[1])))

    return inputs

def find_max_level(inputs):
    max = 0
    for input in inputs:
        if input.ampt > max:
            max = input.ampt
    return max

inputs = read_inputs('input.csv')
rohde_schwarz, rigol = rhigo.instr.discover_rohde_schwarz_and_rigol()

rigol.reset()
rigol.set_peak_search_max()
rigol.set_xy_marker()
rigol.set_marker_trace_auto()
rigol.set_marker_readout_auto()
rigol.set_marker_x_readout_freq()
rigol.set_reference_level(find_max_level(inputs))

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
rohde_schwarz.reset()