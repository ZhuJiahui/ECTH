# -*- coding: utf-8 -*-
'''
Created on 2014年12月30日

@author: ZhuJiahui506
'''

import os
import time
import numpy as np
from TextToolkit import quick_write_list_to_text
from TopicUtil import sparse_DTvsm, get_real_topics, get_topic_proportion

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'

    read_directory = root_directory + u'dataset/topic_model25'
    read_directory2 = root_directory + u'dataset/text_model/select_words'
    write_directory = root_directory + u'dataset/coherent_topic25'
    write_directory1 = write_directory + u'/sparse_topic'
    write_directory2 = write_directory + u'/sparse_topic2'
    write_directory3 = write_directory + u'/topic_pro'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    if (not(os.path.exists(write_directory1))):
        os.mkdir(write_directory1)
    if (not(os.path.exists(write_directory2))):
        os.mkdir(write_directory2)
    if (not(os.path.exists(write_directory3))):
        os.mkdir(write_directory3)
    
    sp = 5
    sp2 = 3
    for i in range(257):
        TW_vsm = np.loadtxt(read_directory + '/' + str(i + 1) + '/pw_z.k25')
        SPTW_vsm = sparse_DTvsm(TW_vsm, sp)
        
        DT_vsm = np.loadtxt(read_directory + '/' + str(i + 1) + '/pz_d.k25')
        SPDT_vsm = sparse_DTvsm(DT_vsm, sp2)
        
        # 本片数据的词汇列表
        this_word_list = []
        f1 = open(read_directory2 + '/' + str(i + 1) + '.txt', 'rb')
        line = f1.readline()
        while line:
            this_word_list.append(line.split()[0])
            line = f1.readline()
        f1.close()
        
        real_topics = get_real_topics(SPTW_vsm, this_word_list)
        
        SPTW_to_string = []
        for j in range(len(SPTW_vsm)):
            str_line = " ".join([str(x) for x in SPTW_vsm[j]])
            SPTW_to_string.append(str_line)
        
        topic_count, topic_proportion = get_topic_proportion(SPDT_vsm)
        count_pro_tostring = []
        for j in range(len(topic_count)):
            count_pro_tostring.append(str(topic_count[j]) + " " + str(topic_proportion[j]))
        
        quick_write_list_to_text(SPTW_to_string, write_directory1 + '/' + str(i + 1) + '.txt')
        quick_write_list_to_text(real_topics, write_directory2 + '/' + str(i + 1) + '.txt')
        quick_write_list_to_text(count_pro_tostring, write_directory3 + '/' + str(i + 1) + '.txt')
    
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    