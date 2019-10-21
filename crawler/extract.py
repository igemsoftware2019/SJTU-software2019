import re,os
real_list=os.listdir("/Volumes/DATA/igem/database2")

f=open("/Users/quyixiang/Desktop/plant_name.html","r")
list= f.readlines()

cycname=re.compile(r'href\=\".+\"\>.+\<\/a\>\<\/h2\>\n')
plantname=re.compile(r"\"\>[A-Za-z ]+\<\/a\>\<\/div\>\<\/div\>\<\/div\>")
dict={}
for line in list:
    if cycname.findall(line):

        foldername=re.sub(r"href\=.+\"\>","",cycname.findall(line)[0]).replace("</a></h2>\n","")
        foldername=re.sub(" \d\.\d$","",foldername)
        #print(foldername)
        index=list.index(line)
        while "<div class=\"field-group-htabs-wrapper" not in list[index]:
            index+=1
        target_line=list[index]

        #print(target_line)
        if plantname.findall(target_line)!=[]:
            if dict.__contains__(foldername):
                pass
            else:
                plant=plantname.findall(target_line)[0].replace("\">","").replace("</a></div></div></div>","")
                dict[foldername]=plant
'''                #print(plant)
key_list=[]
for key in dict.keys():
    key_list.append(key.lower())
for data in real_list:
    if data in key_list:
        pass
    else:
        print(data)
        '''
for key in dict.keys():

    print(key.lower()+",,"+dict[key])
