#!/usr/bin/python
file_name="/Users/sion/Desktop/team_2017.txt"
           
import os,re,urllib
import urllib.request
out_file="team_out_2017.txt"

web_list=[]

def out_put_line(teamlink):
    out_f=open(out_file,"a")
    out_f.write(teamlink)

f=open(file_name,"r")
next(f)

for line in f:
    team_link=line
    print(team_link)

    if team_link in web_list:
        pass
    else:
        web_list.append(team_link)

        request=urllib.request.Request(team_link)
        response=urllib.request.urlopen(request)
        content=response.read().decode('utf-8')

        temp_f=open("temp.html","w")
        temp_f.write(content)
        temp_f.close()

        te_f=open("temp.html","r")
        temp_line=te_f.read()
        print(temp_line.find("delete"))
        m = temp_line.find("delete")
        if m == -1 : 
            print("not find!")
            out_put_line(team_link)  





