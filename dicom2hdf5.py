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
                if str(sl) in self.dicom_files:
                    self.dicom_files[str(sl)].append(ds)
                else:
                    self.dicom_files[str(sl)] = []
                    self.dicom_files[str(sl)].append(ds)
                if float(sl) not in self.sl_list:
                    self.sl_list.append(float(sl))


    def build_volume(self):
        (x, y), length = self.dicom_files[str(self.sl_list[0])][0].pixel_array.shape, len(self.sl_list)
        self.sl_list = sorted(self.sl_list)
        vol = []
        for slice in range(length):

            for version in range(len(self.dicom_files[str(self.sl_list[slice])])):

                raw = self.dicom_files[str(self.sl_list[slice])][version].pixel_array
                normalized = raw/255.0 # normalizing based on range of int values {0,255}, norm func = x-min(x)/(max(x)-min(x))
                vol.append(normalized)

        self.vol = np.array(vol, dtype=np.float32)


    def convert(self):
        #print(self.dicom_files[str(self.sl_list[45])]) #Modality, SeriesDescription, PixelSpacing
        mod, sd, ps = self.dicom_files[str(self.sl_list[45])][0].Modality, \
                      self.dicom_files[str(self.sl_list[45])][0].SeriesDescription, \
                      self.dicom_files[str(self.sl_list[45])][0].PixelSpacing
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
    # override the default -h for help
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--help",  action="help", help="show this help message and exit")
    parser.add_argument("-i", "--input-dicom", dest="dicom_input", help="dicom formatted input file")
    parser.add_argument("-h", "--output-hdf5", dest="hdf5_output", required=True, help="output of hdf5 file")
    parser.add_argument("-j", "--output-json", dest="json_output", required=True, help="json formatted output file")

    test_args = ['-i', '../subtlemedicalcodingchallenge/dicom_data/01_BreastMriNactPilot/Mr_Breast - 148579/SagittalIR_3DFGRE_3/','-h', 'output_data.h5',  '-j','output.json']

    args = parser.parse_args()

    #override with test args array
    #args = parser.parse_args(test_args)

    #converter = Convert("../subtlemedicalcodingchallenge/dicom_data/01_BreastMriNactPilot/Mr_Breast - 148579/SagittalIR_3DFGRE_3/", "output_data.h5", 'output.json')
    converter = Convert(args.dicom_input, args.hdf5_output, args.json_output)
    converter.find_dicom()
    converter.build_volume()
    converter.convert()