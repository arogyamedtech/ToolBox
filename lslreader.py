#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Written for the CEREBROS system, this module reads from open LSL stream 
    and writes the data to a file having any of the following formats -
    a) JSON, b) TXT, c) CSV

    Note: This module was developed in a testing phase and thereofore the file
    write operations are not optimized for long duration or low end h/w setup.
"""

from pylsl import StreamInlet, resolve_stream
import time

__version__ = "1.1.0"
__author__ = "Sandeepan Bhattacharyya <bsandeepan95.work@gmail.com>"
__copyright__ = "Copyright (c) 2019 Sandeepan Bhattacharyya"
__credits__ = ["Sandeepan Bhattacharyya", "Sandeepan Sengupta"]
__license__ = "Creative Commons Attribution-NoDerivatives 4.0 International (CC BY-ND 4.0)"
__maintainer__ = "Sandeepan Bhattacharyya"
__email__ = "bsandeepan95.work@gmail.com"
__status__ = "Development"


def write_stream_to_file(inlet, filename, ext, timespan):
    """ This function redirects to modular function based on file extension."""
    start_time = time.time()
    fl_ext = filename + "." + ext

    if ext == "json":
        jsonwriter(inlet, start_time, fl_ext, timespan)
    elif ext == "txt":
        txtwriter(inlet, start_time, fl_ext, timespan)
    elif ext == "csv":
        csvwriter(inlet, start_time, fl_ext, timespan)


def txtwriter(inlet, start_time, fl_ext, timespan):
    """ Writes timestamp and data list in TXT file."""
    with open(fl_ext, "a") as opf:
        while (int(time.time() - start_time) <= timespan):
            sample, timestamp = inlet.pull_sample()
            to_write = """{}: {}\n""".format(timestamp, sample)
            opf.write(to_write)


def jsonwriter(inlet, start_time, fl_ext, timespan):
    """ Writes timestamp and data list in JSON file."""
    with open(fl_ext, "a") as opf:
        opf.write("{")
        while (int(time.time() - start_time) <= timespan):
            sample, timestamp = inlet.pull_sample()
            to_write = """\n\t"{}": {},""".format(timestamp, sample)
            opf.write(to_write)
        
        opf.seek(0, 2)
        opf.truncate(opf.tell() - 1)
        opf.write("\n}")


def csvwriter(inlet, start_time, fl_ext, timespan):
    """ Writes CSV header and following columns of timestamp and data."""
    csvhdr = input("Provide CSV file header string with all column" + 
            " names separated by ',' below: \n")
    csv_writer_init(fl_ext, csvhdr)
    while (int(time.time() - start_time) <= timespan):
        sample, timestamp = inlet.pull_sample()
        to_write = "\n{}, {}".format(timestamp, ','.join([str(s) 
            for s in sample]))
        csv_writer_repeat(fl_ext, to_write)


def csv_writer_repeat(fl_ext, to_write):
    """ to open csv file to write data repeatedly."""
    with open(fl_ext, "a") as opf:
        opf.write(to_write)


def csv_writer_init(fl_ext, to_write):
    """ initial csv write to write the headers.
        DO NOT REPEAT THIS FUNCTION!
    """
    with open(fl_ext, "w") as opf:
        opf.write(to_write)


def set_stream(stream_name):
    """ First resolve a stream on the lab network. Then,
        return a new inlet to read from the stream.
    """
    return StreamInlet(resolve_stream('type', stream_name)[0])


def set_eeg_stream():
    """ Set EEG Stream inlet ready to read from. """
    return set_stream("EEG")


if __name__ == "__main__":
    inlet = set_eeg_stream()
    fname = input("Enter file name to record data in JSON(no ext): ")
    write_stream_to_file(inlet, fname, "json", 30)
