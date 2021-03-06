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
    
    def clean_overflow(self,space):
        pass
        self.empty_list.append(space)
        
    def update_overflow(self):
        if len(self.empty_list) != 0:
            temp = self.empty_list[0]
            self.empty_list.pop(0)
            return temp
        else:
            temp = self.current_overflow
            self.current_overflow -= 1            
            return temp
            
        
        