# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 11:07:35 2015

@author: bmi
"""
from perfect_balance_3D import *

from B_Patch_Preprocess_recon_3D import *
from Patch_Preprocess_recon_3D import *
from test_SdA import *
from test_network import *
#from testitk import *
import os
import time
from lesion_masker import *
from binarize_output import *
from mlp2 import *
from diceplotter import *
import subprocess

testingImages = 24

prefix = 'big_run'
new_prefix = prefix + 'dropout_'
prefix_list = [new_prefix + 'Masked_RawOutput.nii' + 'WT', new_prefix + 'Masked_RawOutput.nii'+ 'TC', new_prefix + 'Masked_RawOutput.nii'+ 'AT']

# prefix_list = [prefix, prefix, prefix]

if __name__ == '__main__':
    
    root = '/home/suthirth/subru/varghese/Recon_2013_data/'
    
    patch_size_x = 11
    patch_size_y = 11
    patch_size_z = 3
    recon_flag = False
    batch_size = 100
    
    if recon_flag == True:
        n_ins = patch_size_x * patch_size_y * patch_size_z * 5
    else:
        n_ins = patch_size_x * patch_size_y * patch_size_z * 4
    n_outs = 5
    noise_type = 0
    noise_dict = {1:'Gaussian noise', 0:'Masking Noise'}
    
    ## CHECK IMAGE SHAPES FOR PRINTING WEIGHTS ##
    hidden_layers_sizes = [3000,1000,500]
    ## CHECK IMAGE SHAPES FOR PRINTING WEIGHTS ##
    corruption_levels = [0.1,0.2,0.2,0.2]
    
    test_path = root + 'testing'
    
#    prefix = 'rms_9x9x9_5000-2000-500_M222'
    
    


#    print 'Extracting  Balanaced training patches...'
#    B_Patch_Preprocess_recon_3D(patch_size_x,patch_size_y,patch_size_z,prefix,root+'training',
#                                       root+'BRATS_training_patches/',False)
#    print 'Training patches extracted!'                                      
#    
#    print 'Extracting  Balanced validation patches...'
#    B_Patch_Preprocess_recon_3D(patch_size_x,patch_size_y,patch_size_z,prefix,root+'validation',                                     
#                                      root+'BRATS_validation_patches/',False)
#    print 'Validation patches extracted!' 
#    

    # ######################## PIXEL OFFSET !!!!!!!!!!!!!!!!!!!!!!!!! @@@
    # print 'Extracting perfect Balanced Patches...'
    # perfect_balance_3D(patch_size_x, patch_size_y, patch_size_z, prefix, root+'training', root+'BRATS_training_patches/')
    # perfect_balance_3D(patch_size_x, patch_size_y, patch_size_z, prefix, root+'validation', root+'BRATS_validation_patches/')

    ############################# PIXEL OFFSET !!!!!!!!!!!!!!!!!!!!!!!!! @@@
    # print 'Extracting UnBalanced training patches...'
    # U_Patch_Preprocess_recon_3D(patch_size_x,patch_size_y,patch_size_z,prefix,root+'training',
    #                                   root+'BRATS_training_patches/',False)
    # print 'Training patches extracted!'                                      
    
    # print 'Extracting Unbalanced validation patches...'
    # U_Patch_Preprocess_recon_3D(patch_size_x,patch_size_y,patch_size_z,prefix,root+'validation',                                     
    #                                   root+'BRATS_validation_patches/',False)

    # path = '/media/brain/1A34723D34721BC7/BRATS/codes/results/'
    # for subdir, dirs, files in os.walk(path):
    #   test_num = len(dirs)+1
    #   break

    # os.mkdir('/media/brain/1A34723D34721BC7/BRATS/codes/results/test_'+str(test_num)+'_'+prefix)
    # test_root = '/media/brain/1A34723D34721BC7/BRATS/codes/results/test_'+str(test_num)+'_'+prefix+'/'
                                      
    test_root = '/home/suthirth/subru/BRATS/results/big_run_6thSep/'
    print 'Calling test_SdA...'
    
    finetune_lr = 0.01
    pretraining_epochs = 300
    pretrain_lr = 0.001
    training_epochs = 800
    
    f = open(test_root+prefix+'_params_info.txt', 'w')
    f.write( "Current date & time " + time.strftime("%c"))
    f.write('\nPrefix : '+prefix)
    f.write('\n3D Patches. Patch_size : '+str(patch_size_x)+', '+str(patch_size_y)+', '+str(patch_size_z))
    f.write('\nBatch Size : '+str(batch_size))
    f.write('\nHidden Layer Sizes : ['+', '.join(map(str,hidden_layers_sizes))+' ]')
    f.write('\nNoise Type : '+noise_dict[noise_type])
    f.write('\nCorruption Levels : ['+', '.join(map(str,corruption_levels))+' ]')
    f.write('\nNo. of pre-training epochs : '+str(pretraining_epochs))
    f.write('\nNo. of Fine-tuning epochs : '+str(training_epochs))
    f.write('\nPretraining Learning rate : '+str(pretrain_lr))
    f.write('\nFine-tuning learning rate : '+str(finetune_lr))
    f.close()
    
    # test_SdA(finetune_lr, pretraining_epochs,
    #          pretrain_lr, training_epochs,              
    #             root+'BRATS_training_patches/b_trainpatch_3D_'+prefix+'_.npy',
    #             root+'BRATS_training_patches/b_trainlabel_3D_'+prefix+'_.npy',
    #             root+'BRATS_validation_patches/b_validpatch_3D_'+prefix+'_.npy',
    #             root+'BRATS_validation_patches/b_validlabel_3D_'+prefix+'_.npy',
    #             root+'BRATS_training_patches/u_trainpatch_3D_'+prefix+'_.npy',
    #             root+'BRATS_training_patches/u_trainlabel_3D_'+prefix+'_.npy',
    #             root+'BRATS_validation_patches/u_validpatch_3D_'+prefix+'_.npy',
    #             root+'BRATS_validation_patches/u_validlabel_3D_'+prefix+'_.npy',
    #             batch_size, n_ins, n_outs, hidden_layers_sizes, test_root + prefix, corruption_levels, False, True)
                
    # print 'Network Trained and Saved!'                
                
#    test_network(test_root , prefix, test_path, patch_size_x, patch_size_y, patch_size_z, recon_flag)
#    test_path = '/home/bmi/the_real_mega/mega_test'
#    test_network(test_root , prefix, test_path, patch_size_x, patch_size_y, patch_size_z, recon_flag)

    # LesionMasker(test_path + '/' , prefix)
    # binarize(test_root, prefix + 'Masked_RawOutput.nii')

    layer_sizes = [1452,3000, 1000, 500, 5]

    dropout_rates = [[0.0,0.0, 0.3,0.3], [0.0,0.0,0.4,0.4], [0.2,0.2,0.4,0.4]]


    runMLP2(finetune_lr,
           training_epochs,
           batch_size,
           layer_sizes,
           dropout_rates[0],
           test_root + prefix + 'pre_training.pkl',
           root+'BRATS_training_patches/u_trainpatch_3D_'+prefix+'_.npy',
           root+'BRATS_training_patches/u_trainlabel_3D_'+prefix+'_.npy',
           root+'BRATS_validation_patches/u_validpatch_3D_'+prefix+'_.npy',
           root+'BRATS_validation_patches/u_validlabel_3D_'+prefix+'_.npy',
           test_root + prefix)

    # for i in xrange(len(dropout_rates)):
    #     if i == 1:
    #         break
       #  runMLP2(finetune_lr,
       #      150,
       #      batch_size,
       #      layer_sizes,
       #      dropout_rates[i],
       #      test_root + prefix + 'pre_training.pkl',
       #      root+'BRATS_training_patches/u_trainpatch_3D_'+prefix+'_.npy',
       #      root+'BRATS_training_patches/u_trainlabel_3D_'+prefix+'_.npy',
       #      root+'BRATS_validation_patches/u_validpatch_3D_'+prefix+'_.npy',
       #      root+'BRATS_validation_patches/u_validlabel_3D_'+prefix+'_.npy',
       #      test_root + prefix + '_' + str(i))
########################################################################################
    # test_network(test_root,new_prefix,test_path,11,11,3,False,3)

    # ## START OF POST-PROCESSING PIPELINE ###

    # LesionMasker(test_path + '/' , new_prefix)
    # print 'binarizing...'
    # binarize(root, new_prefix + 'Masked_RawOutput.nii')
    # print new_prefix + 'Masked_RawOutput.nii'
    # print 'binarized'

    # callString = 'python analysis.py > ' + new_prefix + '.txt'
    # print callString
    # subprocess.call(callString, shell = True)

    # calculateDice(new_prefix + '.txt', testingImages)
    
    
                

                
