# -*- coding: utf-8 -*-
'''
Created on 2014年12月24日

@author: ZhuJiahui506
'''

import os
import time
import numpy as np
from scipy import special
from ete2 import Tree
from KLD import SKLD


def likelihood_join(Ta, Tb, dir_alpha, pai_gamma):
    '''
    BRT join操作
    :param Ta: 左子树
    :param Tb: 右子树
    :param dir_alpha: V维Dirichlet参数行向量
    :param pai_gamma: 划分粒度控制参数
    '''

    nTm = 2
     
    pai_Tm = 1 - np.power((1 - pai_gamma), (nTm - 1))

    #t_vsm是定义在根节点上的属性
    Za = Ta.t_vsm
    Zb = Tb.t_vsm
    
    # 合并向量空间
    T_vsm = merge_tvsm(Za, Zb)
    
    # 考虑相似度
    if len(Za.shape) == 1:
        avg_Za = Za
    else:
        avg_Za = np.average(Za, 0)
    
    if len(Zb.shape) == 1:
        avg_Zb = Zb
    else:
        avg_Zb = np.average(Zb, 0)
    
    # 权向量
    WT = (Ta.gen_p * avg_Za + Tb.gen_p * avg_Zb) / (Ta.gen_p + Tb.gen_p)
    Z = np.average(T_vsm, 0)
    topic_sim = np.true_divide(1.0, (1.0 + SKLD(WT, Z)))
     
    pZm_Tm = (pai_Tm * FDCM_T(T_vsm, dir_alpha) + (1 - pai_Tm) * Ta.gen_p * Tb.gen_p) * topic_sim
    
    
    return pZm_Tm


def likelihood_absorb(Ta, Tb, dir_alpha, pai_gamma):
    '''
    BRT absorb操作
    :param Ta: 左子树
    :param Tb: 右子树
    :param dir_alpha: V维Dirichlet参数行向量
    :param pai_gamma: 划分粒度控制参数
    '''
    
    nTm = len(Ta.children) + 1
     
    pai_Tm = 1 - np.power((1 - pai_gamma), (nTm - 1))
     
    #t_vsm是定义在根节点上的属性
    Za = Ta.t_vsm
    Zb = Tb.t_vsm
    
    # 合并向量空间
    T_vsm = merge_tvsm(Za, Zb)
    
    ##########################
    temp_product = 1.0
    temp_sum = 0.0
    temp_s_sum = np.zeros(len(T_vsm[0]))
    
    for each in Ta.children:
        temp_product = temp_product * each.gen_p
        temp_sum += each.gen_p
        etv = each.t_vsm
        if len(etv.shape) == 1:
            avg_Za = etv
        else:
            avg_Za = np.average(Za, 0)
        
        temp_s_sum += (avg_Za * each.gen_p)
    
    if len(Zb.shape) == 1:
        avg_Zb = Zb
    else:
        avg_Zb = np.average(Zb, 0)
    
    # 权向量
    WT = (temp_s_sum + Tb.gen_p * avg_Zb) / (temp_sum + Tb.gen_p)
    Z = np.average(T_vsm, 0)
    topic_sim = np.true_divide(1.0, (1.0 + SKLD(WT, Z)))
    ##########################################################
        
    pZm_Tm = (pai_Tm * FDCM_T(T_vsm, dir_alpha) + (1 - pai_Tm) * Tb.gen_p * temp_product) * topic_sim
    
    return pZm_Tm
    
def likelihood_collapse(Ta, Tb, dir_alpha, pai_gamma):
    '''
    BRT collapse操作
    :param Ta: 左子树
    :param Tb: 右子树
    :param dir_alpha: V维Dirichlet参数行向量
    :param pai_gamma: 划分粒度控制参数
    '''
    
    nTm = len(Ta.children) + len(Tb.children)
     
    pai_Tm = 1 - np.power((1 - pai_gamma), (nTm - 1))
     
    #t_vsm是定义在根节点上的属性
    Za = Ta.t_vsm
    Zb = Tb.t_vsm
    
    # 合并向量空间
    T_vsm = merge_tvsm(Za, Zb)
    
    temp_product = 1.0
    temp_sum = 0.0
    temp_s_sum = np.zeros(len(T_vsm[0]))
    
    for each in Ta.children:
        temp_product = temp_product * each.gen_p
        temp_sum += each.gen_p
        etv = each.t_vsm
        if len(etv.shape) == 1:
            avg_Za = etv
        else:
            avg_Za = np.average(Za, 0)
        
        temp_s_sum += (avg_Za * each.gen_p)
        
    for each2 in Tb.children:
        temp_product = temp_product * each2.gen_p
        temp_sum += each2.gen_p
        etv = each2.t_vsm
        if len(etv.shape) == 1:
            avg_Zb = etv
        else:
            avg_Zb = np.average(Zb, 0)
        
        temp_s_sum += (avg_Zb * each2.gen_p)
        
    # 权向量
    WT = np.true_divide(temp_s_sum, temp_sum)
    Z = np.average(T_vsm, 0)
    topic_sim = np.true_divide(1.0, (1.0 + SKLD(WT, Z)))
    ##########################################################
    
    pZm_Tm = (pai_Tm * FDCM_T(T_vsm, dir_alpha) + (1 - pai_Tm) * temp_product) * topic_sim
    
    return pZm_Tm


