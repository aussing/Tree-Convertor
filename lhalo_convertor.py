from unicodedata import decimal
import time, sys, os
import h5py
import numpy as np
from pathlib import Path
from ctypes import c_longlong as c_ll


def get_tree_dtype():         # Define the lhalo tree data structure
    tree_structure=[
    ('Descendant', np.int32),
    ('FirstProgenitor', np.int32),
    ('NextProgenitor', np.int32),
    ('FirstHaloInFOFgroup', np.int32),
    ('NextHaloInFOFgroup', np.int32),
    ('SubLen', np.int32),

    # SAGE reads 3 mass vairables but only uses M_VIR/M_Crit200, M_Mean_200 & M_TopHat aren't used
    ('M_Mean200', np.float32), # Not used in SAGE, can be filled with dummy values
    ('Mvir', np.float32),      # M_crit_200 in Gadget output
    ('M_tophat', np.float32),  # Not used in SAGE, can be filled with dummy values

    ('Pos', (np.float32,3)),
    ('Vel', (np.float32,3)),
    ('VelDisp', np.float32),
    ('Vmax', np.float32),
    ('Spin', (np.float32,3)),
    ('MostBoundID', c_ll),
    ('SnapNum', np.int32),
    ('FileNr', np.int32),
    ('SubhaloIndex', np.int32),
    ('SubHalfMass', np.float32)
    ]
    tree_structure=np.array(tree_structure,dtype=object)
    names = tree_structure[:,0]
    formats = tree_structure[:,1]
    lhalo_dtype = np.dtype({'names':names, 'formats':formats}, align=True) 
    return lhalo_dtype

def read_header_props(tree_data):       # Read out the header properties to be written at the beginning of the SAGE input file
    N_Trees = np.int32(tree_data['Header'].attrs['Ntrees_ThisFile'])
    tot_NHalos = np.int32(tree_data['Header'].attrs['Nhalos_ThisFile'])
    TreeLen = np.array(tree_data['TreeTable/Length'],dtype=np.int32)
    NumSimTreeFiles = tree_data['Header'].attrs['NumFiles']
    return (N_Trees, tot_NHalos, TreeLen, NumSimTreeFiles)


def read_tree_structure(tree_data,tot_NHalos,file_number,start_halo):
    ## Tree properties
    Descendant = np.array(tree_data['TreeHalos/TreeDescendant'])
    FirstProgenitor = np.array(tree_data['TreeHalos/TreeFirstProgenitor'])
    NextProgenitor = np.array(tree_data['TreeHalos/TreeNextProgenitor'])
    FirstHaloInFOFgroup = np.array(tree_data['TreeHalos/TreeFirstHaloInFOFgroup'])
    NextHaloInFOFgroup = np.array(tree_data['TreeHalos/TreeNextHaloInFOFgroup'])
    ##Subhalo Properties
    SubLen = np.array(tree_data['TreeHalos/SubhaloLen'])
    M_Mean200 = np.array(tree_data['TreeHalos/Group_M_Crit200'])    # Not used in SAGE, dummy values
    Mvir = np.array(tree_data['TreeHalos/Group_M_Crit200'])         # Important mass input value
    M_tophat = np.array(tree_data['TreeHalos/Group_M_Crit200'])     # Not used in SAGE, dummy values
    Pos = np.array(tree_data['TreeHalos/SubhaloPos'])
    Vel = np.array(tree_data['TreeHalos/SubhaloVel'])
    VelDisp = np.array(tree_data['TreeHalos/SubhaloVelDisp'])
    Vmax = np.array(tree_data['TreeHalos/SubhaloVmax'])
    Spin = np.array(tree_data['TreeHalos/SubhaloSpin'])
    MostBoundID = np.array(tree_data['TreeHalos/SubhaloIDMostbound'])
    SnapNum = np.array(tree_data['TreeHalos/SnapNum'])
    # File Number read into sage -> "file_number" is defined below from the file name
    # FileNr = tree_data['Header'].attrs['NumFiles'] ## This gives the total number of tree files for the simulation
    FileNr = file_number
    SubhaloIndex = np.array(tree_data['TreeHalos/TreeID'])
    SubHalfMass = np.array(tree_data['TreeHalos/SubhaloHalfmassRad'])

    tree_dtype = get_tree_dtype()
    tree_block = np.empty(tot_NHalos-start_halo, dtype=tree_dtype)
    for write_halo in range(len(tree_block)):
        read_halo = write_halo+start_halo
        tree_block[write_halo]= (
        Descendant[read_halo],
        FirstProgenitor[read_halo],
        NextProgenitor[read_halo],
        FirstHaloInFOFgroup[read_halo],
        NextHaloInFOFgroup[read_halo],
        SubLen[read_halo],
        M_Mean200[read_halo],
        Mvir[read_halo],
        M_tophat[read_halo],
        Pos[read_halo],
        Vel[read_halo],
        VelDisp[read_halo],
        Vmax[read_halo],
        Spin[read_halo],
        MostBoundID[read_halo],
        SnapNum[read_halo],
        FileNr,
        SubhaloIndex[read_halo],
        SubHalfMass[read_halo] )
    return (tree_block)

