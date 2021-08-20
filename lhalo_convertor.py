import h5py 
import numpy as np

trees = '/Users/101125182/Documents/2021/data/DM_L50_N128_output/trees.hdf5'

tree_data = h5py.File(trees, 'r')

## Header Properties
header = tree_data.require_group('Header').attrs
N_Trees = header.__getitem__('Ntrees_Total')  #first thing to be read in
tot_NHalos = header.__getitem__('Nhalos_Total') # Second thing read in
# Tree_NHalos = header.__getitem__('NHalos_per_tree') 
# ParticleMass = header.__getitem__('Pat_Mass') 
NumSimTreeFiles = header.__getitem__('NumFiles')

## 
SnapNum = tree_data['TreeHalos/SnapNum']
FileNr = header.__getitem__('NumFiles') ## Only have outputs w/ 1 tree file atm, not sure where parameter for file number will be stored if at all
SubhaloIndex = tree_data['TreeHalos/TreeID']
SubHalfMass = tree_data['####']  

## Merger tree pointers
Descendant = tree_data['TreeHalos/TreeDescendant']
FirstProgenitor = tree_data['TreeHalos/TreeFirstProgenitor']
NextProgenitor = tree_data['TreeHalos/TreeNextProgenitor']
FirstHaloInFOFgroup = tree_data['TreeHalos/FirstHaloInFOFGroup']
NextHaloInFOFgroup = tree_data['TreeHalos/NextHaloInFOFGroup']


##Sub halo Properties

Len = tree_data['TreeHalos/Len']
Mvir = tree_data['TreeHalos/Group_M_Crit200']
Pos = tree_data['TreeHalos/SubhaloPos']
Vel = tree_data['TreeHalos/SubhaloVel']
VelDisp = tree_data['TreeHalos/SubhaloVelDisp']
Vmax = tree_data['TreeHalos/SubhaloVmax']
Spin = tree_data['TreeHalos/SubhaloSpin']
MostBoundID = tree_data['TreeHalos/SubhaloIDMostBound']

