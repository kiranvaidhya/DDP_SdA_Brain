# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 11:42:21 2015

@author: kiran
"""

import itk
import numpy as np

path = '../BRATS/Normalised_Testing/'
outputs = []
for subdir, dirs, files in os.walk(path):
        for file1 in files:
            if 'output' in file1:
                outputs.append[subdir+'/'+file1]

image_type = itk.Image[itk.F,3]
writer = itk.ImageFileWriter[image_type].New()
itk_py_converter = itk.PyBuffer[image_type]            

outputPath = 'output/'
for i in xrange(len(outputs)):
    a=np.load(outputs[i])
    a=a.reshape(155,240,240) 
    output_image = itk_py_converter.GetImageFromArray(a.tolist())
    writer.SetFileName(outputPath + 'output_'+str(i)+'_.mha')
    writer.SetInput(output_image)
    writer.Update()