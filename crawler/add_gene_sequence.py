#!/usr/bin/env python
import os
file_list=os.listdir("/Volumes/DATA/igem/database2")
new_file_list=[]
for file in file_list:
    if "cyc" in file:
        new_file_list.append(file)


f=open("/Volumes/DATA/igem/species_add_compound.sql","r")
f_out=open("/Volumes/DATA/igem/species_add_compound_add_gene_sequence.sql","w")

lines=f.readlines()
n=0
for line in lines:
    if "insert into species value" in line:
        n+=1
        f_out.write(line)
    elif "insert into gene value" in line:
        sequence="\"\""
        name=line.split("\",")[1].replace("\"","").replace(" ","")+","

        f_name="/Volumes/DATA/sequence/"+new_file_list[n-1]+"_sequence.csv"
        if os.path.exists(f_name):

            temp_f=open(f_name,"r")
            for li in temp_f.readlines():
                if name in li:
                    sequence="\""+li.split(",")[1].replace("\n","")+"\""

        
        new_line=line.replace("\"\"",sequence)
        f_out.write(new_line)
    else:
        f_out.write(line)
        
