# -*- coding: utf-8 -*-
'''
Created on 2014年12月30日

@author: ZhuJiahui506
'''

import numpy as np
from operator import itemgetter

def sparse_DTvsm(DT_vsm, sp):
    '''
    分布稀疏化
    :param DT_vsm:
    :param sp:
    '''
    
    col_num = len(DT_vsm[0])

    if col_num < sp:
        return DT_vsm
    else:
        SPDT_vsm = np.zeros((len(DT_vsm), col_num))
        for i in range(len(DT_vsm)):
            sort_index = np.argsort(DT_vsm[i])
            selected_index = sort_index[(col_num - sp) :]
            selected_element = DT_vsm[i][selected_index]
            temp_sum = np.sum(selected_element)
            changed_element = np.true_divide(selected_element, temp_sum)
            SPDT_vsm[i][selected_index] = changed_element
        return SPDT_vsm

def get_real_topics(SPDT_vsm, this_word_list):
    
    real_topics = []
    
    for j in range(len(SPDT_vsm)):
        this_topic = []
        this_topic_weight = []
        
        for k in range(len(SPDT_vsm[j])):
            if SPDT_vsm[j][k] > 0.0001:
                this_topic.append(this_word_list[k])
                this_topic_weight.append(SPDT_vsm[j][k])
            
        tt = zip(this_topic, this_topic_weight)
        tt = sorted(tt, key = itemgetter(1), reverse=True)
        this_topic = []
        for each in tt:
            this_topic.append(str(each[1]) + '*' + str(each[0]))
            
        real_topics.append(" ".join(this_topic))
    
    return real_topics


def get_topic_proportion(SPDT_vsm):
    
    doc_num = len(SPDT_vsm)
    
    DT_flag = np.ceil(SPDT_vsm)
    topic_count = np.sum(DT_flag, 0)
    
    topic_proportion = np.true_divide(topic_count, doc_num)
    return topic_count, topic_proportion


if __name__ == '__main__':
    s = np.array([[1, 2,3,4,5,6,7,8,11,0,10,9]])
    a = sparse_DTvsm(s, 3)
    print a