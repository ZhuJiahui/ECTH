# -*- coding: utf-8 -*-
'''
Created on 2014年12月27日

@author: ZhuJiahui506
'''
import os
import time
from TextToolkit import quick_write_list_to_text

'''
Step 3
Compute EM weight of each Weibo and ordered by its EM weights to generate the high quality data. 
So the original data was changed.
'''


def generate_high_quality_data(read_directory, write_directory):
    '''
    Linear fusion
    :param read_directory:
    :param write_directory:
    '''
    #K = 3000

    file_number = sum([len(files) for root, dirs, files in os.walk(read_directory)])
    for i in range(file_number):
        
        this_weibo = []
        
        f = open(read_directory + '/' + str(i + 1) + '.txt', 'r')
        line = f.readline()
        while line:
            each_line = line.strip()
            this_text_length = " "
            try:
                this_text_length = each_line.split('\t')[6]
            except:
                this_text_length = " "
                
            if len(this_text_length) >= 150:
                this_weibo.append(each_line)
            
            line = f.readline()
        f.close()
        
        quick_write_list_to_text(this_weibo, write_directory + '/' + str(i + 1) + '.txt')
        
    
if __name__ == '__main__':
    start = time.clock()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory = root_directory + u'dataset/segment'
    write_directory = root_directory + u'dataset/high_quality_data'

    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    
    generate_high_quality_data(read_directory, write_directory)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    