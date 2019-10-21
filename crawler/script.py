#!/usr/bin/env python

f=open("/Users/quyixiang/Desktop/iGEM/web_out/new_data/enzyme.csv","r")
n=0
list=[]
for line in f.readlines():
    ec=line.split(",,")[0]
    if ec in list:
        pass
    else:
        list.append(ec)
        n+=1


print(n)