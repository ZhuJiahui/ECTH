# -*- coding: utf-8 -*-
'''
Created on 2014年5月6日

@author: ZhuJiahui506
'''

import os
import time
from operator import itemgetter
from TextToolkit import quick_write_list_to_text, get_text_to_complex_list,\
    get_text_to_single_list

'''
Step 5
Count TF
'''

def batch_count_tf(read_directory1, read_directory2, write_directory, write_directory2):
    '''
    
    :param read_directory1:
    :param read_directory2:
    :param write_directory:
    '''

    
    file_number = sum([len(files) for root, dirs, files in os.walk(read_directory1)])
    
    for i in range(file_number):
        #each_weibo_fenci = [] 
        all_weibo_fenci = []
        
        #get_text_to_complex_list(each_weibo_fenci, read_directory1 + '/' + str(i + 1) + '.txt', 0)
        get_text_to_single_list(all_weibo_fenci, read_directory2 + '/' + str(i + 1) + '.txt')
        
        '''
        '''
        
        tf_dict = {}  #词频TF字典
        for key in all_weibo_fenci:
            tf_dict[key.strip()] = 0
        
        
        f = open(read_directory1 + '/' + str(i + 1) + '.txt')
        line = f.readline()
        while line:
            
            this_row = line.strip().split('---')

            for j in range(len(this_row)):
                try:
                    tf_dict[this_row[j].split(',')[0].strip()] += 1
                except KeyError:
                    tf_dict[this_row[j].split(',')[0].strip()] += 0

            line = f.readline()  
        f.close()
        
        
        #词频列表
        value_list = []
        for key in all_weibo_fenci:
            value_list.append(tf_dict[key])
        
        # 按词频降序排序
        va = zip(all_weibo_fenci, value_list)
        va = sorted(va, key = itemgetter(1), reverse = True)    
        
        #result_all = []
        result_top = []
        container = []
        #r_count = 1
        for each in va:
            if each[0] not in container:
                #result_all.append(each[0] + " " + str(each[1]))
                container.append(each[0])
                if len(container) <= 500:
                    result_top.append(each[0] + "---" + str(each[1]))
                else:
                    break
                    #r_count += 1
        
        quick_write_list_to_text(container, write_directory + '/' + str(i + 1) + '.txt')
        quick_write_list_to_text(result_top, write_directory2 + '/' + str(i + 1) + '.txt')
        
        print "Segment %d Completed." % (i + 1)

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory1 = root_directory + u'dataset2/text_model2/content1'
    read_directory2 = root_directory + u'dataset2/text_model2/all_weibo_word'
    write_directory = root_directory + u'dataset2/text_model2/tf_all'
    write_directory2 = root_directory + u'dataset2/text_model2/select_words'


    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    if (not(os.path.exists(write_directory2))):
        os.mkdir(write_directory2)
    
    batch_count_tf(read_directory1, read_directory2, write_directory, write_directory2)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    