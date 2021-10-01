import h5py
import numpy as np
from ctypes import c_longlong as c_ll
import sys
# import line_profiler

## Set path to data -- update path can be input
# @profile
def read_trees(file_path):
    ## define data structure of L-Halo tree
    tree_structure=[
    ('Descendant', np.int32),
    ('FirstProgenitor', np.int32),
    ('NextProgenitor', np.int32),
    ('FirstHaloInFOFgroup', np.int32),
    ('NextHaloInFOFgroup', np.int32),
    ('SubLen', np.int32),
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
    tree_dtype = np.dtype({'names':names, 'formats':formats}, align=True) 
    print("data type item size = ",tree_dtype.itemsize)
    ## turn data structure into data type

    tree_data = h5py.File(file_path, 'r')
    print("\nStart reading data from {file_path}\n")
    ## Header Properties
    header = tree_data.require_group('Header').attrs
    N_Trees = np.int32(header.__getitem__('Ntrees_ThisFile'))
    print(f"N_trees = {N_Trees} \n")
    tot_NHalos = np.int32(header.__getitem__('Nhalos_ThisFile'))
    print(f"tot_NHalos = {tot_NHalos} \n")
    NumSimTreeFiles = header.__getitem__('NumFiles')
    TreeLen = np.array(tree_data['TreeTable/Length'],dtype=np.int32)
    ## Datasets ##
    ## Tree properties
    # TreeID = np.array(tree_data['TreeTable/TreeID']) ##Not actually used anywhere
    # TreeIndex = np.array(tree_data['TreeHalos/TreeIndex']) ##Not actually used anywhere
    
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
    ## Position in tree file
    SnapNum = np.array(tree_data['TreeHalos/SnapNum'])
    FileNr = header.__getitem__('NumFiles')  
    ## Only have 1 tree file, conversion on file by file
    SubhaloIndex = np.array(tree_data['TreeHalos/TreeID'])
    SubHalfMass = np.array(tree_data['TreeHalos/SubhaloHalfmassRad'])

    tree_block = np.empty(tot_NHalos, dtype=tree_dtype)
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
    # print('finished reading variables \n')
    return (N_Trees,tot_NHalos,TreeLen,tree_block)

if __name__ == "__main__":
    input_filename = "/Users/101125182/Documents/2021/data/mini-millennium/treedata/trees.hdf5"
    output_filename = "/Users/101125182/Documents/2021/data/mini-millennium/Converted/L_halo_tree.0.test"

    N_trees,tot_NHalos,TreeLen,l_halo_structure = read_trees(input_filename)
    with open(output_filename,'wb') as f:
        f.write(N_trees)
        f.write(tot_NHalos)
        f.write(TreeLen)
        f.write(l_halo_structure)

print(f"Data written to {output_filename} \n")