import h5py 
import numpy as np

path = '/Users/101125182/Documents/2021/data/DM_L50_N128_output/trees.hdf5'

tree_data = h5py.File(path, 'r')

print("Start reading values from ", path)

## Header Properties
header = tree_data.require_group('Header').attrs
N_Trees = header.__getitem__('Ntrees_Total')  #first thing to be read in

tot_NHalos = header.__getitem__('Nhalos_Total') # Second thing read in
# Tree_NHalos = header.__getitem__('NHalos_per_tree') 
# ParticleMass = header.__getitem__('Part_Mass') 
NumSimTreeFiles = header.__getitem__('NumFiles')

## 
SnapNum = tree_data['TreeHalos/SnapNum']
FileNr = header.__getitem__('NumFiles') ## Only have outputs w/ 1 tree file atm, not sure where parameter for file number will be stored if at all
SubhaloIndex = tree_data['TreeHalos/TreeID']
# SubHalfMass = tree_data['TreeHalos/######']  

## Merger tree pointers
Descendant = list(tree_data['TreeHalos/TreeDescendant'])
FirstProgenitor = list(tree_data['TreeHalos/TreeFirstProgenitor'])
NextProgenitor = list(tree_data['TreeHalos/TreeNextProgenitor'])
FirstHaloInFOFgroup = list(tree_data['TreeHalos/TreeFirstHaloInFOFgroup'])
NextHaloInFOFgroup = list(tree_data['TreeHalos/TreeNextHaloInFOFgroup'])



##Sub halo Properties

Len = list(tree_data['TreeHalos/SubhaloLen']) ## tree_data['TreeTable/Length']
Mvir = list(tree_data['TreeHalos/Group_M_Crit200'])
Pos = list(tree_data['TreeHalos/SubhaloPos'])
Vel = list(tree_data['TreeHalos/SubhaloVel'])
VelDisp = list(tree_data['TreeHalos/SubhaloVelDisp'])
Vmax = list(tree_data['TreeHalos/SubhaloVmax'])
Spin = list(tree_data['TreeHalos/SubhaloSpin'])
MostBoundID = list(tree_data['TreeHalos/SubhaloIDMostbound'])

print('finished reading variables')