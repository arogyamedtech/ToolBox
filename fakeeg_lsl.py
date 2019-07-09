"""	Simulator for OpenBCI 8-Channel BioSensing built for Testing purposes only.
"""

import time
import random
from random import random as rand
from pylsl import StreamInfo, StreamOutlet

__version__ = "0.1.0"
__author__ = "Sandeepan Sengupta <mail@sandeepan.info>"
__copyright__ = "Copyright (c) 2019 Sandeepan Sengupta, Sandeepan Bhattacharyya"
__credits__ = ["Sandeepan Bhattacharyya", "Sandeepan Sengupta"]
__license__ = "Creative Commons Attribution-NoDerivatives 4.0 International (CC BY-ND 4.0)"
__maintainer__ = "Sandeepan Bhattacharyya"
__email__ = "bsandeepan95.work@gmail.com"
__status__ = "Development"


def simulate_biosignal():
	""" Start OpenBCI 8-CH Bio Signal Simulattion."""
	#create StreamInfo
	random_id = random.randint(0,255)
	eeg_name = 'openbci_eeg'
	eeg_type = 'EEG'
	eeg_chan = 8
	eeg_hz = 256
	eeg_data = 'float32'
	eeg_id = 'openbci_eeg_id' + str(random_id)
	labels = ['Fp1', 'Fp2', 'C3', 'C4', 'T5', 'T6', 'O1', 'O2',
		'F7', 'F8', 'F3', 'F4', 'T3', 'T4', 'P3', 'P4']
	info = StreamInfo(eeg_name,eeg_type,eeg_chan,eeg_hz,eeg_data,eeg_id)

	# next make an outlet
	outlet = StreamOutlet(info)

	print ("--------------------------------------\n"+ \
		"LSL Configuration: \n" + \
		"  LSL Stream: \n" + \
		"      Name: " + eeg_name + " \n" + \
		"      Type: " + eeg_type + " \n" + \
		"      Channel Count: " + str(eeg_chan) + "\n" + \
		"      Sampling Rate: " + str(eeg_hz) + "\n" + \
		"      Channel Format: "+ eeg_data + " \n" + \
		"      Source Id: " + eeg_id + " \n" + \
		str(labels) + "\n" + \
		"---------------------------------------\n")
	
	while True:
		mysample = [rand() for _ in range(8)]
		outlet.push_sample(mysample)
		time.sleep(1 / eeg_hz)


if __name__ == "__main__":
	simulate_biosignal()
