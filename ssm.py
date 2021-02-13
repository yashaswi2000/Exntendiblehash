import numpy as np
from bucket import *

class sim_secondary_mem:
    def __init__(self,arry_size,rbucket_size,dbucket_size):
        self.bucket_array = np.empty(arry_size,dtype=bucket)
        self.r_size = rbucket_size
        self.d_size = dbucket_size
        self.empty_spaces = arry_size
        self.current_index = 0

    def new_record_bucket(self,depth):
        return bucket_r(self.r_size,depth)
        