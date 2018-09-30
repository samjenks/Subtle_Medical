import pydicom
import numpy as np
import h5py
import os
import random
import json
import argparse


class Convert(object):

    def __init__(self, dicom_path, hdf5_path, json_path):
        self.dicom = dicom_path
        self.hdf5 = hdf5_path
        self.json_path = json_path
        self.dicom_files = {}
        self.sl_list = []
        self.hdf5_file = []
        self.prefix = ""
        self.series_suffix = ""

    def find_files(self):
        # find all the dicom files and store them
        for file in os.listdir(self.dicom):
            if file.endswith(".dcm"):
                ds = pydicom.dcmread(os.path.join(self.dicom, file))
                sl = ds.SliceLocation
                self.dicom_files[str(sl)] = ds
                self.sl_list.append(float(sl))
        # get hdf5 file prepped
        hf = h5py.File(self.hdf5, 'r')
        for data in list(hf.keys()):
            self.hdf5_file = np.array(hf.get(data))

    def reformat(self):
        self.new_series_id()

        vol = self.build_volume()
        rescaled = (255 * self.hdf5_file)
        vol = rescaled

        #print(self.dicom_files[str(self.sl_list[1])])
        for slice in range(len(self.sl_list)):
            print("slice:", self.sl_list[slice])
            #print(type(self.dicom_files[str(self.sl_list[slice])].pixel_array))
            #print(type(vol[slice]))
            # self.dicom_files[str(self.sl_list[slice])].pixel_array = vol[slice]
            self.dicom_files[str(self.sl_list[slice])].SeriesInstanceUID = (self.prefix + "." + str(self.series_suffix))

            print(self.dicom_files[str(self.sl_list[slice])].SOPInstanceUID)



    def build_volume(self):
        (x, y), length = self.dicom_files[str(self.sl_list[0])].pixel_array.shape, len(self.sl_list)
        self.sl_list = sorted(self.sl_list)
        vol = np.empty((length, x, y))
        for slice in range(length):
            vol[slice] = self.dicom_files[str(self.sl_list[slice])].pixel_array
        return vol

    def new_series_id(self):
        list1 = self.dicom_files[str(self.sl_list[1])].SeriesInstanceUID.split(".")
        self.prefix = '.'.join(list1[:-1])
        self.series_suffix = random.randint(0, 999999999999999999999999999999)
        if str(list1[len(list1)-1]) == self.series_suffix:
            self.new_series_id()

    @staticmethod
    def new_id():
        return random.randint(0, 999999999999999999999999999999)



if __name__ == '__main__':
    Converter = Convert("../subtlemedicalcodingchallenge/dicom_data/01_BreastMriNactPilot/Mr_Breast - 148579/SagittalIR_3DFGRE_3/", "output_data.h5", 'output.json')
    Converter.find_files()
    #Converter.reformat()