#!/usr/bin/env python
import os
from fuzzywuzzy import fuzz

def delete_line_mark(list):
    out=""
    for data in list:
        data=data.replace("\n","")
        if out=="":
            out=data
        else:
            out=out+",,"+data
    return out

def spli(file):

    line_list=file.readlines()
    needed_line_list=[]
    temp=0

    for line in line_list:

        if line == "//\n":        
            needed_line_list.append(line_list.index(line,temp+1))
            temp=line_list.index(line,temp+1)
            
    list_length=len(needed_line_list)
    final_list=[]

    for i in range(list_length-1):

        if i == 0:
            tem=0

            for line in line_list:

                if line == "#\n":
                    num=line_list.index(line,tem+1)+1
                    tem=line_list.index(line,tem+1)

                    if "UNIQUE-ID - " not in line_list[num]:
                        pass

                    else:
                        start=num-1
                        break

        else:
            start=int(needed_line_list[i-1])
        
        end=int(needed_line_list[i])

        new_line=delete_line_mark(line_list[start:end])
        final_list.append(new_line)

    return final_list

path="/Volumes/DATA/igem/database2/"

list=[]
for folder in os.listdir(path):
    if "cyc" in folder:

        f_temp=open(path+folder+"/pathways.dat","r",errors="ignore")
        inf_list=spli(f_temp)
        for inf in inf_list:
            sing=inf.split(",,")
            for info in sing:
                if "COMMON-NAME" in info:
                    out=info
                else:
                    pass
            
            name=out.replace("COMMON-NAME - ","")
            #print(name)
            if fuzz.ratio("heliocides",name)>=60 or "heliocides" in name:
                if name in list:
                    pass
                else:
                    list.append(name)
                print(name,folder)
print(len(list))
print(list)
