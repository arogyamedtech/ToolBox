from pathlib import Path
import glob
import pandas as pd


__version__ = "0.1.0"
__author__ = "Sandeepan Bhattacharyya <bsandeepan95.work@gmail.com>"
__copyright__ = "Copyright (c) 2019 Sandeepan Bhattacharyya"
__credits__ = ["Sandeepan Bhattacharyya", "Sandeepan Sengupta"]
__license__ = "Creative Commons Attribution-NoDerivatives 4.0 International (CC BY-ND 4.0)"
__maintainer__ = "Sandeepan Bhattacharyya"
__email__ = "bsandeepan95.work@gmail.com"
__status__ = "Production"


def create_path(Path):
    """ Creates a provided Path. Ignores if it already exists.
    """
    Path.mkdir(parents=True, exist_ok=True)


def merge_csv(src_path, dest_path, searchkw, mergekw, sep="_", ext="csv"):
    """ Lists all CSV files in the source Path and mergers them into 
        one combined CSV file, and saves it to the destination Path. 
    """
    dest_path = dest_path.joinpath("{}{}{}.{}".format(
        searchkw, sep, mergekw, ext))
    src_path = src_path.joinpath(searchkw)
    if not dest_path.parent.exists:
            create_path(dest_path.parent)
    _all_filenames = [i for i in glob.glob('{}{}*.{}'.format(
        src_path, sep, ext))]
    #combine all files in the list & export to csv
    _combined_csv = pd.concat([pd.read_csv(f) for f in _all_filenames ])
    _combined_csv.to_csv(dest_path, index=False, encoding='utf-8-sig')
    print("File Created.")


def write_csv(dataset, csv_header_list, dest_path, index_label):
    """ creates a CSV File Path with _dir and count, then saves the dataset
        to the CSV file according to the CSV Headers.
    """
    if not dest_path.parent.exists:
        create_path(dest_path.parent)
    pd.DataFrame(dataset, columns=csv_header_list).to_csv(dest_path,
        index_label=index_label, encoding='utf-8-sig')


def read_csv(filenamepath, delim=",", type=0, index_col=None):
    """ Reads the file in the FilePath and based on 'type' param value,
        type=0 -> returns a NumPy Array Structure.
        type=1 -> returns a Pandas DataFrame
    """
    if type == 0:
        return pd.read_csv(filenamepath, delimiter=delim, index_col=index_col
            ).values
    elif type == 1:
        return pd.read_csv(filenamepath, delimiter=delim, index_col=index_col)


if __name__ == "__main__":
    # merge csv example
    local_path = "SavedData"
    uuid = input("Gimme UUID to locate directory: ")
    ext = 'csv'
    src_path = Path("{0}/{1}".format(local_path, uuid))
    dest_path = Path(src_path)
    merge_csv(src_path, dest_path, uuid, "complete", sep='_',  ext=ext)
