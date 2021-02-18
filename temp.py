#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 00:23:35 2021

@author: yashaswi
"""

       # if index < self.dir_length:
        #     target = self.dirarray[index].pointer
        #     #record variables
        #     record_bucket = simobject.bucket_array[target]
        #     depth = record_bucket.depth
        #     link = record_bucket.link
        #     records_array = []
        #     self.get_records_overflow(simobject,records_array,record_bucket)
        #     #new bucket creation
        #     simobject.bucket_array[simobject.current_index] = simobject.new_record_bucket(depth + 1)
        #     new_target = simobject.current_index
        #     simobject.current_index += 1
        #     #rearrange pointers
        #     target_list = []
        #     for i in range(len(self.dirarray)):
        #         if self.dirarray[i].pointer == target:
        #             target_list.append(i)
        #     l = len(target_list)
        #     for i in range(l//2,l):
        #         self.dirarray[target_list[i]].pointer = new_target
            
        #     #reset old bucket
        #     simobject.bucket_array[target] = simobject.new_record_bucket(depth + 1)
            
        #     for i in records_array:
        #         self.insert_record(simobject, i, flag)
            
        # else:
            
            
            