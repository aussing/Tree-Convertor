# Tree-Convertor


A python code to convert Gadget-4 tree files into an LHaloTree mergertree format.


This script is designed to read in the output mergertrees that can be generated in post processing from the cosmological simulation Gadget-4. The data is restructured into an LHaloTree mergertree format and written out to a binary file. The script takes in two input arguments. The first argument is the location of Gadget-4 mergertree files. The second argument is desired location for the converted files. The output is intended to be used in Sage-Model, so some values are ignored; M_mean_200 and M_TopHat aren't used in Sage calculations so can be filled with dummy values. This script has the capability to read and organise multiple mergertree files, as files need to contain whole trees to be used in Sage-Model, and Gadget-4 outputs often split trees across two files.
