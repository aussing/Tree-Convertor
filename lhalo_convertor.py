import h5py 
import numpy as np

trees = '/Users/101125182/Documents/2021/data/DM_L50_N128_output/trees.hdf5'

tree_data = h5py.File(trees, 'r')

config = tree_data.require_group('Config').attrs
header = tree_data.require_group('Header').attrs


