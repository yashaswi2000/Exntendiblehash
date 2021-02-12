import numpy as np
from bucket import *
from ssm import *
import pandas as pd


def insert_record(simobject,record,dirarray,global_depth,bucket_rc):
    pass
    to_hash = record.id
    hash_value = hash(to_hash)
    index = format(hash_value,"016b")
    if global_depth == 0:
        index = 0
    else:
        index = int(index[0:global_depth],2)
    print(index)
    print(dirarray[index])
    if dirarray[index] == None:
        pass
        record_bucket = simobject.new_record_bucket()
        record_bucket.array[bucket_rc - record_bucket.empty_spaces] = record
        record_bucket.empty_spaces -= 1
        simobject.bucket_array[simobject.current_index] = simobject.new_record_bucket()
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
        print("not written")






data = pd.read_csv("dataset.csv")
dirarray = np.empty(1024, dtype=directory)
secondary_mem = sim_secondary_mem(1000,5,100)
global_depth = 0

for d in data.iterrows():
    recordobj = records(d[1][0],d[1][1],d[1][2],d[1][3])
    #print(recordobj)
    insert_record(secondary_mem,recordobj,dirarray,global_depth,5)