def merge_tvsm(Za, Zb):
    '''
    合并向量空间
    :param Za:
    :param Zb:
    '''
    #Ta_num = len(Za)
    #Tb_num = len(Zb)
    Ta_shape = Za.shape
    Tb_shape = Zb.shape
    #if Ta_num == 1 and Tb_num == 1:
    # 主题向量空间的合并
    if len(Ta_shape) == 1 and len(Tb_shape) == 1:
        T_vsm = np.zeros((2, Ta_shape[0]))
        T_vsm[0] = Za
        T_vsm[1] = Zb
    elif len(Ta_shape) == 2 and len(Tb_shape) == 1:
        T_vsm = np.zeros(((Ta_shape[0] + 1), Ta_shape[1]))
        T_vsm[0 : Ta_shape[0], :] = Za
        T_vsm[Ta_shape[0]] = Zb
    elif len(Ta_shape) == 1 and len(Tb_shape) == 2:
        T_vsm = np.zeros(((Tb_shape[0] + 1), Tb_shape[1]))
        T_vsm[0] = Za
        T_vsm[1 : (Tb_shape[0] + 1), :] = Zb
    else:
        T_vsm = np.zeros(((Ta_shape[0] + Tb_shape[0]), Ta_shape[1]))
        T_vsm[0 : Ta_shape[0]] = Za
        T_vsm[Ta_shape[0] : (Ta_shape[0] + Tb_shape[0]), :] = Zb
        
    return T_vsm
    

def FDCM_T(T_vsm, dir_alpha):
    '''
    计算主题集合的边缘概率
    :param T_vsm: 主题向量空间
    :param dir_alpha: V维Dirichlet参数行向量
    '''
        
    FDCM = 1.0
    selected_num = 5
    
    T_shape = T_vsm.shape
    
    if len(T_shape) == 1:
        multinomial_up = special.gamma(np.sum(T_vsm) + 1)        
        multinomial_down = np.prod(special.gamma(T_vsm + 1))
        
        #有问题
        delta_up = delta_func(dir_alpha + T_vsm, selected_num)  # 按列求和
        delta_down = delta_func(dir_alpha, selected_num)
        
        this_FDCM = np.true_divide(multinomial_up, multinomial_down) * np.true_divide(delta_up, delta_down)
        
        FDCM = FDCM * this_FDCM
    else:
        topic_size = len(T_vsm)
        for i in range(topic_size):
            
            multinomial_up = special.gamma(np.sum(T_vsm[i]) + 1)        
            multinomial_down = np.prod(special.gamma(T_vsm[i] + 1))
        
            #有问题
            delta_up = delta_func(dir_alpha + T_vsm[i], selected_num)  # 按列求和
            delta_down = delta_func(dir_alpha, selected_num)
        
            this_FDCM = np.true_divide(multinomial_up, multinomial_down) * np.true_divide(delta_up, delta_down)
        
            FDCM = FDCM * this_FDCM
            
            
    return FDCM
        
        
def delta_func(dir_alpha, selected_num):
    '''
    LDA里面的delta函数
    :param dir_alpha: V维Dirichlet参数行向量
    '''
    #选择值最大的前selectd_num个做运算
    
    sorted_data = np.sort(dir_alpha)
    selected_data = sorted_data[(len(dir_alpha) - selected_num) :]
    
    numerator = np.prod(special.gamma(selected_data))
    denominator = special.gamma(np.sum(selected_data))
    return np.true_divide(numerator, denominator)



