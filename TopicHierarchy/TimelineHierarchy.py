# -*- coding: utf-8 -*-
'''
Created on 2015年1月8日

@author: ZhuJiahui506
'''

import os
import time
import numpy as np
from ete2 import Tree
from KLD import SKLD
from TopicHierarchy.SimBRT import BRT_construct
from TextToolkit import write_matrix_to_text

def vsm_reconstruct(TW_vsm1, wd1, new_wd):
    
    topic_num = len(TW_vsm1)
    origin_wd_len = len(TW_vsm1[0])
    
    new_TW1 = np.zeros((topic_num, len(new_wd)))
    
    for i in range(topic_num):
        
        p1_dict = {}
        for j in range(origin_wd_len):
            if TW_vsm1[i][j] >= 0.00001:
                p1_dict[wd1[j]] = TW_vsm1[i][j]
        
        p1_dict2 = {}
        for each1 in new_wd:
            if each1 in p1_dict.keys():
                p1_dict2[each1] = p1_dict[each1]
            else:
                p1_dict2[each1] = 0.0
                
        for j in range(len(new_wd)):
            new_TW1[i, j] = p1_dict2[new_wd[j]]
    
    return new_TW1


def merge_wd(TW_vsm1, TW_vsm2, wd1, wd2):
    
    new_wd = []
    
    origin_wd_len = len(wd1)
    
    vsm_sum1 = np.sum(TW_vsm1, 0)
    for i in range(origin_wd_len):
        if vsm_sum1[i] >= 0.00001:
            new_wd.append(wd1[i])
    
    vsm_sum2 = np.sum(TW_vsm2, 0)
    for i in range(origin_wd_len):
        if (vsm_sum2[i] >= 0.00001) and wd2[i] not in new_wd:
            new_wd.append(wd2[i])
    
    # 新词汇列表构造完毕
    
    new_TW1 = vsm_reconstruct(TW_vsm1, wd1, new_wd)
    new_TW2 = vsm_reconstruct(TW_vsm2, wd2, new_wd)
    
    return new_TW1, new_TW2, new_wd
    

def inner_tree_sim(simBRT, topic_num):

    W1 = np.zeros((topic_num, topic_num))
    for i in range(topic_num):
        for j in range(i, topic_num):
            if i == j:
                pass
            else:
                try:
                    lca = simBRT.get_common_ancestor(str(i), str(j))
                    W1[i, j] = 2 * np.sqrt(lca.gen_p)
                except:
                    W1[i, j] = 0.001
                
                W1[j, i] = W1[i, j]
    return W1


def cross_tree_sim(TW_vsm1, TW_vsm2, wl1, wl2):
    topic_num = len(TW_vsm1)
    
    Ws = np.zeros((topic_num, topic_num))
    
    new_TW1, new_TW2, new_wd = merge_wd(TW_vsm1, TW_vsm2, wl1, wl2)
    
    for i in range(topic_num):
        for j in range(topic_num):
            Ws[i, j] = np.true_divide(1.0, (SKLD(new_TW1[i], new_TW2[j]) + 1.0))
    
    return Ws
    
def get_inv_degree(W1):
    
    dimension = len(W1)
    D1 = np.zeros((dimension, dimension))
   
    for i in range(dimension):
        D1[i, i] = 1.0 / np.sum(W1[i])
    
    return D1


def get_converged_P(Ps0, delta, R1, R2, it):
    
    next_Ps = Ps0
    
    for i in range(it):
        next_Ps = delta * np.dot(R1, Ps0) + (1 - delta) * np.dot(Ps0, R2)
        #print next_Ps
        Ps0 = next_Ps
    
    return next_Ps


def CT_RWR(TW_vsm1, TW_vsm2, proportion1, proportion2, wl1, wl2):
    
    simBRT1 = BRT_construct(TW_vsm1, proportion1)
    simBRT2 = BRT_construct(TW_vsm2, proportion2)
    
    topic_num = len(TW_vsm1)
    W1 = inner_tree_sim(simBRT1, topic_num)
    W2 = inner_tree_sim(simBRT2, topic_num)
    Ws = cross_tree_sim(TW_vsm1, TW_vsm2, wl1, wl2)
    
    #print W1
    #print W2
    print Ws
    
    inv_D1 = get_inv_degree(W1)
    inv_D2 = get_inv_degree(W2)
    inv_Ds = get_inv_degree(Ws)
    
    
    
    P1 = np.dot(inv_D1, W1)
    P2 = np.dot(inv_D2, W2)
    Ps0 = np.dot(inv_Ds, Ws)
    
    #print P1
    #print P2
    #print Ps0
    
    mu = 0.8
    eta = 0.8
    lam = 0.8
    delta = 0.8
    
    R1 = (1 - mu) * np.linalg.inv((np.eye(topic_num) - mu * P1))
    R2 = (1 - eta) * np.linalg.inv((np.eye(topic_num) - eta * P2))

    Ps = get_converged_P(Ps0, delta, R1, R2, it=10)
    
    Rs = (1 - lam) * np.linalg.inv((np.eye(topic_num) - lam * Ps))
    
    return simBRT1, simBRT2, Rs
    
    
if __name__ == '__main__':
    
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'

    read_directory1 = root_directory + u'dataset/coherent_topic10/sparse_topic'
    read_directory2 = root_directory + u'dataset/coherent_topic10/topic_pro'
    read_directory3 = root_directory + u'dataset/text_model/select_words'
    
    write_directory = root_directory + u'dataset/hierarchy10'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    
    for i in range(63, 64):
        
        # 主题边缘概率
        proportion1 = []
        f1 = open(read_directory2 + '/' + str(i) + '.txt', 'rb')
        line = f1.readline()
        while line:
            proportion1.append(float(line.split()[1]))
            line = f1.readline()
        f1.close()
        
        proportion2 = []
        f1 = open(read_directory2 + '/' + str(i + 1) + '.txt', 'rb')
        line = f1.readline()
        while line:
            proportion2.append(float(line.split()[1]))
            line = f1.readline()
        f1.close()
        
        wl1 = []
        f1 = open(read_directory3 + '/' + str(i) + '.txt', 'rb')
        line = f1.readline()
        while line:
            wl1.append(line.split()[0])
            line = f1.readline()
        f1.close()
        
        wl2 = []
        f1 = open(read_directory3 + '/' + str(i + 1) + '.txt', 'rb')
        line = f1.readline()
        while line:
            wl2.append(line.split()[0])
            line = f1.readline()
        f1.close()
        
        TW_vsm1 = np.loadtxt(read_directory1 + '/' + str(i) + '.txt')
        TW_vsm2 = np.loadtxt(read_directory1 + '/' + str(i + 1) + '.txt')
        
        simBRT1, simBRT2, Rs = CT_RWR(TW_vsm1, TW_vsm2, proportion1, proportion2, wl1, wl2)
        
        print simBRT1.get_ascii(show_internal=True)
        print simBRT2.get_ascii(show_internal=True)
        #print Rs
        
        write_matrix_to_text(Rs, write_directory + '/' + str(i) + '.txt')
        
        print "Segment %d Completed." % (i)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    
    
    