#!/usr/bin/env python
import os
file_list=os.listdir("/Volumes/DATA/igem/database2")
new_file_list=[]
for file in file_list:
    if "cyc" in file:
        new_file_list.append(file)

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

f=open("/Volumes/DATA/igem/species_reaction.sql","r")
f_out=open("/Volumes/DATA/igem/species_reaction_add_enzyme.sql","w")

lines=f.readlines()
n=0
for line in lines:
    if "insert into species value" in line:
        n+=1
        f_out.write(line)
        temp_file="/Volumes/DATA/igem/database2/"+new_file_list[n-1]+"/reactions.dat"
        print(temp_file)
        temp_f=open(temp_file,"r",errors='ignore')
        temp_list=spli(temp_f)

    elif "insert into reaction value" in line:
        enzymaticreaction=""

        id=line.split(", \"")[1].replace("\"","").replace(" ","")+","
        uniqueid="UNIQUE-ID - "+id

        for info in temp_list:
            if uniqueid in info:
                single_info=info.split(",,")
                for sin_info in single_info:
                    if "ENZYMATIC-REACTION" in sin_info:
                        temp_enzymicreaction=sin_info.replace("ENZYMATIC-REACTION - ","")
                        if enzymaticreaction=="":
                            enzymaticreaction=temp_enzymicreaction
                        else:
                            enzymaticreaction=enzymaticreaction+",,"+temp_enzymicreaction
        enzymaticreaction="\""+enzymaticreaction+"\""
        out=line.replace("\")\n","\", "+enzymaticreaction+")\n")
        f_out.write(out)

    else:
        f_out.write(line)


