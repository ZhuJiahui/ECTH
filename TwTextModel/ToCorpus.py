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

def to_curpus(read_directory1, read_directory2, write_directory):
    '''
    
    :param read_directory1:
    :param read_directory2:
    :param write_directory:
    '''

    file_number = np.sum([len(files) for root, dirs, files in os.walk(read_directory1)])
    
    for i in range(file_number):
        
        all_weibo_fenci = []
        word_space_dict = {}
        word_count = 0
        
        f = open(read_directory2 + '/' + str(i + 1) + '.txt')
        line = f.readline()
        while line:
            this_word = line.strip().split()[0]
            all_weibo_fenci.append(this_word)
            word_space_dict[this_word] = str(word_count)
            
            word_count += 1
            line = f.readline()  
        f.close()
        
        corpus = []
        
        if len(all_weibo_fenci) >= 1000:
            f = open(read_directory1 + '/' + str(i + 1) + '.txt')
            line = f.readline()
            while line:
                this_line = line.strip().split("---")
                cor_line = []
                for each in this_line:
                    word_entity = each.split(',')[0]
                    try:
                        cor_line.append(word_space_dict[word_entity])
                    except:
                        pass
                if len(cor_line) >= 1:
                    corpus.append(" ".join(cor_line))

                line = f.readline()  
            f.close()
        else:
            pass
        
        
        quick_write_list_to_text(corpus, write_directory + '/' + str(i + 1) + '.txt')
        
        print "Segment %d Completed." % (i + 1)

if __name__ == "__main__":

    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'

    read_directory1 = root_directory + u'dataset2/text_model/content1'
    read_directory2 = root_directory + u'dataset2/text_model/select_words'
    write_directory = root_directory + u'dataset2/text_model/corpus'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    
    to_curpus(read_directory1, read_directory2, write_directory)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    
