# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 19:18:59 2015

@author: subru
"""

from segment_script import *

patch_size_x = [7,9,9,11,13]
patch_size_y = [7,9,9,11,13]
patch_size_z = [7,9,3,3,3]
#noise_type = [1,1,1,1]
hidden_layers_sizes = [[4000,1500,500,100],[5000,2000,500],[5000,2000,500],[4000,2000,500],[5000,2000,500]]
corruption_levels = [[0.2,0.3,0.4,0.3],[0.2,0.3,0.4],[0.2,0.3,0.4],[0.2,0.3,0.4],[0.2,0.3,0.4]]
prefix = ['2013_7x7x7_4000-1500-500-100_M2343','2013_9x9x9_5000-2000-500_M234','2013_9x9x3_5000-2000-500_M234','2013_11x11x3_4000-2000-500_M234','2013_13-13-3_5000-2000-500_M234']
if len(hidden_layers_sizes)!=len(corruption_levels) or len(prefix)!=len(hidden_layers_sizes):
    print 'ERROR! Lengths of hidden layers, noise, prefix doesnot match'
    patch_size_x = []
for i in xrange(len(patch_size_x)):
    if len(hidden_layers_sizes[i])!=len(corruption_levels[i]):
        continue
    segment_script(patch_size_x[i], patch_size_y[i], patch_size_z[i], hidden_layers_sizes[i], corruption_levels[i], prefix[i])
    
    
    
