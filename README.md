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


# Inference Pipeline and reinventing the gaussian wheel

For the mock gaussian filter, I implemented a math formula for a gaussian distribution and then created the kernel from that.
if the the filter needs more than one channel it concatenates with itself to the correct number of channels. 
I assumed that pixel spacing represented the size of the kernel since it wasn't definitively stated. 
from there I just applied the kernel to the entire input image. 

For the Inference Pipeline, the jobs are stored as a nested
dictionary with the high-level key being the job name and sub-level keys being the rest of the names in the named tuple with 
corresponding values. The other minor methods of the Inference class are essentially doing dictionary managment and checking.
The execution method uses a dispatch table to call the stored functions passing in the needed arguments. I created the 
pre/post processing function since there weren't any. As the specific specs and purpose were specified, I assumed that 
pre-processing's job was to collect all of the dicom files in a directory and send them to the job execution function. The
post-processing method's job was to take the newly blurred images and re-insert them into their corresponding dicoms and
save them as a sort of update funtionality.

# Web Backend from Scratch

I would like to preface this section with the information that my web backend creation knowledge is pretty limited to liberty
I know 0% of any of the listed frameworks, but I figured I would attempt to make something. I chose to use flask, I think I
the job route to work functionally as it sets up the inference pipeline, generates a JobEntry and runs it. The query route does not work as I realized that I was running out of time and was far beyond my flask understanding.
