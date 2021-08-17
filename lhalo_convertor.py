import h5py 
import numpy as np

trees = '/Users/101125182/Documents/2021/data/DM_L50_N128_output/trees.hdf5'

tree_data = h5py.File(trees, 'r')

# config = tree_data.require_group('Config').attrs
header = tree_data.require_group('Header').attrs

N_Trees = header.__getitem__('Ntrees_Total')
tot_NHalos = header.__getitem__('Nhalos_Total')
# Tree_NHalos = header.__getitem__('NHalos_per_tree') ## Not sure where value recorded, if at all
# ParticleMass = header.__getitem__('Pat_Mass') ## Not in Header
NumSimTreeFiles = header.__getitem__('NumFiles')

tree_halos = tree_data.require_group('TreeHalos')
# tree_tables = tree_data.require_group('TreeTable')
# tree_times = tree_data.require_group('TreeTimes')

snap_number = tree_halos.__getitem__('SnapNum')  ## snap_number set as array
# snap_number = list(tree_data['TreeHalos/SnapNum'])  ## list of all snap numbers for halos

