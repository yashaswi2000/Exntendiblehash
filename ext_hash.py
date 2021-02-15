import numpy as np
from bucket import *
from ssm import *
import pandas as pd


def insert_directory(simobject,dir_bucket,dirobject):
    if dir_bucket.link == -1 and dir_bucket.empty_spaces > 0:
        dir_bucket.array[simobject.d_size - dir_bucket.empty_spaces] = dirobject
        dir_bucket.empty_spaces -= 1
    elif dir_bucket.link == -1 and dir_bucket.empty_spaces == 0:
        directory_bucket = simobject.new_direct_bucket()
        directory_bucket.array[simobject.d_size - directory_bucket.empty_spaces] = dirobject
        directory_bucket.empty_spaces -= 1
        simobject.bucket_array[simobject.current_overflow] = directory_bucket
        dir_bucket.link = simobject.current_overflow
        dir_bucket.last = 0
        simobject.clean_overflow()
    else:
        insert_directory(simobject,simobject.bucket_array[dir_bucket.link],dirobject)
        
def clean_directory(simobject,od_pointer):
    pass
    


def directory_expansion(dirarray,global_depth,simobject,od_pointer,dir_length):
    pass
    if 2 * len(dirarray) <= dir_length:
        pass
        l = len(dirarray)
        for i in range(l):
            temp_dir = dirarray[0]
            dirarray.pop(0)
            dirarray.append(directory(temp_dir.hash_prefix<<1,temp_dir.pointer))
            dirarray.append(directory((temp_dir.hash_prefix<<1) + 1,temp_dir.pointer))
    else:
        pass
        l = len(dirarray)
        if od_pointer != None:
            directory_bucket = simobject.bucket_array[od_pointer]
            while directory_bucket.link != -1:
                l += simobject.d_size - directory_bucket.empty_spaces
            
            for i in range(l):
                temp_dir = dirarray[0]
                dirarray.pop(0)
                insert_directory(simobject, simobject.bucket_array[od_pointer], directory(temp_dir.hash_prefix<<1,temp_dir.pointer))
                insert_directory(simobject, simobject.bucket_array[od_pointer], directory((temp_dir.hash_prefix<<1) + 1,temp_dir.pointer))
                dirarray.append(clean_directory(simobject,od_pointer))     
        
        else:
            for i in range(l):
                temp_l = len(dirarray)
                if temp_l + 1 <= dir_length:
                    temp_dir = dirarray[0]
                    dirarray.pop(0)
                    dirarray.append(directory(temp_dir.hash_prefix<<1,temp_dir.pointer))
                    dirarray.append(directory((temp_dir.hash_prefix<<1) + 1,temp_dir.pointer))
                else:
                    temp_dir = dirarray[0]
                    dirarray.pop(0)
                    if od_pointer == None:
                        simobject.bucket_array[simobject.current_overflow] = simobject.new_direct_bucket()
                        od_pointer = simobject.current_overflow
                        simobject.clean_overflow()
                    insert_directory(simobject, simobject.bucket_array[od_pointer], directory(temp_dir.hash_prefix<<1,temp_dir.pointer))
                    insert_directory(simobject, simobject.bucket_array[od_pointer], directory((temp_dir.hash_prefix<<1) + 1,temp_dir.pointer))
                    dirarray.append(clean_directory(simobject,od_pointer))  
                    
    global_depth += 1
    return global_depth
        
        

def get_records_overflow(simobject,records_array,record_bucket):
    pass
    records_array.extend(record_bucket.array)
    if record_bucket.link !=-1:
        simobject.bucket_array[record_bucket.link] = get_records_overflow(simobject,records_array,simobject.bucket_array[record_bucket.link])
        simobject.clean_overflow()
    record_bucket.print_bucketr()
    return None    
    
    
def splitting(dirarray, simobject, index, global_depth, bucket_rc, flag,dir_length):
    pass
    if len(dirarray) <= dir_length:
        target = dirarray[index].pointer
        #record variables
        record_bucket = simobject.bucket_array[target]
        depth = record_bucket.depth
        link = record_bucket.link
        records_array = []
        get_records_overflow(simobject,records_array,record_bucket)
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
            dirarray[target_list[i]].pointer = new_target
        
        #reset old bucket
        simobject.bucket_array[target] = simobject.new_record_bucket(depth + 1)
        
        for i in records_array:
            global_depth = insert_record(simobject, i, dirarray, global_depth, bucket_rc, flag)
        
        return global_depth
    


