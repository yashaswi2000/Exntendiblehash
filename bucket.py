import numpy as np
#for storing the records
class records:
    def __init__(self,ID,sale,name,category):
        self.id = ID
        self.sale_amount = sale
        self.customer = name
        self.category = category

#for storing the directories
class directory:
    def __init__(self,prefix,link):
        self.hash_prefix = prefix
        self.pointer = link

#parent class for the buckets
class bucket:
    def __init__(self,size_of_bucket):
        self.empty_spaces = size_of_bucket
        self.link = -1
        self.last = -1

#bucket to store records
class bucket_r(bucket):
    def __init__(self,size_of_bucket,depth):
         super().__init__(size_of_bucket)
         self.depth = depth
         self.array = np.empty(size_of_bucket, dtype=records)

#bucket to store the directories
class bucket_d(bucket):
    def __init__(self,size_of_bucket):
        super().__init__(size_of_bucket)
        self.array = np.empty(size_of_bucket, dtype=directory)
    

