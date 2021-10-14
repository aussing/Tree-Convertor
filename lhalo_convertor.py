from unicodedata import decimal
import h5py
import numpy as np
from ctypes import c_longlong as c_ll
import time
# import sys

def get_tree_dtype():       # Define the lhalo tree data structure
    tree_structure=[
    ('Descendant', np.int32),
    ('FirstProgenitor', np.int32),
    ('NextProgenitor', np.int32),
    ('FirstHaloInFOFgroup', np.int32),
    ('NextHaloInFOFgroup', np.int32),
    ('SubLen', np.int32),

    # SAGE reads 3 mass vairables but only uses M_VIR/M_Crit200, M_Mean_200 & M_TopHat aren't used
    ('M_Mean200', np.float32), # Not used in SAGE, can be filled with dummy values
    ('Mvir', np.float32), ##M_crit_200
    ('M_tophat', np.float32), # Not used in SAGE, can be filled with dummy values

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
    N_Trees = tree_data['Header'].attrs['Ntrees_ThisFile']
    tot_NHalos = tree_data['Header'].attrs['Nhalos_ThisFile']
    # NumSimTreeFiles = tree_data['Header'].attrs['NumFiles']
    TreeLen = np.array(tree_data['TreeTable/Length'],dtype=np.int32)
    print(f"N_trees = {N_Trees}")
    print(f"tot_NHalos = {tot_NHalos}\n")
    return (N_Trees, tot_NHalos, TreeLen)


def read_tree_structure(tree_data,tot_NHalos):
    ## Tree properties
    Descendant = np.array(tree_data['TreeHalos/TreeDescendant'])
    FirstProgenitor = np.array(tree_data['TreeHalos/TreeFirstProgenitor'])
    NextProgenitor = np.array(tree_data['TreeHalos/TreeNextProgenitor'])
    FirstHaloInFOFgroup = np.array(tree_data['TreeHalos/TreeFirstHaloInFOFgroup'])
    NextHaloInFOFgroup = np.array(tree_data['TreeHalos/TreeNextHaloInFOFgroup'])
    ##Subhalo Properties
    SubLen = np.array(tree_data['TreeHalos/SubhaloLen'])
    M_Mean200 = np.array(tree_data['TreeHalos/Group_M_Crit200']) # Not used in SAGE, dummy values
    Mvir = np.array(tree_data['TreeHalos/Group_M_Crit200']) # Important mass input value
    M_tophat = np.array(tree_data['TreeHalos/Group_M_Crit200']) # Not used in SAGE, dummy values
    Pos = np.array(tree_data['TreeHalos/SubhaloPos'])
    Vel = np.array(tree_data['TreeHalos/SubhaloVel'])
    VelDisp = np.array(tree_data['TreeHalos/SubhaloVelDisp'])
    Vmax = np.array(tree_data['TreeHalos/SubhaloVmax'])
    Spin = np.array(tree_data['TreeHalos/SubhaloSpin'])
    MostBoundID = np.array(tree_data['TreeHalos/SubhaloIDMostbound'])
    SnapNum = np.array(tree_data['TreeHalos/SnapNum'])
    FileNr = tree_data['Header'].attrs['NumFiles']
    ## Only have 1 tree file, conversion on file by file
    SubhaloIndex = np.array(tree_data['TreeHalos/TreeID'])
    SubHalfMass = np.array(tree_data['TreeHalos/SubhaloHalfmassRad'])

    tree_dtype = get_tree_dtype()
    tree_block = np.empty(tot_NHalos, dtype=tree_dtype)
    print(f'Started reading trees into lhalo structure \n')
    for this_halo in range(tot_NHalos):
        tree_block[this_halo]= (
        Descendant[this_halo],
        FirstProgenitor[this_halo],
        NextProgenitor[this_halo],
        FirstHaloInFOFgroup[this_halo],
        NextHaloInFOFgroup[this_halo],
        SubLen[this_halo],
        M_Mean200[this_halo],
        Mvir[this_halo],
        M_tophat[this_halo],
        Pos[this_halo],
        Vel[this_halo],
        VelDisp[this_halo],
        Vmax[this_halo],
        Spin[this_halo],
        MostBoundID[this_halo],
        SnapNum[this_halo],
        FileNr, ## FileNr[this halo], FileNr is a single int from the gadget tree header
        SubhaloIndex[this_halo],
        SubHalfMass[this_halo] )
    return (tree_block)

def convert_to_lhalo(input_filename,output_filename):
    tree_data = h5py.File(input_filename, 'r')
    N_trees,tot_NHalos,TreeLen = read_header_props(tree_data)
    l_halo_structure = read_tree_structure(tree_data,tot_NHalos)
    with open(output_filename,'wb') as f:
        f.write(N_trees)
        f.write(tot_NHalos)
        f.write(TreeLen)
        f.write(l_halo_structure)

if __name__ == "__main__":
    start_time =time.time()
    input_filename = "/path/to/data/trees.hdf5"
    output_filename = "path/to/data/L_halo_tree.0"
    
    print(f"\nStart reading data from {input_filename}\n") 
    convert_to_lhalo(input_filename,output_filename)
    print(f"Converted {input_filename} and wrote to {output_filename}")
    end_time = time.time()
    print(f"Time taken = {np.round((end_time-start_time),decimals=2)} seconds\n")