def BRT_join_op(brt_list, similarity_matrix1, c, max_gen_p):
    '''
    真正实施BRT join操作
    :param brt_list: 树集合
    :param similarity_matrix1: 生成概率矩阵
    :param c: BRT树集合中的元素个数
    :param max_gen_p: 最大可能性下的概率值
    '''
    
    max_tree_index1 = np.argmax(similarity_matrix1)
    max_row_index = int(np.ceil(np.true_divide((max_tree_index1 + 1), c)) - 1)
    max_col_index = int(max_tree_index1 - max_row_index * c)
            
    #合并向量空间和概率
    merged_vsm = merge_tvsm(brt_list[max_row_index].t_vsm, brt_list[max_col_index].t_vsm)
            
    len_a = len(brt_list[max_row_index].children)
    len_b = len(brt_list[max_col_index].children)
    
    if len_a == 1 and len_b == 1:
        brt_list[max_row_index].add_child(brt_list[max_col_index].children[0])
            
        brt_list[max_row_index].t_vsm = merged_vsm
        brt_list[max_row_index].gen_p = max_gen_p
                
        # 删除另一个部分
        brt_list.remove(brt_list[max_col_index])
    elif len_a == 1 and len_b > 1:
        brt_list[max_row_index].add_child(brt_list[max_col_index])
                
        brt_list[max_row_index].t_vsm = merged_vsm
        brt_list[max_row_index].gen_p = max_gen_p
                
        # 删除另一个部分
        brt_list.remove(brt_list[max_col_index])
    elif len_a > 1 and len_b == 1:
        brt_list[max_col_index].add_child(brt_list[max_row_index])
                
        brt_list[max_col_index].t_vsm = merged_vsm
        brt_list[max_col_index].gen_p = max_gen_p
                
        # 删除另一个部分
        brt_list.remove(brt_list[max_row_index])
    else:
        brt_merge = Tree()
        brt_merge.add_features(t_vsm=merged_vsm)
        brt_merge.add_features(gen_p=max_gen_p)
                
        brt_merge.add_child(brt_list[max_row_index])
        brt_merge.add_child(brt_list[max_col_index])
                
        # 维护树结构
        brt_list[max_row_index] = brt_merge
        brt_list.remove(brt_list[max_col_index])
        
        
def BRT_absorb_op(brt_list, similarity_matrix2, c, max_gen_p):
    '''
    真正实施BRT absorb操作(left吸收right)
    :param brt_list: 树集合
    :param similarity_matrix2: 生成概率矩阵
    :param c: BRT树集合中的元素个数
    :param max_gen_p: 最大可能性下的概率值
    '''
    
    max_tree_index1 = np.argmax(similarity_matrix2)
    max_row_index = int(np.ceil(np.true_divide((max_tree_index1 + 1), c)) - 1)
    max_col_index = int(max_tree_index1 - max_row_index * c)
            
    #合并向量空间和概率
    merged_vsm = merge_tvsm(brt_list[max_row_index].t_vsm, brt_list[max_col_index].t_vsm)
            
    len_a = len(brt_list[max_row_index].children)
    len_b = len(brt_list[max_col_index].children)
    
    if len_a >= 1 and len_b == 1:
        #退化为join
        brt_list[max_row_index].add_child(brt_list[max_col_index].children[0])
            
        brt_list[max_row_index].t_vsm = merged_vsm
        brt_list[max_row_index].gen_p = max_gen_p
                
        # 删除另一个部分
        brt_list.remove(brt_list[max_col_index])
    else:
        brt_list[max_row_index].add_child(brt_list[max_col_index])
            
        brt_list[max_row_index].t_vsm = merged_vsm
        brt_list[max_row_index].gen_p = max_gen_p
                
        # 删除另一个部分
        brt_list.remove(brt_list[max_col_index])


def BRT_collapse_op(brt_list, similarity_matrix3, c, max_gen_p):
    '''
    真正实施BRT collapse操作
    :param brt_list: 树集合
    :param similarity_matrix3: 生成概率矩阵
    :param c: BRT树集合中的元素个数
    :param max_gen_p: 最大可能性下的概率值
    '''
    
    max_tree_index1 = np.argmax(similarity_matrix3)
    max_row_index = int(np.ceil(np.true_divide((max_tree_index1 + 1), c)) - 1)
    max_col_index = int(max_tree_index1 - max_row_index * c)
            
    #合并向量空间和概率
    merged_vsm = merge_tvsm(brt_list[max_row_index].t_vsm, brt_list[max_col_index].t_vsm)
    
    b_children_list = brt_list[max_col_index].get_children()
    
    for each in b_children_list:
        brt_list[max_row_index].add_child(each)
       
    brt_list[max_row_index].t_vsm = merged_vsm
    brt_list[max_row_index].gen_p = max_gen_p
                
    # 删除另一个部分
    brt_list.remove(brt_list[max_col_index])
    
    

