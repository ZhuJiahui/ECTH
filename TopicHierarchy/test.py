# -*- coding: utf-8 -*-
'''
Created on 2014年12月30日

@author: ZhuJiahui506
'''

import numpy as np
from BRT import FDCM_T, delta_func

if __name__ == '__main__':
    #a = np.array([[0.1,0.2,0.3,0.4],[0.22,0.33,0.44,0.01],[0.1,0.3,0.2,0.4]])
    a = 0.1
    for i in range(100):
        
        dir_alpha = a * np.ones(10)
        #c = FDCM_T(a, dir_alpha)
        c = delta_func(dir_alpha)
        #c2 = delta_func(dir_alpha + 0.01 * np.ones(1000))
        print c
        a += 0.01