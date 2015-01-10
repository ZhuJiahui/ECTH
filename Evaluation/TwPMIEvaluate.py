# -*- coding: utf-8 -*-
'''
Created on 2015年1月7日

@author: ZhuJiahui506
'''

import os
import numpy as np
import time

def pmi(topic_dis, w_corpus, marginal_dis):
    
    is_index = []
    for i in range(len(topic_dis)):
        if topic_dis[i] > 0.0:
            is_index.append(i)
    
    temp_sum = 0.0
    for i in range(len(is_index)):
        for j in range(i, len(is_index)):
            if i == j:
                pass
            else:
                hit_count = 0
                for k in range(len(w_corpus)):
                    if (str(is_index[i]) in w_corpus[k]) and (str(is_index[j]) in w_corpus[k]):
                        hit_count += 1
                joint_p = np.true_divide(hit_count, len(w_corpus))
                
                if joint_p <=0.000001:
                    temp_sum += 0
                else:
                    temp_sum += np.log(joint_p / marginal_dis[is_index[i]] / marginal_dis[is_index[j]])

    pmi_score = np.true_divide(2 * temp_sum, len(is_index) * (len(is_index) - 1))
    
    return pmi_score
    
if __name__ == '__main__':
    
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory1 = root_directory + u'dataset2/text_model/corpus'
    #read_directory2 = root_directory + u'dataset2/coherent_topic30/sparse_topic'
    read_directory2 = root_directory + u'dataset2/LDA/topic_word30'
    
    # 选取10片
    pmi_total = []
    for i in range(213, 218):
        w_corpus = []
        
        f = open(read_directory1 + '/' + str(i) + '.txt', 'rb')
        line = f.readline()
        while line:
            w_corpus.append(line.strip().split())
            line = f.readline()
        f.close()
        
        topic_word = np.loadtxt(read_directory2 + '/' + str(i) + '.txt')
        
        # 计算边缘概率
        marginal_dis = np.zeros(len(topic_word[0]))
    
        for i in range(len(w_corpus)):
            for j in range(len(w_corpus[i])):
                marginal_dis[int(w_corpus[i][j])] += 1.0
    
        marginal_dis = np.true_divide(marginal_dis, len(w_corpus))
        
        # 计算PMI值
        pmi_temp = []
        for j in range(len(topic_word)):
            pmi_score = pmi(topic_word[j], w_corpus, marginal_dis)
            pmi_temp.append(pmi_score)
        
        pmi_total.append(np.average(pmi_temp))
        print pmi_temp
    
    print np.average(pmi_total)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    
    