#file_path is the path where you save the csv
file_path="/Users/quyixiang/Desktop/iGEM/csv_out"

import os,re,urllib
import urllib.request
output_file_pathway="output_pathway.csv"

#define a list to save the website we have visited
web_list=[]

#define a output file to save the data
out_file_pathway=open(output_file_pathway,"w")
out_file_pathway.write("Entry,,Pathway,,Pathway Name,,Link\n")
out_file_pathway.close()

files=os.listdir(file_path)

#define the function that can save the information
def out_put_file(out_file,entry,pathway,pathway_name,link):
    out_f=open(out_file,"a")
    link="https://www.kegg.jp"+link
    out_f.write(entry+",,"+pathway+",,"+pathway_name+",,"+link+"\n")

#define the regular expression of the different tags
re_entry=re.compile(r'\<nobr\>Entry\<\/nobr\>')
re_pathway=re.compile(r'\<nobr\>Pathway\<\/nobr\>')

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
                        elif re_pathway.search(temp_line):
                            temp_line=te_f.readline()
                            pathway=re.compile(r'\>[a-z0-9]{1,}\<\/a\>')
                            pathway_name=re.compile(r'\<td\>[A-Za-z0-9\s\_\,\/\-\(\)]{1,}\<\/td\>')
                            link=re.compile(r'\<a\shref\=\"[0-9A-Za-z\/\-\_\?\+]{1,}\"\>')
                            print(pathway_name.findall(temp_line))
                            n=0
                            for output in pathway.findall(temp_line):
                                output=output.replace(">","")
                                output_pathway=output.replace("</a","")
                                output=pathway_name.findall(temp_line)[n]
                                output=output.replace("</td>","")
                                output_pathway_name=output.replace("<td>","")
                                output=link.findall(temp_line)[n]
                                output=output.replace("<a href=\"","")
                                output_link=output.replace("\">","")
                                n+=1
                                out_put_file(output_file_pathway,entry_out,output_pathway,output_pathway_name,output_link)