def BRT_construct(T_vsm, proportion):
    
    topic_num = len(T_vsm)

    vocabulary_num  = len(T_vsm[0])
    
    #dir_alpha = 0.287 * np.ones(vocabulary_num)
    dir_alpha = 0.1 * np.ones(vocabulary_num)
    pai_gamma = 0.1
    
    brt_list = []
    c = topic_num
    
    # 初始化
    for i in range(topic_num):
        brt_i = Tree()
        brt_i.add_features(t_vsm=T_vsm[i])
        brt_i.add_features(gen_p=proportion[i])
        
        leaf_node = brt_i.add_child(name=str(i))
        leaf_node.add_features(t_vsm=T_vsm[i])
        leaf_node.add_features(gen_p=proportion[i])
        
        brt_list.append(brt_i)
    
    while c > 1:
        similarity_matrix1 = np.zeros((c, c))
        similarity_matrix2 = np.zeros((c, c))
        similarity_matrix3 = np.zeros((c, c))
        
        for i in range(c):
            for j in range(i, c):
                if (i == j):
                    similarity_matrix1[i, j] = 0.0
                    similarity_matrix2[i, j] = 0.0
                    similarity_matrix3[i, j] = 0.0
                else:
                    similarity_matrix1[i, j] = likelihood_join(brt_list[i], brt_list[j], dir_alpha, pai_gamma)
                    similarity_matrix2[i, j] = likelihood_absorb(brt_list[i], brt_list[j], dir_alpha, pai_gamma)
                    similarity_matrix3[i, j] = likelihood_collapse(brt_list[i], brt_list[j], dir_alpha, pai_gamma)
                    
                    similarity_matrix1[j, i] = similarity_matrix1[i, j]
                    similarity_matrix2[j, i] = likelihood_absorb(brt_list[j], brt_list[i], dir_alpha, pai_gamma)
                    similarity_matrix3[j, i] = similarity_matrix3[i, j]
        #print similarity_matrix1
        max_list = np.zeros(3)            
        max_list[0] = np.max(similarity_matrix1)
        max_list[1] = np.max(similarity_matrix2)
        max_list[2] = np.max(similarity_matrix3)
        
        #print max_list
        
        max_gen_p = np.max(max_list)
        
        max_list_index = np.argmax(max_list)
        
        
        '''
        合并Join,吸收Absorb,塌陷collapse
        '''
        # join 合并
        if max_list_index == 0:
            BRT_join_op(brt_list, similarity_matrix1, c, max_gen_p)
            #print "Join"
                
        # absorb 吸收  
        elif max_list_index == 1:
            BRT_absorb_op(brt_list, similarity_matrix2, c, max_gen_p)
            #print "Absorb"
        # collapse 塌陷    
        elif max_list_index == 2:
            BRT_collapse_op(brt_list, similarity_matrix3, c, max_gen_p)
            #print "Collapse"
            
        else:
            print "Error!"
            break
        
        c = c - 1
    
    # 跳出循环
    this_BRT = brt_list[0]

    #print this_BRT.get_ascii(show_internal=True)
    return this_BRT


if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'

    read_directory = root_directory + u'dataset/coherent_topic10/sparse_topic'
    read_directory2 = root_directory + u'dataset/coherent_topic10/topic_pro'
    #write_directory = root_directory + u'dataset/sparse_topic'

    
    #if (not(os.path.exists(write_directory))):
        #os.mkdir(write_directory)

    
    # 本片数据的主题比例
    proportion = []
    f1 = open(read_directory2 + '/' + str(60) + '.txt', 'rb')
    line = f1.readline()
    while line:
        proportion.append(float(line.split()[1]))
        line = f1.readline()
    f1.close()
    
    TW_vsm = np.loadtxt(read_directory + '/' + str(60) + '.txt')
        
        
    #quick_write_list_to_text(SPTW_to_string, write_directory + '/' + str(i + 1) + '.txt')
    this_BRT = BRT_construct(TW_vsm, proportion)

    print this_BRT.get_ascii(show_internal=True)
    #lca = this_BRT.get_common_ancestor("6", "1")
    #print lca.gen_p
    #print lca.t_vsm
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'

