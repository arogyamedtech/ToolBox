"""
    Pulls EEG/ECG data from LSL Stream and creates -
    1.  Several CSV files generated at regular interval containing data chunks.
    2.  A Complete CSV file containing entire dataset (merged). 
"""

from lslreader import set_eeg_stream
from datetime import datetime
import uuid
from pathlib import Path
import csv_opds as csv_op
import time


__version__ = "0.1.0"
__author__ = "Sandeepan Sengupta <mail@sandeepan.info>"
__copyright__ = "Copyright (c) 2019 Sandeepan Sengupta, Sandeepan Bhattacharyya"
__credits__ = ["Sandeepan Bhattacharyya", "Sandeepan Sengupta"]
__license__ = "Creative Commons Attribution-NoDerivatives 4.0 International (CC BY-ND 4.0)"
__maintainer__ = "Sandeepan Bhattacharyya"
__email__ = "bsandeepan95.work@gmail.com"
__status__ = "Development"


def grab(_inlet, _count = 1280):
    """ Reads EEG/ECG data stream from LSL Inlet. 
    """
    _ts_init = time.time_ns() / (10 ** 9)
    counter = 0
    _dataset = []
    _lsl_data, _lsl_time = _inlet.pull_sample()
    while counter < _count:
        if _lsl_data is not None:
            _dataset.append([_lsl_time, _lsl_data])
            counter += 1
        _lsl_data, _lsl_time = _inlet.pull_sample()

    return _ts_init, _dataset, datetime.utcnow()


def package(dataset, _count=0, _dir=str(uuid.uuid4().hex), _t_ref=0, _t_start=0):
    """ Reformats EEG dataset into a 2D array and writes it 
        into CSV File(s) along with Header Index array.
    """ 
    csv_header_list = ["TimeStamp", "CH1", "CH2", "CH3", 
        "CH4", "CH5", "CH6", "CH7", "CH8"]
    dataset = [[(_t_start + (data[0] - _t_ref))] + data[1] for data in dataset]
    csv_path = Path("{0}/data_{0}_{1}.csv".format(_dir, _count))
    csv_op.write_csv(dataset, csv_header_list, csv_path, "Index")


def fetch(_duration=10, _count=1280, _sampleRate=256,
    _inlet=set_eeg_stream(), _UUID=uuid.uuid4().hex):
    """ Handles all the following -
        1. Calculates how many chunk-oriented CSV files to generate.
        2. Records EEG/ECG data from LSL stream into a 3D dataset array.
        3. Manages writing datasets to chunk CSV files.
        4. Writes info of all chunk CSV files into a metadata CSV file.
        5. Merges all chun CSV files into a complete CSV file.
    """
    _loopCount = (_duration * _sampleRate)/_count
    _loopLeft = 0

    # create the directory if not exists
    _dir = str(_UUID)
    Path(_dir).mkdir(parents=True, exist_ok=True)

    md_file = Path("{}/_{}.csv".format(_dir, _UUID))
    
    md_header = ["Start", "End", "Count"]
    _md = []

    if(_loopCount < 1):
        _loopCount = 1
        _count = int(_duration * _sampleRate)
    else:
        _loopLeft = _loopCount - int(_loopCount)
        _loopCount = int(_loopCount)
    
    _loopCounter = 0
    _LSL_t_ref = 0

    while(_loopCounter < _loopCount):
        
        __t_begin, __dataset, __t_stop = grab(_inlet, _count)
        if _loopCounter is 0:
            _LSL_t_ref = __dataset[0][0]

        package(__dataset, _loopCounter,_dir, _LSL_t_ref, __t_begin)
        _md.append([__t_begin, __t_stop, _count])
        _loopCounter += 1
        
        if(_loopLeft > 0 and _loopCounter is _loopCount):
            
            _count = int(_duration * _sampleRate) - (_count * _loopCount)
            __t_begin, __dataset, __t_stop = grab(_inlet, _count)
            package(__dataset, _loopCounter,_dir, _LSL_t_ref, __t_begin)
      
        _md.append([__t_begin, __t_stop, _count])
        
    csv_op.write_csv(_md, md_header, md_file, "Index")
    concat_path = Path(_dir)
    csv_op.merge_csv(concat_path, concat_path, ("data_" + _UUID), "complete")


if __name__ == "__main__":

    _drn = float(input("Enter duration (seconds)\t:\t"))
    _cnt = int(input("Enter sample index count\t:\t"))
    _srt = int(input("Enter sample rate (Hertz)\t:\t"))
    _uid = uuid.uuid4().hex
        
    print("\n\nEvent ID\t:\t" + str(_uid) + "\n")
    print("\nInitiated at\t:\t" + str(datetime.utcnow()))
    fetch(_duration = _drn, _count = _cnt, _sampleRate = _srt, _inlet = set_eeg_stream(), _UUID = _uid)
    print("\nCompleted at\t:\t" + str(datetime.utcnow()))
