# -*- coding: utf-8 -*-
'''
Created on 2014年7月28日

@author: ZhuJiahui506
'''


import os
import numpy as np
from TextToolkit import quick_write_list_to_text
import time
from KLD import SKLD

def average_td(PHAI):
    
    W1 = np.zeros((len(PHAI), len(PHAI)))
    for j in range(len(PHAI)):
        for k in range(j, len(PHAI)):
            W1[j, k] = SKLD(PHAI[j], PHAI[k])
            W1[k, j] = W1[j, k]
    
    td = np.average(W1) / len(PHAI)
    
    return td


def compute_td(read_directory1, read_directory2, read_directory3, read_directory4, write_filename1, write_filename2, write_filename3, write_filename4):
    
    file_number = sum([len(files) for root, dirs, files in os.walk(read_directory1)])
    
    td_list1 = []
    td_list2 = []
    td_list3 = []
    td_list4 = []
    
    # at K=10, 15, 20, 25, 30
    
    for i in range(213, 223):
        PHAI1 = np.loadtxt(read_directory1 + '/' + str(i + 1) + '.txt')  #CHN-LDA
        PHAI2 = np.loadtxt(read_directory2 + '/' + str(i + 1) + '.txt')  #CHN-BTM
        PHAI3 = np.loadtxt(read_directory3 + '/' + str(i + 1) + '.txt')  #EN-LDA
        PHAI4 = np.loadtxt(read_directory4 + '/' + str(i + 1) + '.txt')  #EN-BTM
        
        if len(PHAI1) >= 300:
            PHAI1 = np.array([PHAI1])
        if len(PHAI2) >= 300:
            PHAI2 = np.array([PHAI2])
        if len(PHAI3) >= 300:
            PHAI3 = np.array([PHAI3])
        

        td1 = average_td(PHAI1)
        td2 = average_td(PHAI2)
        td3 = average_td(PHAI3)
        td4 = average_td(PHAI4)
        
        
        td_list1.append(str(td1))
        td_list2.append(str(td2))
        td_list3.append(str(td3))
        td_list4.append(str(td4))
    
    quick_write_list_to_text(td_list1, write_filename1)
    quick_write_list_to_text(td_list2, write_filename2)
    quick_write_list_to_text(td_list3, write_filename3)
    quick_write_list_to_text(td_list4, write_filename4)
        

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory1 = root_directory + u'dataset/LDA/topic_word20'
    read_directory2 = root_directory + u'dataset/coherent_topic20/sparse_topic'
    read_directory3 = root_directory + u'dataset2/LDA/topic_word20'
    read_directory4 = root_directory + u'dataset2/coherent_topic20/sparse_topic'
    
    write_filename1 = root_directory + u'dataset/evaluation/lda_td.txt'
    write_filename2 = root_directory + u'dataset/evaluation/btm_td.txt'
    write_filename3 = root_directory + u'dataset2/evaluation/lda_td.txt'
    write_filename4 = root_directory + u'dataset2/evaluation/btm_td.txt'
    
    compute_td(read_directory1, read_directory2, read_directory3, read_directory4, write_filename1, write_filename2, write_filename3, write_filename4)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'

    