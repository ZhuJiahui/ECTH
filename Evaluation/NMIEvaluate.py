# -*- coding: utf-8 -*-
'''
Created on 2015年1月7日

@author: ZhuJiahui506
'''

import os
import numpy as np
import time


def joint_p_tw(topic_word, j, k):
    pij = 0.0
    for i in range(len(topic_word)):
        pij += (topic_word[i][j] * topic_word[i][k])
    
    return pij

def H_entropy(x):
    Ha = 0.0
    for i in range(len(x)):
        if x[i] <= 0.000001:
            pass
        else:
            Ha += (-1 * x[i] * np.log2(x[i]))
    
    return Ha

def nmi(topic_word):
    
    topic_num = len(topic_word)
    word_num = len(topic_word[0])
    
    marginal_dis = np.average(topic_word, 0)
    
    nmi_score = []
    for i in range(topic_num):
        for j in range(i, topic_num):
            if i == j:
                pass
            else:
                # 每一对之间进行互信息运算
                Ipq = 0.0
                for p in range(word_num):
                    for q in range(p, word_num):
                        if p == q:
                            pass
                        else:
                            if (topic_word[i][p] <= 0.000001) or (topic_word[j][q] <= 0.000001):
                                pass
                            else:
                                joint_p = joint_p_tw(topic_word, p, q)
                                if joint_p <= 0.00001:
                                    Ipq += 0
                                else:
                                    Ipq += (joint_p * (np.log(joint_p) - np.log(marginal_dis[p] * marginal_dis[q])))
                
                Ha = H_entropy(topic_word[i])
                Hb = H_entropy(topic_word[j])
                
                nmi_ij = 2 * Ipq / (Ha + Hb)
                nmi_score.append(nmi_ij)
    
    avg_nmi = np.average(nmi_score)
    
    return avg_nmi

if __name__ == '__main__':

    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    #read_directory1 = root_directory + u'dataset/text_model/corpus'
    read_directory = root_directory + u'dataset/coherent_topic20/sparse_topic'
    #read_directory2 = root_directory + u'dataset/LDA/topic_word30'
    
    tw = np.loadtxt(read_directory + '/' + str(69) + '.txt')
    
    #cluster_dis = [[2, 5, 13, 14], [9, 15, 16, 19], [0, 1, 3, 4, 6, 7, 8, 10, 11, 12, 17, 18]]
    #cluster_dis = [[1, 7, 10, 12, 15, 17, 19], [0, 2, 9, 14, 16], [3, 4, 5, 6, 8, 11, 13, 18]]
    #cluster_dis = [[0, 1, 3, 4, 9, 13, 14, 15], [2, 5, 6, 7, 8, 10, 11, 12, 16, 17, 18, 19]]
    #cluster_dis = [[0, 17], [5, 7], [4, 8], [11, 16], [1, 2, 13, 15, 18], [3, 6, 9, 10, 12, 14, 19]]
    #cluster_dis = [[0, 10], [2, 7], [6, 13], [12, 19], [1, 4, 5, 11], [8, 14, 17], [3, 9, 15, 16, 18]]
    #cluster_dis = [[0, 3, 9, 19], [4, 13, 14, 15], [1, 2, 5, 8, 10], [6, 7, 11, 12, 16, 17, 18]]
    #cluster_dis = [[0, 1, 4, 17], [2, 5, 11, 14], [7, 12, 13, 16], [3, 10, 18, 19], [6, 8, 9, 15]]
    #cluster_dis = [[0, 6], [3, 5], [4, 10], [13, 19], [1, 2, 8, 15], [7, 14, 16, 18], [9, 11, 12, 17]]
    #cluster_dis = [[1, 4, 13, 18], [8, 9, 11, 16], [2, 6], [17, 19], [0, 3, 5, 12], [7, 10, 14, 15]]
    #cluster_dis = [[0, 8], [1, 4], [3, 11], [7, 9], [2, 5, 18, 19], [14, 16, 17], [6, 10, 15], [12, 13]]
    
    #cluster_dis = [[0, 1, 6, 9, 10, 15], [2], [3], [4, 5, 12, 17, 19], [7, 8, 11, 13, 14], [16], [18]]
    #cluster_dis = [[1], [12], [7, 10, 15], [2, 9], [14], [0, 16, 17], [3, 4, 5, 6, 8, 11, 13, 18, 19]]
    #cluster_dis = [[5, 11, 17, 19], [12], [10, 16], [2, 7, 18], [6, 8], [0, 1, 3, 4, 9, 13, 14, 15]]
    #cluster_dis = [[3, 6, 9, 19], [12], [10, 14], [1], [2, 5], [13, 18], [0, 4, 5, 7, 8, 11, 16, 17]]
    #cluster_dis = [[1, 4, 5, 11], [14], [8, 17], [9], [15, 16], [3, 18], [0, 2, 6, 7, 10, 12, 13, 19]]
    #cluster_dis = [[4, 11], [8], [3, 7], [9, 10, 13, 14, 15, 16, 18], [1, 2, 5, 12, 17], [19], [0], [6]]
    #cluster_dis = [[1], [12], [7, 10, 15], [2, 9], [14], [0, 16, 17], [3, 4, 5, 6, 8, 11, 13, 18, 19]]
    #cluster_dis = [[10, 17], [12], [0, 6], [2, 3, 5, 7, 18], [1, 4, 8, 9, 13, 14, 16], [15], [11], [19]]
    #cluster_dis = [[3], [13], [6, 7, 18], [4, 5, 10, 12, 14, 16, 17], [8, 11, 12, 15], [0], [19], [9]]
    cluster_dis = [[19], [17], [16], [1, 7, 18], [6, 8, 9, 11, 14, 15], [4], [13], [0, 2, 3, 5, 10, 12]]
    
    nmi_ss = []
    for i in range(len(cluster_dis)):
        topic_word = tw[cluster_dis[i], :]

        if len(topic_word) == 1:
            this_nmi = 1.0
        else:
            this_nmi = nmi(topic_word)
        
        print this_nmi

        nmi_ss.append(this_nmi)
    
    print np.average(nmi_ss)
    

    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    
    
    