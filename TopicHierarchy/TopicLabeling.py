# -*- coding: utf-8 -*-
'''
Created on 2015年4月26日

@author: ZhuJiahui506
'''

import numpy as np

def topic_labeling0(TW_vsm, topic_labels, word_list, corpus):
    topic_num = len(TW_vsm)
    label_num = len(topic_labels)
    
    word_dict = {}
    count_dict = {}
    for i in range(len(word_list)):
        word_dict[word_dict[i]] = i
        count_dict[i] = 0
    
    total_count = 0
    # 计算每个词汇的概率
    for i in range(len(corpus)):
        for j in range(len(corpus[i])):
            this_word = int(corpus[i][j].split('||')[0])
            this_count = int(corpus[i][j].split('||')[1])
            total_count += this_count
            try:
                count_dict[this_word] += this_count
            except:
                pass
    
    topic_labels_n = []
    for i in range(label_num):
        this_line = []
        for j in range(len(topic_labels[i])):
            try:
                this_line.append(word_dict[topic_labels[i][j]])
            except:
                pass
        
        topic_labels_n.append(this_line)
    
    score_matrix = np.zeros((topic_num, label_num))
    
    for i in range(topic_num):
        for j in range(label_num):
            this_score = 0.0
            for k in range(len(topic_labels_n[j])):
                pui_theta = TW_vsm[i, topic_labels_n[j][k]]
                pui = np.true_divide(count_dict[topic_labels_n[j][k]], total_count)
                if (pui_theta > 0.0001) and (pui > 0.00001):
                    this_score += np.log2(np.true_divide(pui_theta, pui))
            
            score_matrix[i, j] = this_score
    
    

if __name__ == '__main__':
    pass