
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 17:12:53 2015

@author: subru
"""

from mha import *
from mha2 import *
import numpy as np
import os
from random import shuffle
from sklearn.feature_extraction import image
#from matplotlib import pyplot as plt

#Initialize user variables
#patch_size = 125
def U_Patch_Preprocess_recon_3D(patch_size_x=5,patch_size_y=5,patch_size_z=5,prefix='SdA',in_root='',out_root='',recon_flag=True):
    
        
    patch_pixels = patch_size_x*patch_size_y*patch_size_z
    
    pixel_offset_x = int(patch_size_x*0.5)
    pixel_offset_y = int(patch_size_y*0.5)
    pixel_offset_z = 2
    
    padding = patch_size_x/2
    #patches = np.zeros(patch_pixels*4)
    if recon_flag is True:
        recon_num = 5
    else:
        recon_num = 4
    patches = np.zeros(patch_size_x*patch_size_y*patch_size_z*recon_num)
    ground_truth = np.zeros(1)
    
    #paths to images
    path = in_root
    print path
    
    Flair = []
    T1 = []
    T2 = []
    T_1c = []
    Truth = []
    Recon=[]
    Folder = []
    
    for subdir, dirs, files in os.walk(path):
        if len(Flair) is 21:
            break
        for file1 in files:     
                
            #print file1
            if file1[-3:]=='mha' and ('Flair' in file1):
                
                Flair.append(file1)
                Folder.append(subdir+'/')
            elif file1[-3:]=='mha' and ('T1' in file1 and 'T1c' not in file1):
                T1.append(file1)
            elif file1[-3:]=='mha' and ('T2' in file1):
                T2.append(file1)
            elif file1[-3:]=='mha' and ('T1c' in file1 or 'T_1c' in file1):
                T_1c.append(file1)
            elif file1[-3:]=='mha' and 'OT' in file1:
                Truth.append(file1)            
            elif file1[-3:]=='mha' and 'Recon' in file1:
                Recon.append(file1)
                
    number_of_images = len(Flair)
    print 'Number of images : ', number_of_images
    
    
    for image_iterator in range(number_of_images):
        print 'Image number : ',image_iterator+1
        print 'Folder : ', Folder[image_iterator]
        Flair_image = new(Folder[image_iterator]+Flair[image_iterator])
        T1_image = new(Folder[image_iterator]+T1[image_iterator])
        T2_image = new(Folder[image_iterator]+T2[image_iterator])
        T_1c_image = new(Folder[image_iterator]+T_1c[image_iterator])
        if recon_flag is True:
            Recon_image = new(Folder[image_iterator]+Recon[image_iterator])
        try:
            Truth_image = new(Folder[image_iterator]+Truth[image_iterator])
        except:
            Truth_image = new2(Folder[image_iterator]+Truth[image_iterator])
        
        Flair_image = Flair_image.data
        T1_image = T1_image.data
        T2_image = T2_image.data
        T_1c_image = T_1c_image.data
        if recon_flag is True:
            Recon_image=Recon_image.data
        Truth_image = Truth_image.data
        ######################################################################
        ##################Converting truth####################################
        # new_Truth_image = np.zeros(Truth_image.shape,dtype=int)
        # new_Truth_image[np.where(Truth_image==0)] = 0
        # new_Truth_image[np.where(Truth_image==1)] = 4
        # new_Truth_image[np.where(Truth_image==2)] = 1
        # new_Truth_image[np.where(Truth_image==3)] = 3
        # new_Truth_image[np.where(Truth_image==4)] = 2
        # Truth_image = new_Truth_image
        ######################################################################
        
        x_span,y_span,z_span = np.where(Truth_image!=0)
        x_start = np.min(x_span) - padding
        x_stop = np.max(x_span) + padding+1
        y_start = np.min(y_span) - padding
        y_stop = np.max(y_span) + padding+1
        z_start = np.min(z_span) - padding
        z_stop = np.max(z_span) +padding+1
        
        Flair_patch = image.extract_patches(Flair_image[x_start:x_stop, y_start:y_stop, z_start:z_stop], [patch_size_x,patch_size_y,patch_size_z],(pixel_offset_x,pixel_offset_y,pixel_offset_z))
        T1_patch = image.extract_patches(T1_image[x_start:x_stop, y_start:y_stop, z_start:z_stop], [patch_size_x,patch_size_y,patch_size_z],(pixel_offset_x,pixel_offset_y,pixel_offset_z))
        T2_patch = image.extract_patches(T2_image[x_start:x_stop, y_start:y_stop, z_start:z_stop], [patch_size_x,patch_size_y,patch_size_z],(pixel_offset_x,pixel_offset_y,pixel_offset_z))
        T_1c_patch = image.extract_patches(T_1c_image[x_start:x_stop, y_start:y_stop, z_start:z_stop], [patch_size_x,patch_size_y,patch_size_z],(pixel_offset_x,pixel_offset_y,pixel_offset_z))
        if recon_flag is True:        
            Recon_patch = image.extract_patches(Recon_image[x_start:x_stop, y_start:y_stop, z_start:z_stop], [patch_size_x,patch_size_y,patch_size_z],(pixel_offset_x,pixel_offset_y,pixel_offset_z))
        Truth_patch = image.extract_patches(Truth_image[x_start:x_stop, y_start:y_stop, z_start:z_stop], [patch_size_x,patch_size_y,patch_size_z],(pixel_offset_x,pixel_offset_y,pixel_offset_z))
        
        print 'Raw patches extracted'    
        
        Flair_patch = Flair_patch.reshape(Flair_patch.shape[0]*Flair_patch.shape[1]*Flair_patch.shape[2], patch_size_x*patch_size_y*patch_size_z)
        T1_patch = T1_patch.reshape(T1_patch.shape[0]*T1_patch.shape[1]*T1_patch.shape[2], patch_size_x*patch_size_y*patch_size_z)
        T2_patch = T2_patch.reshape(T2_patch.shape[0]*T2_patch.shape[1]*T2_patch.shape[2], patch_size_x*patch_size_y*patch_size_z)  
        T_1c_patch = T_1c_patch.reshape(T_1c_patch.shape[0]*T_1c_patch.shape[1]*T_1c_patch.shape[2], patch_size_x*patch_size_y*patch_size_z)
        if recon_flag is True:
            Recon_patch = Recon_patch.reshape(Recon_patch.shape[0]*Recon_patch.shape[1]*Recon_patch.shape[2], patch_size_x*patch_size_y*patch_size_z)
        Truth_patch = Truth_patch.reshape(Truth_patch.shape[0]*Truth_patch.shape[1]*Truth_patch.shape[2], patch_size_x, patch_size_y, patch_size_z)
    
        print 'Patches reshaped'    
        
        if recon_flag is True:
            slice_patch = np.concatenate([Flair_patch, T1_patch, T2_patch, T_1c_patch, Recon_patch], axis=1)
        else:
            slice_patch = np.concatenate([Flair_patch, T1_patch, T2_patch, T_1c_patch], axis=1)
        Truth_patch = Truth_patch[:,(patch_size_x-1)/2,(patch_size_y-1)/2,(patch_size_z-1)/2]
        Truth_patch = np.array(Truth_patch)
        Truth_patch = Truth_patch.reshape(len(Truth_patch),1)
        #print '3. truth dimension :', Truth_patch.shape
            
        patches = np.vstack([patches,slice_patch])
        ground_truth = np.vstack([ground_truth, Truth_patch])
        
        #######################################################################
        ##########Extracting more patches from ground truth####################
        Flair_image[x_start:x_stop, y_start:y_stop, z_start:z_stop] = 0
        Flair_patch = image.extract_patches(Flair_image, [patch_size_x,patch_size_y,patch_size_z],(pixel_offset_x,pixel_offset_y,pixel_offset_z))
        T1_patch = image.extract_patches(T1_image, [patch_size_x,patch_size_y,patch_size_z],(pixel_offset_x,pixel_offset_y,pixel_offset_z))
        T2_patch = image.extract_patches(T2_image, [patch_size_x,patch_size_y,patch_size_z],(pixel_offset_x,pixel_offset_y,pixel_offset_z))
        T_1c_patch = image.extract_patches(T_1c_image, [patch_size_x,patch_size_y,patch_size_z],(pixel_offset_x,pixel_offset_y,pixel_offset_z))
        Truth_patch = image.extract_patches(Truth_image, [patch_size_x,patch_size_y,patch_size_z],(pixel_offset_x,pixel_offset_y,pixel_offset_z))
        
        print 'New Raw patches extracted' 
        Flair_patch = Flair_patch.reshape(Flair_patch.shape[0]*Flair_patch.shape[1]*Flair_patch.shape[2], patch_size_x*patch_size_y*patch_size_z)
        T1_patch = T1_patch.reshape(T1_patch.shape[0]*T1_patch.shape[1]*T1_patch.shape[2], patch_size_x*patch_size_y*patch_size_z)
        T2_patch = T2_patch.reshape(T2_patch.shape[0]*T2_patch.shape[1]*T2_patch.shape[2], patch_size_x*patch_size_y*patch_size_z)  
        T_1c_patch = T_1c_patch.reshape(T_1c_patch.shape[0]*T_1c_patch.shape[1]*T_1c_patch.shape[2], patch_size_x*patch_size_y*patch_size_z)
        Truth_patch = Truth_patch.reshape(Truth_patch.shape[0]*Truth_patch.shape[1]*Truth_patch.shape[2], patch_size_x, patch_size_y, patch_size_z)
        
        indexx = np.where(Flair_patch[:,int(patch_size_x*patch_size_y*patch_size_z/2)]>1.5)
        indexx = indexx[0]
        shuffle(indexx)
        if len(indexx)>250:
            indexx = indexx[0:250]
            
            
        Flair_patch = Flair_patch[indexx,:]
        T1_patch = T1_patch[indexx,:]
        T2_patch = T2_patch[indexx,:]
        T_1c_patch = T_1c_patch[indexx,:]
        Truth_patch =Truth_patch[indexx, :]
        
        slice_patch = np.concatenate([Flair_patch, T1_patch, T2_patch, T_1c_patch], axis=1)
#        slice_patch = slice_patch[0,:,:]
        Truth_patch = Truth_patch[:,(patch_size_x-1)/2,(patch_size_y-1)/2,(patch_size_z-1)/2]
        Truth_patch = np.array(Truth_patch)
        Truth_patch = Truth_patch.reshape(len(Truth_patch),1)
        
        patches = np.vstack([patches,slice_patch])
        ground_truth = np.vstack([ground_truth, Truth_patch])
        print 'Extra patches added! ', len(indexx)
        print 'Patches reshaped'
        #######################################################################
    #
    #
    print 'Number of non-zeros in ground truth : ', np.sum((ground_truth!=0).astype(int))
    print 'Number of zeros in ground truth : ', np.sum((ground_truth==0).astype(int))
    
    print
    print 'No. of 1 Necrotic: ', np.sum((ground_truth==1).astype(int))
    print 'No. of 2 Edyma: ', np.sum((ground_truth==2).astype(int))
    print 'No. of 3 Non-enhancing: ', np.sum((ground_truth==3).astype(int))
    print 'No. of 4 Enhancing: ', np.sum((ground_truth==4).astype(int))
    
    ground_truth = ground_truth.reshape(len(ground_truth))
    
    #np.save('Training_patches.npy',patches)
    #np.save('Training_labels.npy',ground_truth)
    #print ground_truth.shape
    #print patches.shape
    if 'training' in out_root and recon_flag==True:
        print'... Saving the unbalanced training patches'
        np.save(out_root+'u_trainpatch_3D_'+prefix+'_.npy',patches)
        np.save(out_root+'u_trainlabel_3D_'+prefix+'_.npy',ground_truth)
    elif recon_flag==True:
        print '... Saving the unbalanced test ing patches'
        np.save(out_root+'u_validpatch_3D_'+prefix+'_.npy',patches)
        np.save(out_root+'u_validlabel_3D_'+prefix+'_.npy',ground_truth)
        
    if 'training' in out_root and recon_flag==False:
        print'... Saving the unbalanced training patches'
        np.save(out_root+'u_trainpatch_3D_'+prefix+'_.npy',patches)
        np.save(out_root+'u_trainlabel_3D_'+prefix+'_.npy',ground_truth)
    elif recon_flag==False:
        print '... Saving the unbalanced testing patches'
        np.save(out_root+'u_validpatch_3D_'+prefix+'_.npy',patches)
        np.save(out_root+'u_validlabel_3D_'+prefix+'_.npy',ground_truth)
        
