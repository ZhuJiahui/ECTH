# -*- coding: utf-8 -*-
'''
Created on 2015年1月2日

@author: ZhuJiahui506
'''

import os
import time
from operator import itemgetter
from TimeConvert import CST_to_Unix, unCST_to_Unix

def sort_tag(read_directory, write_directory):
    
    file_list = os.listdir(read_directory)
    
    for i in range(len(file_list)):
        #print i
        f = open(read_directory + '/' + file_list[i], 'rb')
        line = f.readline()
        this_time_series = []
        this_file_texts = []
        while line:
            this_file_texts.append(line.strip())
            
            cst_time = line.strip().split(':::!:::')[-1]
            
            if cst_time.endswith("0000"):
                this_time = unCST_to_Unix(cst_time)
            else:
                #try:
                this_time = CST_to_Unix(cst_time)
                #except:
                    #print cst_time
                    #print line.strip()
                    #break

            this_time_series.append(this_time)
            
            line = f.readline()
        f.close()
        #break
        
        #文本获取完毕按时间排序
        tt = zip(this_time_series, this_file_texts)
        tt1 = sorted(tt, key = itemgetter(0))
        
        this_file_texts = []
        tt = []
        f = open(write_directory + "/" + str(i + 1) + "-" + file_list[i], 'w')
        for j in range(len(tt1) - 1):
            f.write(str(i + 1) + ":::!:::" + tt1[j][1]) 
            f.write('\n')
            
        f.write(str(i + 1) + ":::!:::" + tt1[-1][1])
        f.close()
        print "Segment %d Completed." % (i + 1)
    

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory = root_directory + u'dataset2/Twitter UGC 2013'
    
    write_directory = root_directory + u'dataset2/original_data'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    
    sort_tag(read_directory, write_directory)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    
    