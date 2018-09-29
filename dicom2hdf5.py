import pydicom
import numpy as np
import h5py
import os
import argparse

class Convert(object):

    def __init__(self, dicom_path, hdf5_path, json_path):
        self.dicom = dicom_path
        self.hdf5 = hdf5_path
        self.json_path = json_path
        self.dicom_files = {}
        self.sl_list = []

    def find_dicom(self):
        for file in os.listdir(self.dicom):
            if file.endswith(".dcm"):
                ds = pydicom.dcmread(os.path.join(self.dicom, file))
                sl = ds.SliceLocation
                self.dicom_files[str(sl)] = ds
                self.sl_list.append(float(sl))



    def build_volume(self):
        (x, y), length = self.dicom_files[str(self.sl_list[0])].pixel_array.shape, len(self.sl_list)
        self.sl_list = sorted(self.sl_list)
        vol = np.empty((length, x, y), np.float32)
        for slice in range(length):
            raw = self.dicom_files[str(self.sl_list[slice])].pixel_array
            normalized = raw
            vol[slice] = normalized





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    #parser.add_argument("-i", "--input-dicom")
    #parser.add_argument("-h", "--output-hdf5")
    #parser.add_argument("-j", "--output-json")



    parser.parse_args()

    converter = Convert("../subtlemedicalcodingchallenge/dicom_data/01_BreastMriNactPilot/Mr_Breast - 148579/SagittalIR_3DFGRE_3/", "", "")
    converter.find_dicom()
    converter.build_volume()