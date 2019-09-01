#file_path is the path where you save the csv
file_path="/Users/quyixiang/Desktop/iGEM/csv_out"

import os,re,urllib
import urllib.request
output_file_total="output_total.csv"

#define a list to save the website we have visited
web_list=[]

#define a output file to save the data
out_file_total=open(output_file_total,"w")
out_file_total.write("Entry,,Name,,Formula,,Exact mass,,Mol weight\n")
out_file_total.close()

files=os.listdir(file_path)

#define the function that can save the information
def out_put_line(out_file,entry,name,formula,exact_mass,mol_weight):
    out_f=open(out_file,"a")
    out_f.write(entry+",,"+name+",,"+formula+",,"+exact_mass+",,"+mol_weight+"\n")

#define the regular expression of the different tags
re_entry=re.compile(r'\<nobr\>Entry\<\/nobr\>')
re_name=re.compile(r'\<nobr\>Name\<\/nobr\>')
re_formula=re.compile(r'\<nobr\>Formula\<\/nobr\>')
re_exact_mass=re.compile(r'\<nobr\>Exact mass\<\/nobr\>')
re_mol_weight=re.compile(r'\<nobr\>Mol weight\<\/nobr\>')
re_pathway=re.compile(r'\<nobr\>Pathway\<\/nobr\>')
re_module=re.compile(r'\<nobr\>Module\<\/nobr\>')
re_enzyme=re.compile(r'\<nobr\>Enzyme\<\/nobr\>')
re_brite=re.compile(r'\<nobr\>Brite\<\/nobr\>')


#loop
for file in files:
    pattern=re.compile(r'[0-9a-zA-Z\_]{1,}\_entry\_list\.csv$')
    if pattern.match(file):
        file=file_path+"/"+file
        print(file)
        f=open(file,"r")
        next(f)
        
        #for every line execute the code
        for line in f:
            #to judge whether it is a compound
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
                            #print(entry_out)
                        elif re_name.search(temp_line):
                            out=te_f.readline()
                            print(out)
                            test=re.compile(r'\>[A-Za-z0-9\_\s\-\,\(\)]{1,}\;\<br\>')
                            test_line=re.compile(r'[A-Za-z0-9\_\s\-\,\(\)]{1,}\;\<br\>')
                            
                            #这里有一个问题，要是有三行就没法处理
                            if test.search(out):
                                out=te_f.readline()
                                if test_line.search(out):
                                    out=te_f.readline()
                                    out=re.findall(r'[A-Za-z0-9\_\s\-\,\;\(\)]{1,}\<br\>',out)[0]
                                    out=out.replace(">","")
                                    out=out.replace(";","")
                                    name_out=out.replace("<br","")
                                    print(name_out)
                                else:
                                    out=re.findall(r'[A-Za-z0-9\_\s\-\,\(\)]{1,}\<br\>',out)[0]
                                    name_out=out.replace("<br>","")
                                    print(name_out)
                            else:
                                out=re.findall(r'\>[A-Za-z0-9\_\s\-\,\(\)]{1,}\<br\>',out)[0]
                                out=out.replace(">","")
                                name_out=out.replace("<br","")
                                print(name_out+"\n")
                        elif re_formula.search(temp_line):
                            out=te_f.readline()
                            out=re.findall(r'\>[A-Za-z0-9\_\s\-\,\(\)]{1,}\<br\>',out)[0]
                            out=out.replace(">","")
                            formula_out=out.replace("<br","")
                            #print(formula_out)
                        elif re_exact_mass.search(temp_line):
                            out=te_f.readline()
                            out=re.findall(r'\>[A-Za-z0-9\_\.]{1,}\<br\>',out)[0]
                            out=out.replace(">","")
                            exact_mass_out=out.replace("<br","")
                            #print(exact_mass_out)
                        elif re_mol_weight.search(temp_line):
                            out=te_f.readline()
                            out=re.findall(r'\>[A-Za-z0-9\_\.]{1,}\<br\>',out)[0]
                            out=out.replace(">","")
                            mol_weight_out=out.replace("<br","")
                            #print(mol_weight_out)

                    #write the information into the output file
                    print(entry_out)
                    out_put_line(output_file_total,entry_out,name_out,formula_out,exact_mass_out,mol_weight_out)
