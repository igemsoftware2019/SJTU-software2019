#!/usr/bin/env python

file_path="/Volumes/DATA/igem/database2/"
import os,re,shutil

list=["enzrxns.dat","enzymes.col","genes.col","genes.dat","pathways.col","pathways.dat","reactions.dat","pubs.dat","species.dat","compounds.dat"]

pattern = re.compile(r"^\d.+")

for dir in os.listdir(file_path):
    if "cyc" in dir:


        temp=file_path+dir
        print(temp)

        temp_list=os.listdir(temp)

        for file in temp_list:
            if pattern.findall(file):
                temp_dir=pattern.findall(file)[0]

        dir_name=file_path+dir+"/"+temp_dir+"/data"
        dir_file=os.listdir(dir_name)
        for file_name in dir_file:
            if file_name in list:
                file_path_ori=dir_name+"/"+file_name
                file_path_new=temp+"/"+file_name
                shutil.copyfile(file_path_ori,file_path_new)
        shutil.rmtree(temp+"/"+temp_dir)

        os.remove(temp+"/default-version")
