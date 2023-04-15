from os import path
from datetime import datetime
import constants
import warnings
warnings.filterwarnings("ignore")

def get_location_of_uploaded():
    BASEDIR = constants.BASEDIR + str('/images/original')
    PREFIX = 'image'
    EXTENSION = 'jpg'
    file_name_format = "{:s}-{:%Y%m%d_%H%M%S}.{:s}"

    date = datetime.now()
    file_name = file_name_format.format(PREFIX, date, EXTENSION)

    file_path = path.normpath(path.join(BASEDIR, file_name))
    return file_path, file_name

def get_save_location_of_detected():
    BASE_DIR = constants.BASEDIR + str('/images/detected')
    PREFIX = 'pothole-detected'
    EXTENSION = 'jpg'
    file_name_format = "{:s}-{:%Y%m%d_%H%M%S}.{:s}"

    date = datetime.now()

    file_name = file_name_format.format(PREFIX, date, EXTENSION)

    file_path = path.normpath(path.join(BASE_DIR, file_name))
    return file_path, file_name

def get_show_location_of_detected(my_file_name):
    BASE_DIR = constants.BASEDIR + str('/images/detected')
    PREFIX = my_file_name
    file_name = path.normpath(path.join(PREFIX))
    file_path = path.normpath(path.join(BASE_DIR, file_name))
    return file_path
