# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 19:19:06 2015

@author: administrator
"""

import os
# from medpy.io import load
from mha import *
from mha2 import *

import numpy as np
import nibabel as nib

path = '/media/brain/1A34723D34721BC7/BRATS/varghese/Recon_2013_data/testing/'

for subdir, dirs, files in os.walk(path):
    for file1 in files:
        if 'OT' in file1:
            # m,h = load(subdir+'/'+file1)
            try:
                m = new(subdir+'/'+file1)
            except:
                m = new2(subdir+'/'+file1)

            m = m.data
            print 'saving'
	    #m = m.data

            m[np.where(m!=0)] = 1   ### whole tumor

            # m[np.where(m==2)] = 0    #### for tumor core
            # m[np.where(m!=0)] = 1    ### for tumor core

            # m[np.where(m!=np.unique(m)[-1])] = 0
            # m[np.where(m!=0)] = 1

            affine = [[-1,0,0,0],[0,-1,0,0],[0,0,1,0],[0,0,0,1]]
            img = nib.Nifti1Image(m, affine)
            img.set_data_dtype(np.int32)
            nib.save(img,subdir + '/binary_truth_whole_tumor.nii')
            
            
