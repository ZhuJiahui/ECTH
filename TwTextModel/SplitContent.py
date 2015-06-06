# -*- coding: utf-8 -*-
'''
Created on 2015年5月4日

@author: ZhuJiahui506
'''
import os
import time
from TextToolkit import get_text_to_single_list, quick_write_list_to_text

def split_content(read_directory1, read_directory2, read_directory3, read_directory4, read_directory5, write_directory1, write_directory2, write_directory3, write_directory4, write_directory5):
    
    file_number = sum([len(files) for root, dirs, files in os.walk(read_directory1)])
    
    first_time = []
    get_text_to_single_list(first_time, read_directory1 + '/1.txt')
    
    start_time = int(float(first_time[0]) + 28800) / 86400 * 86400 - 28800
    segment_interval = 86400 * 2
    
    for i in range(file_number):
        this_time = []
        this_content1 = []
        this_content2 = []
        this_class_tag = []
        this_all_weibo_word = []
        
        get_text_to_single_list(this_time, read_directory1 + "/" + str(i + 1) + ".txt")
        get_text_to_single_list(this_content1, read_directory2 + "/" + str(i + 1) + ".txt")
        get_text_to_single_list(this_content2, read_directory3 + "/" + str(i + 1) + ".txt")
        get_text_to_single_list(this_class_tag, read_directory4 + "/" + str(i + 1) + ".txt")
        get_text_to_single_list(this_all_weibo_word, read_directory5 + "/" + str(i + 1) + ".txt")
        
        if len(this_time) == 0:
            quick_write_list_to_text([], write_directory1 + "/" + str(2 * i + 1) + ".txt")
            quick_write_list_to_text([], write_directory2 + "/" + str(2 * i + 1) + ".txt")
            quick_write_list_to_text([], write_directory3 + "/" + str(2 * i + 1) + ".txt")
            quick_write_list_to_text([], write_directory4 + "/" + str(2 * i + 1) + ".txt")
            quick_write_list_to_text([], write_directory5 + "/" + str(2 * i + 1) + ".txt")

            quick_write_list_to_text([], write_directory1 + "/" + str(2 * i + 2) + ".txt")
            quick_write_list_to_text([], write_directory2 + "/" + str(2 * i + 2) + ".txt")
            quick_write_list_to_text([], write_directory3 + "/" + str(2 * i + 2) + ".txt")
            quick_write_list_to_text([], write_directory4 + "/" + str(2 * i + 2) + ".txt")
            quick_write_list_to_text([], write_directory5 + "/" + str(2 * i + 2) + ".txt")
        else:
            split_index = 0
            for j in range(len(this_time)):
                if (float(this_time[j]) < float(start_time + 86400)):
                    split_index += 1
                else:
                    break
            
            quick_write_list_to_text(this_time[0 : split_index], write_directory1 + "/" + str(2 * i + 1) + ".txt")
            quick_write_list_to_text(this_content1[0 : split_index], write_directory2 + "/" + str(2 * i + 1) + ".txt")
            quick_write_list_to_text(this_content2[0 : split_index], write_directory3 + "/" + str(2 * i + 1) + ".txt")
            quick_write_list_to_text(this_class_tag[0 : split_index], write_directory4 + "/" + str(2 * i + 1) + ".txt")
            quick_write_list_to_text(this_all_weibo_word, write_directory5 + "/" + str(2 * i + 1) + ".txt")

            quick_write_list_to_text(this_time[split_index:], write_directory1 + "/" + str(2 * i + 2) + ".txt")
            quick_write_list_to_text(this_content1[split_index:], write_directory2 + "/" + str(2 * i + 2) + ".txt")
            quick_write_list_to_text(this_content2[split_index:], write_directory3 + "/" + str(2 * i + 2) + ".txt")
            quick_write_list_to_text(this_class_tag[split_index:], write_directory4 + "/" + str(2 * i + 2) + ".txt")
            quick_write_list_to_text(this_all_weibo_word, write_directory5 + "/" + str(2 * i + 2) + ".txt")
            
        start_time = start_time + segment_interval
          
    
    
if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory1 = root_directory + u'dataset2/text_model/time'
    read_directory2 = root_directory + u'dataset2/text_model/content1'
    read_directory3 = root_directory + u'dataset2/text_model/content2'
    read_directory4 = root_directory + u'dataset2/text_model/class_tag'
    read_directory5 = root_directory + u'dataset2/text_model/all_weibo_word'
    
    write_directory = root_directory + u'dataset2/text_model2'
    write_directory1 = root_directory + u'dataset2/text_model2/time'
    write_directory2 = root_directory + u'dataset2/text_model2/content1'
    write_directory3 = root_directory + u'dataset2/text_model2/content2'
    write_directory4 = root_directory + u'dataset2/text_model2/class_tag'
    write_directory5 = root_directory + u'dataset2/text_model2/all_weibo_word'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
        os.mkdir(write_directory1)
        os.mkdir(write_directory2)
        os.mkdir(write_directory3)
        os.mkdir(write_directory4)
        os.mkdir(write_directory5)
    
    split_content(read_directory1, read_directory2, read_directory3, read_directory4, read_directory5, write_directory1, write_directory2, write_directory3, write_directory4, write_directory5)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'