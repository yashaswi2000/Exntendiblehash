#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 21:03:29 2021

@author: yashaswi
"""

import numpy as np
from bucket import *

class sim_secondary_mem:
    def __init__(self,arry_size,rbucket_size,dbucket_size):
        self.bucket_array = np.empty(arry_size,dtype=bucket)
        self.r_size = rbucket_size
        self.d_size = dbucket_size
        self.empty_spaces = arry_size
        self.current_index = 0
        self.current_overflow = arry_size - 1
        self.start_overflow = arry_size - 1
        self.empty_list = []

    def new_record_bucket(self,depth):
        return bucket_r(self.r_size,depth)
    
    def new_direct_bucket(self):
        return bucket_d(self.d_size)
    
    def clean_overflow(self,space = None):
        pass
        self.current_overflow -= 1
    
            
        
        