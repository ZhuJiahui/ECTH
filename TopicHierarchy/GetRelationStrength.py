# -*- coding: utf-8 -*-
'''
Created on 2015年3月22日

@author: ZhuJiahui506
'''

import os
import time
import numpy as np
from TextToolkit import quick_write_list_to_text

def get_rs(read_directory, write_filename):
    
    file_number = sum([len(files) for root, dirs, files in os.walk(read_directory)])
    
    interval = 0.05
    
    segment = np.floor(1 / interval)
    
    result = np.zeros(segment)
    
    for i in range(file_number):
        strength = np.loadtxt(read_directory + '/' + str(63 + i) + '.txt')
        
        for j in range(len(strength)):
            for k in range(len(strength[0])):
                if (1 - strength[j, k]) < 0.001:
                    result[-1] += 1
                else:
                    index = np.floor(np.true_divide(strength[j, k], interval))
                    result[index] += 1
     
    str_result = [str(x) for x in result]
    quick_write_list_to_text(str_result, write_filename)
     
        

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory = root_directory + u'dataset/hierarchy10'
    write_filename = root_directory + u'dataset/10_stat.txt'
    
    get_rs(read_directory, write_filename)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    