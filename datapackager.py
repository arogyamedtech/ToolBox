"""
    A Packager module that collects patient metadata and EEG/ECG data from
    LSL stream, and generates a patient metada CSV file and a Comprehensive
    Data CSV file. These files will be used in further applications.
"""

import packeeg as peg
import gen_operations as gnop
from uuid import uuid4
import csv_opds as csvop
from pathlib import Path
from datetime import datetime
import pandas as pd

__version__ = "0.1.0"
__author__ = "Sandeepan Bhattacharyya <bsandeepan95.work@gmail.com>"
__copyright__ = "Copyright (c) 2019 Sandeepan Bhattacharyya"
__credits__ = ["Sandeepan Bhattacharyya", "Sandeepan Sengupta"]
__license__ = "Creative Commons Attribution-NoDerivatives 4.0 International (CC BY-ND 4.0)"
__maintainer__ = "Sandeepan Bhattacharyya"
__email__ = "bsandeepan95.work@gmail.com"
__status__ = "Development"


def generate_files(savepath):
    """ It is a package function. Read module description above.
            savepath: Path() variable pointing to the Save Folder Path.
    """
    # generate session id and create a dir using it in Save Folder Path
    _session = uuid4().hex
    _ssnpath = savepath.joinpath(_session)
    csvop.create_path(_ssnpath)

    ssnhdr = 'session_id'
    dhdr = ["h_id", "h_name"]
    data = {}
    data[dhdr[0]] = uuid4().hex
    data[dhdr[1]] = input("Enter Hospital Name: ")

    _temp_h, _temp_d = gnop.get_patient_meta_cli()
    data.update(_temp_d)
    dhdr = [ssnhdr,] + _temp_h + dhdr
    data[dhdr[0]] = _session
    _to_write = [data[d] for d in dhdr]

    # write patient metadata to file
    _pt_path = _ssnpath.joinpath("patient_{}.csv".format(data[dhdr[1]]))
    with open(_pt_path, 'w') as ptf:
        ptf.write("{}\n{}\n".format(", ".join(dhdr), ", ".join(_to_write)))

    _drn = float(input("Enter duration (seconds)\t:\t"))
    _cnt = int(input("Enter sample index count\t:\t"))
    print("\n\nEvent ID\t:\t" + str(_session) + "\n")
    print("\nInitiated at\t:\t" + str(datetime.utcnow()))
    peg.fetch(_duration=_drn, _count=_cnt, _UUID=_session)
    print("\nCompleted at\t:\t" + str(datetime.utcnow()))
    
    print("Generating Final CSV File...")
    dat_data = csvop.read_csv(Path().joinpath(_session, 
        "data_{}_complete.csv".format(_session)), type=1, index_col=0)
    dat_data.insert(0, dhdr[1].upper(), data[dhdr[1]])
    final_fpath = Path("{0}/data_{0}_integrated.csv".format(_session))
    dat_data.to_csv(final_fpath, index_label="Index", encoding='utf-8-sig')
    print("File Generated Successfully at {}.".format(final_fpath))


if __name__ == "__main__":
    generate_files(Path("SavedData"))
