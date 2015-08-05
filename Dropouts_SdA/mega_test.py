from test_network import *
from lesion_masker import *

prefix = '2013new_9x9x9_5000-2000-500_M244'
root = '/media/varkey/mega_test/HGG_NORM/'
test_root = '/home/bmi/BRATS/results/test_147_2013new_9x9x9_5000-2000-500_M244/'
test_path = root

test_network(test_root,prefix,test_path,9,9,9,False,3)
#LesionMasker(prefix, test_path)

