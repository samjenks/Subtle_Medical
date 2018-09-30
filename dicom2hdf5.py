import pydicom
import numpy as np
import h5py
import os
import json
import argparse

class Convert(object):

    def __init__(self, dicom_path, hdf5_path, json_path):
        self.dicom = dicom_path
        self.hdf5 = hdf5_path
        self.json_path = json_path
        self.dicom_files = {}
        self.sl_list = []
        self.vol = None

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
            normalized = raw/255.0 # normalizing based on range of int values {0,255}, norm func = x-min(x)/(max(x)-min(x))
            vol[slice] = normalized
        self.vol = vol

    def convert(self):
        #print(self.dicom_files[str(self.sl_list[45])]) #Modality, SeriesDescription, PixelSpacing
        mod, sd, ps = self.dicom_files[str(self.sl_list[45])].Modality, \
                      self.dicom_files[str(self.sl_list[45])].SeriesDescription, \
                      self.dicom_files[str(self.sl_list[45])].PixelSpacing
        data = {}
        data['Modality'] = mod
        data['SeriesDescription'] = sd
        data['PixelSpacing'] = (ps[0], ps[1])

        with open(self.json_path, 'w') as outfile:
            json.dump(data, outfile)

        hf = h5py.File(self.hdf5, 'w')
        hf.create_dataset('dataset', data=self.vol)
        hf.close()





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--output-hdf5")
    parser.add_argument("-i", "--input-dicom")
    parser.add_argument("-j", "--output-json")



    args = parser.parse_args()
    #converter = Convert("../subtlemedicalcodingchallenge/dicom_data/01_BreastMriNactPilot/Mr_Breast - 148579/SagittalIR_3DFGRE_3/", "output_data.h5", 'output.json')
    converter = Convert(args.input-dicom, args.output-hdf5, args.output-json)
    converter.find_dicom()
    converter.build_volume()
    converter.convert()