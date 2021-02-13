import numpy as np
from bucket import *
from ssm import *
import pandas as pd


def directory_expansion(dirarray,global_depth):
    pass
    if 2 * dir_length <= 1024:
        pass
        for i in range(len(dirarray)):
            temp_dir = dirarray[i]
            dirarray.pop(i)
            dirarray.append(directory(temp_dir.hash_prefix<<1,temp_dir.pointer))
            dirarray.append(directory((temp_dir.hash_prefix<<1) + 1,temp_dir.pointer))
        global_depth += 1
        return global_depth
    else:
        pass
    
    
def splitting(dirarray, simobject, index, global_depth, bucket_rc, flag):
    pass
    if len(dirarray) <= 1024:
        target = dirarray[index].pointer
        #record variables
        record_bucket = simobject.bucket_array[target]
        records_array = record_bucket.array
        depth = record_bucket.depth
        #new bucket creation
        simobject.bucket_array[simobject.current_index] = simobject.new_record_bucket(depth + 1)
        new_target = simobject.current_index
        simobject.current_index += 1
        #rearrange pointers
        target_list = []
        for i in range(len(dirarray)):
            if dirarray[i].pointer == target:
                target_list.append(i)
        l = len(target_list)
        for i in range(l//2,l):
            dirarray[i].pointer = new_target
        
        #reset old bucket
        simobject.bucket_array[target] = simobject.new_record_bucket(depth + 1)
        
        for i in records_array:
            global_depth = insert_record(simobject, i, dirarray, global_depth, bucket_rc, flag)
        
        return global_depth
    


def insert_record(simobject,record,dirarray,global_depth,bucket_rc,flag):
    pass
    to_hash = record.id
    hash_value = hash(to_hash)
    index = format(hash_value,"03b")
    print(index)
    if global_depth == 0:
        index = 0
    else:
        index = int(index[0:global_depth],2)
    print(index,"this is it")
    print(dirarray[index])
    if dirarray[index] == None:
        pass
        record_bucket = simobject.new_record_bucket(0)
        record_bucket.array[bucket_rc - record_bucket.empty_spaces] = record
        record_bucket.empty_spaces -= 1
        simobject.bucket_array[simobject.current_index] = record_bucket
        dirarray[index] = directory(index,simobject.current_index)
        simobject.current_index += 1

    elif simobject.bucket_array[dirarray[index].pointer].empty_spaces > 0:
        pass
        record_bucket = simobject.bucket_array[dirarray[index].pointer]
        record_bucket.array[bucket_rc - record_bucket.empty_spaces] = record
        record_bucket.empty_spaces -= 1
        simobject.bucket_array[dirarray[index].pointer] = record_bucket

    else:
        pass
        if simobject.bucket_array[dirarray[index].pointer].depth == global_depth and flag==0:
            pass
            print("gd == ld")
            global_depth = directory_expansion(dirarray,global_depth)
            print(dirarray)
            print(global_depth)
            global_depth = insert_record(simobject,record,dirarray,global_depth,bucket_rc,1)
        
        elif simobject.bucket_array[dirarray[index].pointer].depth < global_depth:
            pass
            print("spltting")
            global_depth = splitting(dirarray, simobject, index, global_depth, bucket_rc, flag)
            global_depth = insert_record(simobject,record,dirarray,global_depth,bucket_rc,flag)
        
        else:
            print("overflow")
            
    
    return global_depth

    




data = pd.read_csv("dataset.csv")
dirarray = [None]
secondary_mem = sim_secondary_mem(1000,5,100)
global_depth = 0
dir_length = 1

for d in data.iterrows():
    recordobj = records(d[1][0],d[1][1],d[1][2],d[1][3])
    #print(recordobj)
    global_depth = insert_record(secondary_mem,recordobj,dirarray,global_depth,5,0)