def insert_record(simobject,record,dirarray,global_depth,bucket_rc,flag,od_pointer,dir_length):
    pass
    to_hash = record.id
    hash_value = hash(to_hash)
    index = format(hash_value,"05b")
    print(index)
    if global_depth == 0:
        index = 0
    else:
        index = int(index[0:global_depth],2)
    print(index,"this is it")
    if index < dir_length:
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
            if simobject.bucket_array[dirarray[index].pointer].depth == global_depth and flag==0 and simobject.bucket_array[dirarray[index].pointer].link==-1:
                pass
                print("gd == ld")
                global_depth = directory_expansion(dirarray,global_depth,simobject,od_pointer,dir_length)
                visualise(dirarray,simobject)
                global_depth = insert_record(simobject,record,dirarray,global_depth,bucket_rc,1,od_pointer,dir_length)
            
            elif simobject.bucket_array[dirarray[index].pointer].depth < global_depth:
                pass
                print("spltting")
                global_depth = splitting(dirarray, simobject, index, global_depth, bucket_rc, flag)
                global_depth = insert_record(simobject,record,dirarray,global_depth,bucket_rc,flag,od_pointer,dir_length)
            
            else:
                print("overflow")
                record_bucket = simobject.bucket_array[dirarray[index].pointer]
                if record_bucket.last == -1:
                    pass
                    overflow_bucket = simobject.new_record_bucket(0)
                    overflow_bucket.array[bucket_rc - overflow_bucket.empty_spaces] = record
                    overflow_bucket.empty_spaces -= 1
                    simobject.bucket_array[simobject.current_overflow] = overflow_bucket
                    record_bucket.link = simobject.current_overflow
                    record_bucket.last = 0
                    simobject.clean_overflow()
                    
                else:
                    pass
                    record_bucket = simobject.bucket_array[dirarray[index].pointer]
                    while record_bucket.last!=-1:
                        record_bucket = simobject.bucket_array[record_bucket.link]
                    if record_bucket.empty_spaces!=0:
                        pass
                        record_bucket.array[simobject.r_size - record_bucket.empty_spaces] = record
                        record_bucket.empty_spaces -= 1
                    elif flag!=1:
                        pass
                        global_depth = directory_expansion(dirarray,global_depth,simobject,od_pointer,dir_length)
                        visualise(dirarray,simobject)
                        global_depth = insert_record(simobject,record,dirarray,global_depth,bucket_rc,1,od_pointer,dir_length)
                    else:
                        overflow_bucket = simobject.new_record_bucket(0)
                        overflow_bucket.array[bucket_rc - overflow_bucket.empty_spaces] = record
                        overflow_bucket.empty_spaces -= 1
                        simobject.bucket_array[simobject.current_overflow] = overflow_bucket
                        record_bucket.link = simobject.current_overflow
                        record_bucket.last = 0
                        simobject.clean_overflow()
                
                
    else:
        pass
            
    
    return global_depth

    

def visualise(dirarray,simobject):
    print("visualizing the datastructure")
    for i in dirarray:
        print(i.hash_prefix," ",i.pointer)
        temp = simobject.bucket_array[i.pointer]
        while True:
            array = temp.array
            for a in array:
                if a != None:
                    a.print_record()
                else:
                    print(None)
            if temp.last == -1:
                break 
            
            temp = simobject.bucket_array[temp.link]
            
            print("overflow buckets -----------")
                
        print("next bucket")
    




data = pd.read_csv("dataset.csv")
dirarray = [None]
secondary_mem = sim_secondary_mem(1000,3,100)
global_depth = 0
dir_length = 1024
od_pointer = None

for d in data.iterrows():
    recordobj = records(d[1][0],d[1][1],d[1][2],d[1][3])
    #print(recordobj)
    global_depth = insert_record(secondary_mem,recordobj,dirarray,global_depth,3,0,od_pointer,dir_length)
    visualise(dirarray,secondary_mem)
    print("--------------------------")
    
print(secondary_mem.bucket_array[900:910])
for i in range(900,910):
    if secondary_mem.bucket_array[i] != None:
        secondary_mem.bucket_array[i].print_bucketr()






