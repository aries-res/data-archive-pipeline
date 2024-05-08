__author__ = 'ankita sahu'
__email__ = 'sahuankita2203@gmail.com'

import gc
import glob
import os
import pandas as pd
from astropy.io import fits
from configparser import ConfigParser

fits_file_extension_list = ["*fits", "*FITS", "*Fits"]

class ImageData:
    d_header = dict()
    def __init__(self,config_filepath, telescope=None):
        self.current_filepath = os.getcwd() + "/"
        self.config_filepath = self.current_filepath + config_filepath
        self.fits_filepath = None
        self.master_header_filepath = None
        self.telescope = telescope
    def readConfigurationFile(self, mode="DEFAULT"):
        config = ConfigParser()
        config.sections()
        config.read(self.config_filepath)
        self.fits_filepath = config[mode]["fits_filepath"]
        self.master_header_filepath = config[mode]["master_header_filepath_"+self.telescope]
        pass

    def createDictOfAllHeaders(self):
        df = pd.read_csv(self.master_header_filepath, encoding='utf-8')
        df["Value"] = ""
        self.d_header = dict(zip(df["Header"],df["Value"]))
        pass

    def generateCsvSummaryOfFitsFiles(self):
        l_col_header = list(self.d_header.keys())
        l_col_header.insert(0, "Filename")
        df = pd.DataFrame(columns=l_col_header)
        for extn in fits_file_extension_list:
            for files in glob.glob(self.fits_filepath + extn):
                print(files)
                with fits.open(files) as hdulist:
                    header = hdulist[0].header
                    hdr_dict = dict()
                    df_row = [files.split("/")[-1]]
                    for i in header.keys():
                        if i:
                            hdr_dict[i] = header[i]
                    for k in self.d_header.keys():
                        df_row.append(hdr_dict[k] if k in hdr_dict else '')
                df.loc[len(df)] = df_row
                df.to_csv(os.getcwd()+"/summaryOfAllFitsFiles.csv", index=False, sep=',', encoding='UTF-8')
        del df
        gc.collect()

if __name__ == "__main__":
    o_imagedata = ImageData("config.ini",telescope="DOT")
    o_imagedata.readConfigurationFile(mode="TEST")     # to be disabled when run in server
    o_imagedata.readConfigurationFile()      # to be enabled when run in server
    o_imagedata.createDictOfAllHeaders()
    o_imagedata.generateCsvSummaryOfFitsFiles()
