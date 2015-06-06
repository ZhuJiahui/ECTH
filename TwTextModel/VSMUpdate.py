# -*- coding: utf-8 -*-
'''
Created on 2014年12月28日

@author: ZhuJiahui506
'''

import os
import time
import numpy as np
from TextToolkit import quick_write_list_to_text, get_text_to_single_list


'''
Step 8
Generate the Vector Space Model.
'''

def vsm_update(read_directory1, read_directory2, read_directory3, write_directory1, write_directory2, write_directory3):
    '''
    
    :param read_directory:
    :param write_directory:
    '''

    file_number = sum([len(files) for root, dirs, files in os.walk(read_directory1)])
    
    for i in range(file_number):
        
        update_vsm = []
        vsm = []
        update_time = []
        pre_time = []
        update_tag = []
        pre_tag = []
        
        get_text_to_single_list(vsm, read_directory1 + '/' + str(i + 1) + '.txt')
        get_text_to_single_list(pre_time, read_directory2 + '/' + str(i + 1) + '.txt')
        get_text_to_single_list(pre_tag, read_directory3 + '/' + str(i + 1) + '.txt')
        
        for j in range(len(vsm)):
            str_vsm = vsm[j].split()
            float_vsm = [float(x) for x in str_vsm]
            if np.sum(float_vsm) > 0.1:               
                update_vsm.append(vsm[j])
                update_time.append(pre_time[j])
                update_tag.append(pre_tag[j])
        
        quick_write_list_to_text(update_vsm, write_directory1 + '/' + str(i + 1) + '.txt')
        quick_write_list_to_text(update_time, write_directory2 + '/' + str(i + 1) + '.txt')
        quick_write_list_to_text(update_tag, write_directory3 + '/' + str(i + 1) + '.txt')
        
        print "Segment %d Completed." % (i + 1)

if __name__ == "__main__":

    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'

    read_directory1 = root_directory + u'dataset2/text_model/vsm'
    read_directory2 = root_directory + u'dataset2/text_model/time'
    read_directory3 = root_directory + u'dataset2/text_model/class_tag'
    write_directory1 = root_directory + u'dataset2/text_model/update_vsm'
    write_directory2 = root_directory + u'dataset2/text_model/update_time'
    write_directory3 = root_directory + u'dataset2/text_model/update_class_tag'
    
    if (not(os.path.exists(write_directory1))):
        os.mkdir(write_directory1)
    
    if (not(os.path.exists(write_directory2))):
        os.mkdir(write_directory2)
    
    if (not(os.path.exists(write_directory3))):
        os.mkdir(write_directory3)
    
    vsm_update(read_directory1, read_directory2, read_directory3, write_directory1, write_directory2, write_directory3)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    
