#!/usr/bin/env python
import os
list=os.listdir("/Volumes/DATA/igem/database2")
new_list=[]
for file in list:
    if "cyc" in file:
        new_list.append(file)
print(new_list[7])
