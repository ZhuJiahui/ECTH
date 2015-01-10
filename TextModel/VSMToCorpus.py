# -*- coding: utf-8 -*-
'''
Created on 2014年12月28日

@author: ZhuJiahui506
'''

import os
import time
import numpy as np
from TextToolkit import quick_write_list_to_text


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
        
        corpus = []
        
        vsm = np.loadtxt(read_directory + '/' + str(i + 1) + '.txt')
        
        for j in range(len(vsm)):
            non_zero_index = []
            for k in range(len(vsm[0])):
                if vsm[j][k] > 0.1:
                    non_zero_index.append(str(k))
            
            corpus.append(" ".join(non_zero_index))
        
        quick_write_list_to_text(corpus, write_directory + '/' + str(i + 1) + '.txt')
        
        print "Segment %d Completed." % (i + 1)

if __name__ == "__main__":

    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'

    read_directory = root_directory + u'dataset/text_model/update_vsm'
    write_directory = root_directory + u'dataset/text_model/corpus'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    
    vsm_to_curpus(read_directory, write_directory)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    
