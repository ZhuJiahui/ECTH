# -*- coding: utf-8 -*-
'''
Created on 2014年5月5日

@author: ZhuJiahui506
'''
import os
import time
import re
from TextToolkit import quick_write_list_to_text
from TimeConvert import unCST_to_Unix, CST_to_Unix

'''
Step 4
Word segmentation of the high quality data.Also get its id,time and class tag.
'''

def tw_word_segment(read_directory, write_directory1, write_directory2, write_directory3, write_directory4, write_directory5):
    '''
    
    :param read_directory:
    :param write_directory1:
    :param write_directory2:
    :param write_directory3:
    :param write_directory4:
    :param write_directory5:
    '''
    
    file_number = sum([len(files) for root, dirs, files in os.walk(read_directory)])
    for i in range(file_number):
        time_series = []
        class_tag = []
        
        content_with_tag = []
        content_without_tag = []
        
        all_weibo_word = []
        
        f = open(read_directory + '/' + str(i + 1) + '.txt', 'rb')
        line = f.readline()
        while line:
            this_line = line.strip().split(':::!:::')

            try:
                this_text = this_line[2]
            except:
                this_text = " "
            
            pattern = r"\([^\(\)]+\)"
            pro_text = re.findall(pattern, this_text)
            
            if len(pro_text) > 5:           
                wd_with_tag = []
                wd_without_tag = []
                for each in pro_text:
                    tp = each[1 : -1].split(',')
                    wd = tp[0].strip()
                    wtg = tp[1].strip()
                    wd_with_tag.append(wd + "," + wtg)
                    wd_without_tag.append(wd)
            
                # 此处的词汇带有词性标注
                for word in set(wd_with_tag).difference(all_weibo_word):
                    if word not in all_weibo_word:
                        all_weibo_word.append(word)
            
                content_with_tag.append("---".join(wd_with_tag))
                content_without_tag.append("---".join(wd_without_tag))
                
                cst_time = this_line[-1]
            
                if cst_time.endswith("0000"):
                    this_time = unCST_to_Unix(cst_time)
                else:
                    this_time = CST_to_Unix(cst_time)
                
                time_series.append(str(this_time))
            
                class_tag.append(this_line[0])
            
            line = f.readline()
        f.close()
        
        quick_write_list_to_text(time_series, write_directory1 + '/' + str(i + 1) + '.txt')
        quick_write_list_to_text(content_with_tag, write_directory2 + '/' + str(i + 1) + '.txt')
        quick_write_list_to_text(content_without_tag, write_directory3 + '/' + str(i + 1) + '.txt')
        quick_write_list_to_text(class_tag, write_directory4 + '/' + str(i + 1) + '.txt')
        quick_write_list_to_text(all_weibo_word, write_directory5 + '/' + str(i + 1) + '.txt')
        
        print "Segment %d Completed." % (i + 1)

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory = root_directory + u'dataset2/segment'
    write_directory = root_directory + u'dataset2/text_model'
    write_directory1 = root_directory + u'dataset2/text_model/time'
    write_directory2 = root_directory + u'dataset2/text_model/content1'
    write_directory3 = root_directory + u'dataset2/text_model/content2'
    write_directory4 = root_directory + u'dataset2/text_model/class_tag'
    write_directory5 = root_directory + u'dataset2/text_model/all_weibo_word'

    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
        os.mkdir(write_directory1)
        os.mkdir(write_directory2)
        os.mkdir(write_directory3)
        os.mkdir(write_directory4)
        os.mkdir(write_directory5)
        
    if (not(os.path.exists(write_directory1))):
        os.mkdir(write_directory1)
    if (not(os.path.exists(write_directory2))):
        os.mkdir(write_directory2)   
    if (not(os.path.exists(write_directory3))):
        os.mkdir(write_directory3)
    if (not(os.path.exists(write_directory4))):
        os.mkdir(write_directory4)
    if (not(os.path.exists(write_directory5))):
        os.mkdir(write_directory5)
    
    tw_word_segment(read_directory, write_directory1, write_directory2, write_directory3, write_directory4, write_directory5)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    