#!/usr/bin/env python

f=open("/Users/quyixiang/Desktop/iGEM/sql/modify_sql/final/species.sql","r")
line_list=f.readlines()
def spli(file):

    need_line_list=[]
    temp=0

    for line in line_list:
        if "insert into species value" in line:
            need_line_list.append(line_list.index(line,temp+1))
            temp=line_list.index(line,temp+1)
    print(need_line_list)
    return need_line_list
    
list=spli(line_list)
list.append(int("5013629"))

print(line_list[47815])


for i in list:
    if list.index(i)!=101:
        name=line_list[i].split(", \"")[1].replace("\"","")
        f_out=open("/Users/quyixiang/Desktop/iGEM/sql/modify_sql/new_final/"+name+".sql","w")
        f_out.writelines(line_list[i:list[list.index(i)+1]])