def run_all(input_data_directory,output_data_directory):
    # Loops over all "trees." files in the input directory
    for file_name in [ file_name for file_name in os.listdir(input_data_directory) if file_name.startswith("trees.")]:
        file_start_time =time.time()
        print(f"file being converted = {file_name}")
        file = input_data_directory+"/"+file_name
        tree_data = h5py.File(file, 'r')

        # When Gadget-4 outputs >1 treefiles the 6th element in the output treefile name is the n-th file associated with the simulation.
        # ie. If there are 3 output files they'll be named trees.0.hdf5, trees.1.hdf5, & trees.2.hdf5
        # If there is only 1 output tree file it'll be named trees.hdf5, and the 6th element will be the "h" as in ".hdf5". In this case 
        # I've set it to 0 for SAGE input simplicity 
        file_number = file_name[6] 
        if file_number=="h": 
            file_number = "0"

        output_filename = "l_halo_tree."+file_number
        final_output = output_data_directory+"/"+output_filename

        N_Trees, tot_NHalos, TreeLen, NumSimTreeFiles = read_header_props(tree_data)
        
        print(f"Total trees in this file = {N_Trees}, Total halos in this file = {tot_NHalos}")
        print(f"sum tree length = {np.sum(TreeLen)}")
        # print(f"length tree length = {len(TreeLen)}\n")
        
        if NumSimTreeFiles == 1:
            l_halo_structure = read_tree_structure(tree_data,tot_NHalos,file_number,start_halo)

        elif NumSimTreeFiles > 1 :
            start_halo = np.where([tree_data['TreeTable/TreeID'][0]==tree_data['TreeHalos/TreeID']])[1][0]
            l_halo_structure = read_tree_structure(tree_data,tot_NHalos,file_number,start_halo)
            if np.sum(TreeLen) > (tot_NHalos-start_halo):
                append_file_name = list(file_name)
                append_file_name[6] = str(int(file_number)+1)
                append_file_name="".join(append_file_name)
                append_file = input_data_directory+"/"+append_file_name
                append_tree_data = h5py.File(append_file, 'r')
                append_n_halos = np.where([append_tree_data['TreeTable/TreeID'][0]==append_tree_data['TreeHalos/TreeID']])[1][0]

                append_l_halo_structure = read_tree_structure(append_tree_data,append_n_halos,file_number,0)
                l_halo_structure = np.concatenate((l_halo_structure,append_l_halo_structure))
                tot_NHalos = np.int32(len(l_halo_structure))
        
        print(f"Total trees written out to file {file_number} = {N_Trees}")
        print(f"All halos for trees in the file {file_number} = {len(l_halo_structure)}")
        with open(final_output,'wb') as f:
            f.write(N_Trees)
            f.write(tot_NHalos)
            f.write(TreeLen)
            f.write(l_halo_structure)
        
        file_end_time = time.time()
        print(f"Finished converting {file_name} into {output_filename}")
        print(f"File time taken = {np.round((file_end_time-file_start_time),decimals=2)} seconds\n")
        print("====================================================================\n")
        

if __name__ == "__main__":
    start_time =time.time()

    input_data_directory = sys.argv[1]          # Gets the location of the Gadget-4 mergertree files
    # input_data_directory = "/path/to/data"          # allows for hardcoding of Gadget-4 mergertree files
    output_data_directory = sys.argv[2]         # Gets the location of the converted filesd
    # output_data_directory = "/path/to/output"        # allows for hardcoding of converted files
    
    print("")                
    print(f"Input data location = {input_data_directory}")
    print(f"Output data location = {output_data_directory}")
    print("====================================================================\n")
    
    run_all(input_data_directory,output_data_directory)

    end_time = time.time()
    print(f"Total time taken = {np.round((end_time-start_time),decimals=2)} seconds\n")