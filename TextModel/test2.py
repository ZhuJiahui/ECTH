#coding:utf-8
'''
Created on 2015年5月31日

@author: ZhuJiahui506
'''
import os
import time
import numpy as np
from TextToolkit import quick_write_list_to_text, get_text_to_single_list

def get_stat(read_directory1):
    
    file_number = sum([len(files) for root, dirs, files in os.walk(read_directory1)])
    
    #all_count = []
    
    for i in range(70, 80):
        all_tag = []
        get_text_to_single_list(all_tag, read_directory1 + '/' + str(i) + '.txt')
        
        this_count = 0
        for each in all_tag:
            if each.strip() == "41":
                this_count += 1
                
        #all_count.append(str(this_count))
        print np.true_divide(this_count, len(all_tag))

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory1 = root_directory + u'dataset/text_model/class_tag'
    
    get_stat(read_directory1)
    
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'