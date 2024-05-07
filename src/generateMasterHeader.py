__author__ = 'ankita sahu'
__email__ = 'sahuankita2203@gmail.com'

import gc
import glob
import os
import pandas as pd
from astropy.io import fits
from configparser import ConfigParser

fits_file_extension_list = ["*fits", "*FITS", "*Fits"]

class MasterHeader:
    def __init__(self,config_filepath):
        self.config_filepath = os.getcwd() + "/" + config_filepath
        self.fits_filepath = None
        self.current_filepath = os.getcwd() + "/"
        pass

    def readConfigurationFile(self, mode="DEFAULT"):
        config = ConfigParser()
        config.sections()
        config.read(self.config_filepath)
        self.fits_filepath = config[mode]["fits_filepath"]
        pass

    def generateMasterHeaderCSV(self, telescope_name=None):
        master_header_filepath = self.current_filepath + "MasterHeaderList_" + telescope_name + ".csv"
        # if not os.path.exists(master_header_filepath):      # for first run
        if os.path.exists(master_header_filepath):  # for subsequent runs after first run
            master_header = set()
            with open(master_header_filepath, 'w+') as out_file:
                for extn in fits_file_extension_list:
                    for files in glob.glob(self.fits_filepath + extn):
                        print(files)
                        with fits.open(files) as hdulist:
                            header = hdulist[0].header
                            dict_header = {k: header[k] for k in header.keys() if k}
                        master_header.update(dict_header)
                df = pd.DataFrame(sorted(master_header))
                df.to_csv(out_file, sep=',', index=False, header=False, encoding='utf-8')
                del df
        gc.collect()


if __name__ == "__main__":
    o_mh = MasterHeader("config.ini")
    # o_mh.readConfigurationFile(mode="TEST")     # to be disabled when run in server
    o_mh.readConfigurationFile()      # to be enabled when run in server
    o_mh.generateMasterHeaderCSV(telescope_name="DOT")
