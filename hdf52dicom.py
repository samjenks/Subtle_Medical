import pydicom
import numpy as np
import h5py
import os
import random
import argparse


class Convert(object):

    def __init__(self, dicom_path, hdf5_path, dicom_output):
        self.dicom = dicom_path
        self.hdf5 = hdf5_path
        self.output_path = dicom_output
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
                if str(sl) in self.dicom_files:
                    self.dicom_files[str(sl)].append(ds)
                else:
                    self.dicom_files[str(sl)] = []
                    self.dicom_files[str(sl)].append(ds)
                if float(sl) not in self.sl_list:
                    self.sl_list.append(float(sl))
        # get hdf5 file prepped
        hf = h5py.File(self.hdf5, 'r')
        for data in list(hf.keys()):
            self.hdf5_file = np.array(hf.get(data), dtype=np.int16)

    def reformat(self):
        self.new_series_id()

        rescaled = (255 * self.hdf5_file)
        vol = rescaled
        vol_idx = 0
        for slice in range(len(self.sl_list)):
            for version in range(len(self.dicom_files[str(self.sl_list[slice])])):
                # sent the dicom np array to writable
                self.dicom_files[str(self.sl_list[slice])][version].pixel_array.setflags(write=1)
                # write to copy
                np.copyto(self.dicom_files[str(self.sl_list[slice])][version].pixel_array, vol[vol_idx])
                # sent back to unwritable
                self.dicom_files[str(self.sl_list[slice])][version].pixel_array.setflags(write=0)

                # replace IDs with new versions
                self.dicom_files[str(self.sl_list[slice])][version].SeriesInstanceUID = self.prefix + "." + str(self.series_suffix)
                self.dicom_files[str(self.sl_list[slice])][version].SOPInstanceUID = self.prefix + "." + str(self.new_id())

                # write pixel_array to pixel data and same dicom to output path
                self.dicom_files[str(self.sl_list[slice])][version].PixelData = \
                    self.dicom_files[str(self.sl_list[slice])][version].pixel_array.tobytes()

                if not os.path.isdir(self.output_path):
                    os.mkdir(self.output_path)
                self.dicom_files[str(self.sl_list[slice])][version]. \
                    save_as(self.output_path + "output" + str(vol_idx) + ".dcm")

                # increase index of hdf5 volume 3d pixel array
                vol_idx += 1

    def new_series_id(self):
        list1 = self.dicom_files[str(self.sl_list[1])][0].SeriesInstanceUID.split(".")
        self.prefix = '.'.join(list1[:-1])
        self.series_suffix = random.randint(0, 999999999999999999999999999999)
        if str(list1[len(list1)-1]) == self.series_suffix:
            self.new_series_id()

    @staticmethod
    def new_id():
        return random.randint(0, 999999999999999999999999999999)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--help", action="help", help="show this help message and exit")
    parser.add_argument("-d", "--input-dicom", dest="dicom_input", help="dicom formatted input file")
    parser.add_argument("-h", "--output-hdf5", dest="hdf5_output", required=True, help="output of hdf5 file")
    parser.add_argument("-o", "--output-dicom", dest="dicom_output", required=True, help="json formatted output file")

    test_args = ['-d',
                 '../subtlemedicalcodingchallenge/dicom_data/01_BreastMriNactPilot/Mr_Breast - 148579/SagittalIR_3DFGRE_3/',
                 '-h', 'output_data.h5', '-o', 'output/']

    # args = parser.parse_args()

    # override with test args array
    args = parser.parse_args(test_args)

    Converter = Convert(args.dicom_input, args.hdf5_output, args.dicom_output)

    # Converter = Convert("../subtlemedicalcodingchallenge/dicom_data/01_BreastMriNactPilot/Mr_Breast - 148579/SagittalIR_3DFGRE_3/", "output_data.h5", 'output/')
    Converter.find_files()
    Converter.reformat()