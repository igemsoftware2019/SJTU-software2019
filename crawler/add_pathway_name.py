#!/usr/bin/env python
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


f=open("/Volumes/DATA/species_final.sql","r")

f_out=open("/Volumes/DATA/species_real_final.sql","w")

lines=f.readlines()
n=0
for line in lines:
    if "insert into species value" in line:
        n+=1
        print(n)
        f_out.write(line)
        #print(line.split(", \"")[1])
        foldername=line.split(", \"")[1].replace("\"","")
        f_read=open("/Volumes/DATA/igem/database2/"+foldername+"/pathways.dat","r",errors='ignore')
        read_list=spli(f_read)
    elif "insert into pathway value" in line:
        line_split=line.split("\" ,\"")[1].split("\", \"")[0]
        uniqueid="UNIQUE-ID - "+line_split
        for pathway in read_list:
            if uniqueid in pathway:
                pathway_list=pathway.split(",,")
                for single_info in pathway_list:
                    if "COMMON-NAME - " in single_info:
                        name=single_info.replace("COMMON-NAME - ","")
                        break
                break
        out=(line.split("\" ,\"")[0]+"\" ,\""+name+"\", \""+line.split("\" ,\"")[1]).replace("\" ,\"","\", \"")
        #print(out)
        f_out.write(out)
    else:
        f_out.write(line)
        
