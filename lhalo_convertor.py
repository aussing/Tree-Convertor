import h5py
import numpy as np
from ctypes import c_longlong as c_ll
import sys

## Set path to data -- update path can be input
path = '/Users/101125182/Documents/2021/data/DM_L50_N128_output/trees.hdf5'

class all_trees:
    def read_trees(file_path):
        ## define data structure of L-Halo tree
        tree_structure=[
        ('Descendant', np.int32),
        ('FirstProgenitor', np.int32),
        ('NextProgenitor', np.int32),
        ('FirstHaloInFOFgroup', np.int32),
        ('NextHaloInFOFgroup', np.int32),
        ('SubLen', np.int32),
        ('M_Mean200', np.float32),
        ('Mvir', np.float32), ##M_crit_200
        ('M_tophat', np.float32),
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
        ## turn data structure into data type

        tree_data = h5py.File(file_path, 'r')
        print("Start reading data from ", path,"\n")
        ## Header Properties
        header = tree_data.require_group('Header').attrs
        N_Trees = np.int32(header.__getitem__('Ntrees_Total'))
        tot_NHalos = np.int32(header.__getitem__('Nhalos_Total'))
        NumSimTreeFiles = header.__getitem__('NumFiles')
        ## Datasets ##
        ## Tree properties
        # TreeID = np.array(tree_data['TreeTable/TreeID']) ##Not actually used anywhere
        # TreeIndex = np.array(tree_data['TreeHalos/TreeIndex']) ##Not actually used anywhere
        TreeLen = np.array(tree_data['TreeTable/Length'],dtype=np.int32)
        Descendant = np.array(tree_data['TreeHalos/TreeDescendant'])
        FirstProgenitor = np.array(tree_data['TreeHalos/TreeFirstProgenitor'])
        NextProgenitor = np.array(tree_data['TreeHalos/TreeNextProgenitor'])
        FirstHaloInFOFgroup = np.array(tree_data['TreeHalos/TreeFirstHaloInFOFgroup'])
        NextHaloInFOFgroup = np.array(tree_data['TreeHalos/TreeNextHaloInFOFgroup'])
        ##Subhalo Properties
        SubLen = np.array(tree_data['TreeHalos/SubhaloLen'])
        Mvir = np.array(tree_data['TreeHalos/Group_M_Crit200'])
        M_Mean200 = np.array(tree_data['TreeHalos/SubhaloMass'])
        M_tophat = np.array(tree_data['TreeHalos/SubhaloMass'])
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
            print(SnapNum[this_halo])
        
##trying to turn the headerparams (N_Trees,Tot_NHalos,TreeLen(N_halos/tree)) into structure & combine with tree block-not sure if necessary
        # new_thing = [
        #     ('N_Trees', np.int32),
        #     ('tot_NHalos', np.int32),
        #     ('TreeLen',(np.int32,len(TreeLen)))
        # #     ('tree_block', (tree,tot_NHalos))
        # ]
        # new_thing=np.array(new_thing,dtype=object)
        # new_names = new_thing[:,0]
        # new_formats = new_thing[:,1]
        # new_tree = np.dtype({'names':new_names, 'formats':new_formats}, align=True)
        
        # final = np.empty((1,),dtype=new_tree)
        # final[0,] = (N_Trees,
        #     tot_NHalos,
        #     TreeLen,)
            # tree_block)
            
        print('finished reading variables \n')
        return (N_Trees,tot_NHalos,TreeLen,tree_block)

N_trees,tot_NHalos,TreeLen,l_halo_structure = all_trees.read_trees(path)
print(N_trees,tot_NHalos,TreeLen.shape)
print(l_halo_structure.shape)

with open('/Users/101125182/Documents/2021/data/L_halo_tree','wb+') as f:
    f.write(N_trees)
    f.write(tot_NHalos)
    f.write(TreeLen)
    f.write(l_halo_structure)
 
    
print("Data written to /Users/101125182/Documents/2021/data/L_halo_tree")