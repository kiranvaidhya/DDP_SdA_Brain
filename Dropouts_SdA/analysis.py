import os
import getopt
import sys
from segment import prefix_list

truth_list = ['binary_truth_whole_tumor', 'binary_truth_tumor_core', 'binary_truth_active_tumor']

ANTSPATH = '/home/brain/ANTs/antsbin/bin/'
LABELPATH = '/media/brain/1A34723D34721BC7/BRATS/varghese/Recon_2013_data/testing'
TRUTHPATH = '/media/brain/1A34723D34721BC7/BRATS/varghese/Recon_2013_data/testing'

for prefix, truth in zip(prefix_list, truth_list):

	files = os.listdir(LABELPATH)
	LABELPATH, patients, files = os.walk(LABELPATH).next()
	#print patients
	for p in patients:
		print p
	   	imgs=os.listdir(LABELPATH+'/'+p)
	   	for i in imgs:
	   		if prefix in i and i[-3:]=='nii':
	   			classified_path=LABELPATH+'/'+p+'/'+i
	   		if truth in i :
	   			truth_path=TRUTHPATH+'/'+p+'/'+i
	            
	#    print classified_path
	#    print truth_path
	#    print(ANTSPATH+'LabelOverlapMeasures 3 ' +truth_path+' '+classified_path+' 1')
		os.system(ANTSPATH+'LabelOverlapMeasures 3 ' +truth_path+' '+classified_path+' ')


