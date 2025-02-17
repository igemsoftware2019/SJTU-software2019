#file_path is the path where you save the csv
file_path="/Users/quyixiang/Desktop/iGEM/csv_out"

import os,re,urllib
import urllib.request
output_file_enzyme="output_enzyme.csv"

#define a list to save the website we have visited
web_list=[]

#define a output file to save the data
out_file_enzyme=open(output_file_enzyme,"w")
out_file_enzyme.write("Entry,,Enzyme,,Link\n")
out_file_enzyme.close()

files=os.listdir(file_path)

#define the function that can save the information
def out_put_file(out_file,entry,enzyme,link):
    out_f=open(out_file,"a")
    link="https://www.kegg.jp"+link
    out_f.write(entry+",,"+enzyme+",,"+link+"\n")

#define the regular expression of the different tags
re_entry=re.compile(r'\<nobr\>Entry\<\/nobr\>')
re_enzyme=re.compile(r'\<nobr\>Enzyme\<\/nobr\>')
re_enzyme_end=re.compile(r'\<\/div\>\<\/td\>\<\/tr\>')

#loop
for file in files:
    pattern=re.compile(r'[0-9a-zA-Z\_]{1,}\_entry\_list\.csv$')
    if pattern.match(file):
        file=file_path+"/"+file
        print(file)
        f=open(file,"r")
        next(f)

        for line in f:
            if line.split(",")[2]=="compound":
                line_link=eval(line.split(",")[3])
                print(line_link)

                if line_link in web_list:
                    pass
                else:
                    web_list.append(line_link)

                    #to get the html
                    request=urllib.request.Request(line_link)
                    response=urllib.request.urlopen(request)
                    content=response.read().decode('utf-8')

                    #save the html to a tempory file
                    temp_f=open("temp.html","w")
                    temp_f.write(content)
                    temp_f.close()
                    te_f=open("temp.html","r")
                    temp_line="_"

                    while temp_line != '':
                        temp_line=te_f.readline()
                        if re_entry.search(temp_line):
                            out=te_f.readline()
                            out=re.findall(r'\<nobr\>[A-Za-z0-9\_]{1,}\&nbsp',out)[0]
                            out=out.replace("<nobr>","")
                            entry_out=out.replace("&nbsp","")
                            print(entry_out)
                        elif re_enzyme.search(temp_line):
                            temp_line=te_f.readline()
                            while re_enzyme_end.search(temp_line)==None:
                                enzyme=re.compile(r'\>[A-Za-z0-9\.]{1,}\<\/a\>')
                                link=re.compile(r'\<a\shref\=\"[A-Za-z0-9\_\/\-\?\:\.]{1,}\"\>')
                                print(enzyme.findall(temp_line))
                                print(link.findall(temp_line))
                                n=0
                                for output in enzyme.findall(temp_line):
                                    output=output.replace(">","")
                                    output_enzyme=output.replace("</a","")
                                    output=link.findall(temp_line)[n]
                                    output=output.replace("<a href=\"","")
                                    output_link=output.replace("\">","")
                                    n+=1
                                    out_put_file(output_file_enzyme,entry_out,output_enzyme,output_link)
                                temp_line= te_f.readline()