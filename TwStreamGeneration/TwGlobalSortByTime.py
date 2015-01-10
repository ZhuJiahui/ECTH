# -*- coding: utf-8 -*-
'''
Created on 2014年7月22日

@author: ZhuJiahui506
'''
import os
import time
from operator import itemgetter
from TextToolkit import quick_write_list_to_text
from TimeConvert import CST_to_Unix, unCST_to_Unix


def get_time_range(read_directory):
    '''
    最初时间与最后时间
    :param read_directory:
    '''
    time_series = []
    each_time_interval = []
    
    #file_number = sum([len(files) for root, dirs, files in os.walk(read_directory)])
    file_list = os.listdir(read_directory)
    
    for i in range(len(file_list)):
        #print i
        f = open(read_directory + '/' + file_list[i], 'rb')
        line = f.readline()
        this_time_series = []
        while line:
            cst_time = line.strip().split(':::!:::')[-1]
            
            if cst_time.endswith("0000"):
                this_time = unCST_to_Unix(cst_time)
            else:
                this_time = CST_to_Unix(cst_time)
            
            time_series.append(this_time)
            this_time_series.append(this_time)
            
            line = f.readline()
        f.close()
        
        each_time_interval.append([this_time_series[0], this_time_series[-1]])
    
    #升序排序
    time_series = sorted(time_series)
    
    start_time = time_series[0]
    final_time = time_series[-1]
    
    print "The start time is: %f." % start_time
    print "The final time is: %f." % final_time
    return start_time, final_time, each_time_interval

def global_sort_by_time(start_time, final_time, each_time_interval, read_directory, write_directory):
    
    print "Begin sorting." 
    print "May take a long time, Please Wait..."

    file_list2 = os.listdir(read_directory)

    #start_time = 1388505600  # 2014/01/01 0:00
    
    start_time = int(start_time + 28800) / 86400 * 86400 - 28800
    segment_interval = 86400 * 2
    
    file_number = 1
    
    while start_time <= final_time:
        this_time_series = []
        this_file_texts = []
        
        print "Segment %d ." % file_number
        
        for i in range(len(file_list2)):
            
            if (start_time >= each_time_interval[i][0] and start_time <= each_time_interval[i][1]) or ((start_time + segment_interval) > each_time_interval[i][0] and (start_time + segment_interval) < each_time_interval[i][1]):
                 
                f = open(read_directory + '/' + file_list2[i], 'rb')
                line = f.readline()
                while line:
                    cst_time = line.strip().split(':::!:::')[-1]
            
                    if cst_time.endswith("0000"):
                        this_time = unCST_to_Unix(cst_time)
                    else:
                        this_time = CST_to_Unix(cst_time)
                
                    if this_time < (start_time + segment_interval) and this_time >= start_time:
                        this_time_series.append(this_time)
                        this_file_texts.append(line.strip())
                    elif this_time >= (start_time + segment_interval):
                        break
                    else:
                        pass

                    line = f.readline()

                f.close()
        
        #文本获取完毕按时间排序
        tt = zip(this_time_series, this_file_texts)
        tt1 = sorted(tt, key = itemgetter(0))
        
        this_file_texts = []
        for each in tt1:
            this_file_texts.append(each[1])
        
        quick_write_list_to_text(this_file_texts, write_directory + "/" + str(file_number) + ".txt")
        
        file_number = file_number + 1
        start_time = start_time + segment_interval
    
    print "Global Sort Complete!!!"
    print "Total Segment %d ." % (file_number - 1)
    

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory = root_directory + u'dataset2/original_data'
    
    write_directory = root_directory + u'dataset2/segment'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    
    start_time, final_time, each_time_interval = get_time_range(read_directory)
        
    global_sort_by_time(start_time, final_time, each_time_interval, read_directory, write_directory)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    
