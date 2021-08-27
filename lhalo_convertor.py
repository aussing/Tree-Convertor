import h5py 
import numpy as np
from ctypes import c_longlong as c_ll

path = '/Users/101125182/Documents/2021/data/DM_L50_N128_output/trees.hdf5'

tree_data = h5py.File(path, 'r')

print("Start reading data from ", path,"\n")

## Header Properties
header = tree_data.require_group('Header').attrs

N_Trees = int(header.__getitem__('Ntrees_Total'))
tot_NHalos = int(header.__getitem__('Nhalos_Total'))
# Tree_NHalos = header.__getitem__('NHalos_per_tree') 
# ParticleMass = header.__getitem__('Part_Mass') 
NumSimTreeFiles = int(header.__getitem__('NumFiles'))

## Datasets ##

## Merger tree pointers
TreeID = np.array(tree_data['TreeHalos/TreeID'], dtype=int)
TreeIndex = np.array(tree_data['TreeHalos/TreeIndex'], dtype=int)
TreeLen = np.array(tree_data['TreeTable/Length'], dtype=int)
Descendant = np.array(tree_data['TreeHalos/TreeDescendant'], dtype=int)
FirstProgenitor = np.array(tree_data['TreeHalos/TreeFirstProgenitor'], dtype=int)
NextProgenitor = np.array(tree_data['TreeHalos/TreeNextProgenitor'], dtype=int)
FirstHaloInFOFgroup = np.array(tree_data['TreeHalos/TreeFirstHaloInFOFgroup'], dtype=int)
NextHaloInFOFgroup = np.array(tree_data['TreeHalos/TreeNextHaloInFOFgroup'], dtype=int)

##Sub halo Properties
SubLen = np.array(tree_data['TreeHalos/SubhaloLen'], dtype=float)
Mvir = np.array(tree_data['TreeHalos/Group_M_Crit200'], dtype=float)
Pos = np.array(tree_data['TreeHalos/SubhaloPos'], dtype=float)
Vel = np.array(tree_data['TreeHalos/SubhaloVel'], dtype=float)
VelDisp = np.array(tree_data['TreeHalos/SubhaloVelDisp'], dtype=float)
Vmax = np.array(tree_data['TreeHalos/SubhaloVmax'], dtype=float)
Spin = np.array(tree_data['TreeHalos/SubhaloSpin'], dtype=float)
MostBoundID = np.array(tree_data['TreeHalos/SubhaloIDMostbound'], dtype=c_ll)

## Position in tree file

SnapNum = np.array(tree_data['TreeHalos/SnapNum'], dtype=int)
FileNr = int(header.__getitem__('NumFiles'))
## Only have outputs w/ 1 tree file atm, not sure where parameter for file number will be stored if at all
SubhaloIndex = np.array(tree_data['TreeHalos/TreeID'], dtype=int)
SubHalfMass = np.array(tree_data['TreeHalos/SubhaloHalfmassRad'], dtype=float)
print('finished reading variables \n')

## Write out to binary file -- WIP


print('Writing to L_Halo binary file \n')

## Combine to make things more readable
HeaderParams = np.array([N_Trees,tot_NHalos,*TreeLen])#,NumSimTreeFiles], dtype=int)
print(HeaderParams)
# MergerTreeData = np.array([*Descendant,*FirstProgenitor,*NextProgenitor,*FirstHaloInFOFgroup,*NextHaloInFOFgroup], dtype=int)
# SubHaloData = np.array([*SubLen,*Mvir,*Pos,*Vel,*VelDisp,*Vmax,*Spin])
# PositionInTree = np.array([*SnapNum, FileNr, *SubhaloIndex], dtype=int) 

All = np.array([HeaderParams], dtype=np.int32)#, *MergerTreeData,*SubHaloData,*MostBoundID,*PositionInTree,*SubHalfMass]) 
# print("All Shape: ", All.shape)pwd
with open('/Users/101125182/Documents/2021/data/L_halo_tree','wb+') as f:
    f.write(All)
print("done")