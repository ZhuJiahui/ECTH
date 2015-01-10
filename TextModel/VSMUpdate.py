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

def vsm_to_curpus(read_directory, write_directory):
    '''
    
    :param read_directory:
    :param write_directory:
    '''

    file_number = sum([len(files) for root, dirs, files in os.walk(read_directory)])
    
    for i in range(file_number):
        
        update_vsm = []
        vsm = []
        
        get_text_to_single_list(vsm, read_directory + '/' + str(i + 1) + '.txt')
        
        for j in range(len(vsm)):
            str_vsm = vsm[j].split()
            float_vsm = [float(x) for x in str_vsm]
            if np.sum(float_vsm) > 0.1:               
                update_vsm.append(vsm[j])
        
        quick_write_list_to_text(update_vsm, write_directory + '/' + str(i + 1) + '.txt')
        
        print "Segment %d Completed." % (i + 1)

if __name__ == "__main__":

    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'

    read_directory = root_directory + u'dataset/text_model/vsm'
    write_directory = root_directory + u'dataset/text_model/update_vsm'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    
    vsm_to_curpus(read_directory, write_directory)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    
