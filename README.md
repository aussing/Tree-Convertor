# Tree-Convertor


A python code to convert Gadget-4 tree files into an LHaloTree mergertree format.


This script is designed to read in the output mergertrees from the cosmological simulation Gadget-4. The data is restructured into an LHaloTree mergertree format and written out to a binary file. The output is intended to be used in Sage-Model, so some values are ignored; M_mean_200 and M_TopHat aren't used in Sage calculations so can be filled with dummy values (they also aren't properly defined in the Gadget output). 

The code currently doens't have the capability to handle multiple input files at once, thus any trees split across multiple input files will remain split in the converted files.
