import pydicom
import numpy
import h5py
import os
import argparse

class Convert(object):

    def __init__(self, dicom_path, hdf5_path, json_path):
        self.dicom = dicom_path
        self.hdf5 = hdf5_path
        self.json_path = json_path
        self.dicom_files = []

    def find_dicom(self):
        for file in os.listdir(self.dicom):
            if file.endswith(".dcm"):
                self.dicom_files.append(os.path.join(self.dicom, file))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    #parser.add_argument("-i", "--input-dicom")
    #parser.add_argument("-h", "--output-hdf5")
    #parser.add_argument("-j", "--output-json")



    parser.parse_args()

    converter = Convert("../subtlemedicalcodingchallenge/dicom_data/01_BreastMriNactPilot/Mr_Breast - 148579/SagittalIR_3DFGRE_3/", "", "")
    converter.find_dicom()