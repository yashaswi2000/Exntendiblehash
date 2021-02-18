import numpy as np
#for storing the records
class records:
    def __init__(self,ID,sale,name,category):
        self.id = ID
        self.sale_amount = sale
        self.customer = name
        self.category = category
    
    def print_record(self):
        print(self.id," ",self.sale_amount," ",self.customer," ",self.category)

#for storing the directories
class directory:
    def __init__(self,prefix,link):
        self.hash_prefix = prefix
        self.pointer = link
    
    def print_directory(self):
        print(self.hash_prefix," ",self.pointer)

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
         
    def print_bucket(self):
        array = self.array
        for a in array:
            if a != None:
                a.print_record()
            else:
                print(None)

#bucket to store the directories
class bucket_d(bucket):
    def __init__(self,size_of_bucket):
        super().__init__(size_of_bucket)
        self.array = np.empty(size_of_bucket, dtype=directory)
        
    def print_bucket(self):
        array = self.array
        for a in array:
            if a != None:
                a.print_directory()
            else:
                print(None)
    

