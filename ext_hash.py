import numpy as np
from bucket import *
from ssm import *
import pandas as pd



class extensible_hash:
    def __init__(self,global_depth,dir_length):
        self.global_depth = global_depth
        self.dir_length = dir_length
        self.od_pointer = None
        self.dirarray = [None]
        

    def insert_directory(self,simobject,dir_bucket,dirobject):
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
            self.insert_directory(simobject,simobject.bucket_array[dir_bucket.link],dirobject)
        
    def clean_directory(self,simobject,od_pointer):
        pass
        if simobject.bucket_array[od_pointer].link == -1:
            pass
            dir_bucket = simobject.bucket_array[od_pointer]
            send_dir = dir_bucket.array[0]
            dir_bucket.array = np.delete(dir_bucket.array,0)
            dir_bucket.array = np.append(dir_bucket.array,None)
            dir_bucket.empty_spaces += 1
            return send_dir 
        else:
            dir_object = self.clean_directory(simobject,simobject.bucket_array[od_pointer].link)
            link_pointer = simobject.bucket_array[od_pointer].link
            if simobject.bucket_array[link_pointer].empty_spaces == simobject.d_size:
                simobject.bucket_array[link_pointer] = None
            dir_bucket = simobject.bucket_array[od_pointer]
            send_dir = dir_bucket.array[0]
            dir_bucket.array = np.delete(dir_bucket.array,0)
            dir_bucket.array = np.append(dir_bucket.array,dir_object)
            return send_dir 


    def directory_expansion(self,simobject):
        pass
        if 2 * len(self.dirarray) <= self.dir_length:
            pass
            l = len(self.dirarray)
            for i in range(l):
                temp_dir = self.dirarray[0]
                self.dirarray.pop(0)
                self.dirarray.append(directory(temp_dir.hash_prefix<<1,temp_dir.pointer))
                self.dirarray.append(directory((temp_dir.hash_prefix<<1) + 1,temp_dir.pointer))
        else:
            pass
            l = len(self.dirarray)
            if self.od_pointer != None:
                directory_bucket = simobject.bucket_array[self.od_pointer]
                while directory_bucket.link != -1:
                    l += simobject.d_size - directory_bucket.empty_spaces
                    directory_bucket = simobject.bucket_array[directory_bucket.link]
                
                for i in range(l):
                    temp_dir = self.dirarray[0]
                    self.dirarray.pop(0)
                    insert_directory(simobject, simobject.bucket_array[self.od_pointer], directory(temp_dir.hash_prefix<<1,temp_dir.pointer))
                    insert_directory(simobject, simobject.bucket_array[self.od_pointer], directory((temp_dir.hash_prefix<<1) + 1,temp_dir.pointer))
                    self.dirarray.append(clean_directory(simobject,self.od_pointer))     
            
            else:
                for i in range(l):
                    temp_l = len(self.dirarray)
                    if temp_l + 1 <= self.dir_length:
                        temp_dir = self.dirarray[0]
                        self.dirarray.pop(0)
                        self.dirarray.append(directory(temp_dir.hash_prefix<<1,temp_dir.pointer))
                        self.dirarray.append(directory((temp_dir.hash_prefix<<1) + 1,temp_dir.pointer))
                    else:
                        temp_dir = self.dirarray[0]
                        self.dirarray.pop(0)
                        if self.od_pointer == None:
                            simobject.bucket_array[simobject.current_overflow] = simobject.new_direct_bucket()
                            self.od_pointer = simobject.current_overflow
                            simobject.clean_overflow()
                        self.insert_directory(simobject, simobject.bucket_array[self.od_pointer], directory(temp_dir.hash_prefix<<1,temp_dir.pointer))
                        self.insert_directory(simobject, simobject.bucket_array[self.od_pointer], directory((temp_dir.hash_prefix<<1) + 1,temp_dir.pointer))
                        self.dirarray.append(self.clean_directory(simobject,self.od_pointer))  
                        
        self.global_depth += 1

    def get_records_overflow(self,simobject,records_array,record_bucket):
        pass
        records_array.extend(record_bucket.array)
        if record_bucket.link !=-1:
            simobject.bucket_array[record_bucket.link] = self.get_records_overflow(simobject,records_array,simobject.bucket_array[record_bucket.link])
            simobject.clean_overflow()
        record_bucket.print_bucket()
        return None

    def get_directory(self,od_pointer,index,simobject):
        pass
        if index < self.dir_length:
            return self.dirarray[index]
        else:
            index -= self.dir_length
            while index >= simobject.d_size:
                od_pointer = simobject.bucket_array[od_pointer].link
                index -= simobject.d_size
            #print(od_pointer,"here it is")
            return simobject.bucket_array[od_pointer].array[index]

    def set_directory(self,od_pointer,index,simobject,value):
        pass
        if index < self.dir_length:
            self.dirarray[index].pointer = value
        else:
            index -= self.dir_length
            while index >= simobject.d_size:
                od_pointer = simobject.bucket_array[od_pointer].link
                index -= simobject.d_size
            simobject.bucket_array[od_pointer].array[index].pointer = value 

    def set_directory_obj(self,od_pointer,index,simobject,value):
        pass
        if index < self.dir_length:
            self.dirarray[index] = value
        else:
            index -= self.dir_length
            while index >= simobject.d_size:
                od_pointer = simobject.bucket_array[od_pointer].link
                index -= simobject.d_size
            simobject.bucket_array[od_pointer].array[index] = value                               
    

    def get_direct_length(self,simobject):
        pass
        if self.od_pointer != None:
            l = self.dir_length
            directory_bucket = simobject.bucket_array[self.od_pointer]
            while directory_bucket.link != -1:
                l += simobject.d_size - directory_bucket.empty_spaces
                directory_bucket = simobject.bucket_array[directory_bucket.link]
            return l
        else:
            return len(self.dirarray)
    
    def splitting(self,simobject, index, flag):
        pass
        print(self.od_pointer,"this is check")
        dir_index = self.get_directory(self.od_pointer, index, simobject)
        target = dir_index.pointer
        #record variables
        record_bucket = simobject.bucket_array[target]
        depth = record_bucket.depth
        link = record_bucket.link
        records_array = []
        self.get_records_overflow(simobject,records_array,record_bucket)
        #new bucket creation
        simobject.bucket_array[simobject.current_index] = simobject.new_record_bucket(depth + 1)
        new_target = simobject.current_index
        simobject.current_index += 1
        #rearrange pointers
        target_list = []
        total_l = self.get_direct_length(simobject)
        for i in range(total_l):
            dir_i = self.get_directory(self.od_pointer, i, simobject)
            if dir_i.pointer == target:
                target_list.append(i)
        l = len(target_list)
        for i in range(l//2,l):
            self.set_directory(self.od_pointer, target_list[i], simobject,new_target)
        
        #reset old bucket
        simobject.bucket_array[target] = simobject.new_record_bucket(depth + 1)
        
        for i in records_array:
            self.insert_record(simobject, i, flag)
            
    
    def insert_record(self,simobject,record,flag):
        to_hash = record.id
        hash_value = hash(to_hash)
        index = format(hash_value,"05b")
        print(index,self.global_depth)
        if self.global_depth == 0:
            index = 0
        else:
            index = int(index[0:self.global_depth],2)
        print(index,"this is it")
        dir_index = self.get_directory(self.od_pointer,index,simobject)
        if dir_index == None:
            pass
            record_bucket = simobject.new_record_bucket(0)
            record_bucket.array[simobject.r_size - record_bucket.empty_spaces] = record
            record_bucket.empty_spaces -= 1
            simobject.bucket_array[simobject.current_index] = record_bucket
            self.set_directory_obj(self.od_pointer,index,simobject,directory(index,simobject.current_index))
            simobject.current_index += 1
    
        elif simobject.bucket_array[dir_index.pointer].empty_spaces > 0:
            pass
            record_bucket = simobject.bucket_array[dir_index.pointer]
            record_bucket.array[simobject.r_size - record_bucket.empty_spaces] = record
            record_bucket.empty_spaces -= 1
            simobject.bucket_array[dir_index.pointer] = record_bucket
    
        elif simobject.bucket_array[dir_index.pointer].depth == self.global_depth and flag==0 and simobject.bucket_array[dir_index.pointer].link==-1:
            pass
            print("gd == ld")
            self.directory_expansion(simobject)
            visualise(self.dirarray,simobject,self.od_pointer)
            self.insert_record(simobject,record,1)
            
        elif simobject.bucket_array[dir_index.pointer].depth < global_depth:
            pass
            print("spltting")
            self.splitting(simobject, index,flag)
            self.insert_record(simobject,record,flag)
            
        else:
            print("overflow")
            record_bucket = simobject.bucket_array[dir_index.pointer]
            if record_bucket.last == -1:
                pass
                overflow_bucket = simobject.new_record_bucket(0)
                overflow_bucket.array[simobject.r_size - overflow_bucket.empty_spaces] = record
                overflow_bucket.empty_spaces -= 1
                simobject.bucket_array[simobject.current_overflow] = overflow_bucket
                record_bucket.link = simobject.current_overflow
                record_bucket.last = 0
                simobject.clean_overflow()
                
            else:
                pass
                record_bucket = simobject.bucket_array[dir_index.pointer]
                while record_bucket.last!=-1:
                    record_bucket = simobject.bucket_array[record_bucket.link]
                if record_bucket.empty_spaces!=0:
                    pass
                    record_bucket.array[simobject.r_size - record_bucket.empty_spaces] = record
                    record_bucket.empty_spaces -= 1
                elif flag!=1:
                    pass
                    self.directory_expansion(simobject)
                    visualise(self.dirarray,simobject,self.od_pointer)
                    self.insert_record(simobject,record,1)
                else:
                    overflow_bucket = simobject.new_record_bucket(0)
                    overflow_bucket.array[simobject.r_size - overflow_bucket.empty_spaces] = record
                    overflow_bucket.empty_spaces -= 1
                    simobject.bucket_array[simobject.current_overflow] = overflow_bucket
                    record_bucket.link = simobject.current_overflow
                    record_bucket.last = 0
                    simobject.clean_overflow()
                   

    

def visualise(dirarray,simobject,od_pointer):
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
    if od_pointer != None:
        while od_pointer != -1:
            dir_array = simobject.bucket_array[od_pointer].array
            for i in dir_array:
                if i is not None:
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
            od_pointer = simobject.bucket_array[od_pointer].link
            
            
    




data = pd.read_csv("dataset.csv")
secondary_mem = sim_secondary_mem(1000,3,100)
global_depth = 0
dir_length = 1
ext = extensible_hash(global_depth,dir_length)

for d in data.iterrows():
    recordobj = records(d[1][0],d[1][1],d[1][2],d[1][3])
    ext.insert_record(secondary_mem,recordobj,0)
    visualise(ext.dirarray,secondary_mem,ext.od_pointer)
    print("--------------------------")
    
print(secondary_mem.bucket_array[900:910])
for i in range(900,910):
    if secondary_mem.bucket_array[i] != None:
        secondary_mem.bucket_array[i].print_bucket()






