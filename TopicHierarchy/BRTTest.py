# -*- coding: utf-8 -*-
'''
Created on 2014年12月26日

@author: ZhuJiahui506
'''

import numpy as np
from scipy import special
from ete2 import Tree

def ss(s):
    s[0] = 1
    s.remove(s[2])

if __name__ == '__main__':
    a = [11,22,33]
    ss(a)
    print a
    
    brt_list = []
    topic_num = 5
    
    # 初始化
    for i in range(topic_num):
        brt_i = Tree()
        brt_i.add_features(t_vsm=22)
        brt_i.add_features(gen_p=0.5)
        
        leaf_node = brt_i.add_child(name=str(i))
        leaf_node.add_features(t_vsm=22)
        leaf_node.add_features(gen_p=0.5)
        
        brt_list.append(brt_i)
    
    #print brt_list[2].children
    brt_list[1].add_child(brt_list[2].children[0])
    #print brt_list[1]
    
    TT = Tree()
    A = TT.add_child(name="1")
    B = TT.add_child(name="2")
    C = TT.add_child(name="3")
    D = A.add_child(name="11")
    E = A.add_child(name="12")
    F = B.add_child(name="21")
    G = B.add_child(name="22")
    H = C.add_child(name="31")
    
    
    #TT2 = Tree(name="AAAA")
    #AA = TT2.add_child(name="AA")
    #AB = TT2.add_child(name="AB")
    
    #print TT2
    
    #TT.add_child(TT2.get_children()[0])
    #TT.add_child(TT2.get_children()[1])
    print TT.get_ascii(show_internal=True)
    lca = TT.get_common_ancestor(D, E)
    print type(lca)
    #TT.write(outfile="tree.txt")
    
    #print TT.get_children()[1]
    #TT2.delete()
    #print TT
