# Coding_Challenge_SM
Subtle Medical Coding Challenge
# Converting from Dicom to hdf5 and back again
to convert from dicom to hdf5 use the dicom2hdf5.py file

input arguments:

  • --input-dicom, -i path to input DICOM directory
  
  • --output-hdf5, -h path to output hdf5 file
  
  • --output-json, -j path to output JSON file
  
  
to do the reverse, use: hdf52dicom.py

input arguments:

  • --input-hdf5, -h path to input hdf5 file
  
  • --input-dicom, -d path to the template DICOM directory
  
  • --output-dicom, -o path to output DICOM directory

# Code structure:

takes input commands via argparse. Then it searches for all dicom file in a directory, 
it stacks them into a dictionary via the pydicom reader and uses their slice location as the key
since there are 3 slices per slice location its 

key -> array [ dicom1, dicom2, dicom3 ]

I then sort the slice location array and use that to order the dicom dictionary into ascending order, from there I extract
and stack each dicom's pixel array and then normalize each array. Once everything has been stacked and normalized I cast 
it to np.float32, and store it into an hdf5

For the reverse, it mostly happens in opposite order with a few different steps for formating and functionality.

# Testing

You can test the code with your own command line arguments or you can uncomment out my test code at the bottom of the main






