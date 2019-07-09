"""
   Contains all general CLI operation methods that are used in CEREBROS
   s/w cli system.

   Note that this module is still being developed.
"""

from uuid import uuid4

__version__ = "0.1.0"
__author__ = "Sandeepan Bhattacharyya <bsandeepan95.work@gmail.com>"
__copyright__ = "Copyright (c) 2019 Sandeepan Bhattacharyya"
__credits__ = ["Sandeepan Bhattacharyya", "Sandeepan Sengupta"]
__license__ = "Creative Commons Attribution-NoDerivatives 4.0 International (CC BY-ND 4.0)"
__maintainer__ = "Sandeepan Bhattacharyya"
__email__ = "bsandeepan95.work@gmail.com"
__status__ = "Development"


def get_baby_meta_cli():
    """ Gets baby's information from user from Console.
        Then returns the info as an object.
    """

    baby_data = {}
    baby_data['id'] = uuid4().hex
    baby_data['name'] = input("Enter baby's name: ")
    baby_data['mother_name'] = input("Enter mother's name: ")
    baby_data['baby_id'] = input("Enter baby's ID: ")
    baby_data['date_of_birth'] = input("Enter baby's DOB: ")
    baby_data['time_of_birth'] = input("Enter baby's TOB: ")
    baby_data['body_weight'] = input("Enter baby's body weight (in kg): ")
    baby_data['gestational_age'] = input("Enter baby's age: ")
    baby_data['baby_image'] = input("Enter baby's image link: ")
    return baby_data


def get_neonate_meta_cli():
    """ Gets neonate's information from user from Console.
        Then returns the info as an object.
    """
    neonate_data = {}
    neonate_data['n_id'] = uuid4().hex
    neonate_data['n_mother'] = input("Enter mother's name: ")
    neonate_data['n_name'] = "Baby of " + neonate_data["mother_name"]
    # neonate_data['n_ncu_id'] = input("Enter neonate's NCU/SNCU ID: ")
    neonate_data["n_disc_no"] = input("Enter Disc. No.: ")
    neonate_data["n_sex"] = input("Enter neonate's sex (Male/Female/Other): ")
    neonate_data['n_dob'] = input("Enter baby's DOB: ")
    neonate_data['n_tob'] = input("Enter baby's TOB: ")
    neonate_data['n_bw'] = input("Enter baby's body weight (in kg): ")
    neonate_data['n_gage'] = input("Enter getational age (weeks): ")
    return neonate_data


def get_patient_meta_cli():
    """ Gets patient's information from user from Console.
        Then returns the info as an object.
    """

    pt_header = ["p_id", "p_mom", "p_name", "p_mom_id_type", "p_mom_id_num",
        "p_dob", "p_tob", "p_gage", "p_sex", "d_id"]
    pt_data = {}
    pt_data[pt_header[0]] = uuid4().hex
    pt_data[pt_header[1]] = input("Enter patient's mother's name: ")
    pt_data[pt_header[2]] = "Baby of " + pt_data[pt_header[1]]
    pt_data[pt_header[3]] = input("Enter mother's govt. ID " + 
                        "type (PAN/AADHAAR/VOTER): ")
    pt_data[pt_header[4]] = input("Enter mother's govt. ID: ")
    pt_data[pt_header[5]] = input("Enter patient's Date of Birth (DD/MM/YYYY): ")
    pt_data[pt_header[6]] = input("Enter patient's Time of Birth (HH:MM): ")
    pt_data[pt_header[7]] = input("Enter gestational age: ") + " weeks"
    pt_data[pt_header[8]] = get_patient_sex()
    pt_data[pt_header[9]] = uuid4().hex
    return pt_header, pt_data


def get_patient_sex():
    """ Gets Patient's Sex from user."""

    _pstr = """
        Provide Patient's Sex -
        \tPress 1 (or M/m) for Male.
        \tPress 2 (or F/f) for Female.
        \tPress 3 (or O/o) for Other.
        \nEnter your choice: """
    psex = input(_pstr).lower()
    if psex in ('1', 'm'):
        return "Male"
    elif psex in ('2', 'f'):
        return "Female"
    elif psex in ('3', 'o'):
        return "Other"
    else:
        print("Wrong input. Try again.")
        get_patient_sex()


if __name__ == "__main__":
    get_patient_meta_cli()
