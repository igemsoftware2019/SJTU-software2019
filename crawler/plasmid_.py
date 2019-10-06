import os,re
import urllib
from bs4 import BeautifulSoup
import lxml
import requests

file_name="/Users/url_fin.csv"
out_file_total="plasmid.csv"

def out_put_file(out_file,name,PURPOSE,DP_LAB,LAB_link,pub,pub_link,seq_link,BB_vector,BB_manu,BB_size,Vector_size,Vector_type,Mod2BB,Bac_Re,Temp,Strain,Copy_nu,insert_name,insert_type,insert_size,Prom,mutation,tag,pe5,pe3,Document_url,Document,License,License_url,Cite,Cite_url,Cite_it1,Cite_it2):
    out_f=open(out_file,"a")
    out_f.write(name+",,"+PURPOSE+",,"+DP_LAB+",,"+LAB_link+",,"+pub+",,"+pub_link+",,"+seq_link+",,"+BB_vector+",,"+BB_manu+",,"+BB_size+",,"+Vector_size+",,"+Vector_type+",,"+Mod2BB+",,"+Bac_Re+",,"+Temp+",,"+Strain+",,"+Copy_nu+",,"+insert_name+",,"+insert_type+",,"+insert_size+",,"+Prom+",,"+mutation+",,"+tag+",,"+pe5+",,"+pe3+",,"+Document_url+",,"+Document+",,"+License+",,"+License_url+",,"+Cite+",,"+Cite_url+",,"+Cite_it1+",,"+Cite_it2+"\n")

f=open(file_name,"r")
next(f)

web_list=[]



for line in f:
    link=line
    print(link)

    if link in web_list:
        pass
    else:
        web_list.append(link)

        res = requests.get(link)
        res.encoding='utf-8'
        bs=BeautifulSoup(res.text,'html.parser')  

        name=""
        PURPOSE=""
        DP_LAB=""
        LAB_link=""
        seq_link=""
        pub_link=""
        pub=""
        seq_link=""
        BB_vector=""
        BB_manu=""
        BB_size=""
        Vector_size=""
        Vector_type=""
        Mod2BB=""
        Bac_Re=""
        Temp=""
        Strain=""
        Copy_nu=""
        insert_name=""
        insert_type=""
        insert_size=""
        Prom=""
        mutation=""
        tag=""
        pe5=""
        pe3=""
        Document_url=""
        Document=""
        License=""
        License_url=""
        Cite=""
        Cite_url=""
        Cite_it1=""
        Cite_it2=""
 
        name = "".join('%s' %id for id in (bs.find(attrs={'class':'material-name'})))
        PURPOSE_re=re.compile(r"Purpose</div>[\s\S]*?</div>")
        if PURPOSE_re.findall(res.text) != []:
        	PURPOSE=re.split("<|>|\n","".join('%s' %id for id in (PURPOSE_re.findall(res.text))))[7]
        DP_LAB_re=re.compile(r"Depositing Lab</div>[\s\S]*?</div>")
        if DP_LAB_re.findall(res.text) != []:
        	DP_LAB=re.split("\n|</a>","".join('%s' %id for id in (DP_LAB_re.findall(res.text))))[4]
        	LAB_link="https://www.addgene.org"+re.split("\n|</a>|\"","".join('%s' %id for id in (DP_LAB_re.findall(res.text))))[6]
        pub_re=re.compile(r"Publication</div>[\s\S]*?</cite>")
        pub0="".join('%s' %id for id in (pub_re.findall(res.text)))
        if pub0 != "":
        	pub=(re.split("\n|</a>",pub0))[9]+(re.split("\n|</a>",pub0))[10]
        	pub_link="https://www.addgene.org"+(re.split("\n|</a>|\"",pub0))[7]
        seq_re=re.compile(r"/\d*/sequences/")
        seq_link="https://www.addgene.org"+seq_re.findall(res.text)[1]
        
        BB_vector_re=re.compile(r"Vector\sbackbone</div>[\s\S]*?</div")
        if BB_vector_re.findall(res.text) != []:
        	BB_vector = re.split("<|>|\n","".join('%s' %id for id in (BB_vector_re.findall(res.text) )))[4]
        BB_manu_re=re.compile(r"manufacturer</div>[\s\S]*?</li>")
        if BB_manu_re.findall(res.text) != []:
        	BB_manu = re.split("<|>|\n","".join('%s' %id for id in (BB_manu_re.findall(res.text) )))[3]
        BB_size_re=re.compile(r"Backbone\ssize[\s\S]*?</li>")
        if BB_size_re.findall(res.text) != []:
        	BB_size = re.split("<|>|\n","".join('%s' %id for id in (BB_size_re.findall(res.text) )))[7]
        Vector_size_re=re.compile(r"Total\svector\ssize\s\(bp\)</span>[\s\S]*?</li>")
        if Vector_size_re.findall(res.text) != []:
        	Vector_size = re.split("<|>|\n","".join('%s' %id for id in (Vector_size_re.findall(res.text) )))[3]
        Mod2BB_re=re.compile(r"Modifications\sto\sbackbone</div>[\s\S]*?</li>")
        if Mod2BB_re.findall(res.text) != []:
        	Mod2BB = re.split("<|>|\n","".join('%s' %id for id in (Mod2BB_re.findall(res.text) )))[3]
        Vector_type_re=re.compile(r"Vector\stype</div>[\s\S]*?</li>")
        if Vector_type_re.findall(res.text) != []:
        	Vector_type = re.split("<|>|\n","".join('%s' %id for id in (Vector_type_re.findall(res.text) )))[3]
        Bac_Re_re=re.compile(r"Resistance\(s\)</div>[\s\S]*?</li>")
        if Bac_Re_re.findall(res.text) != []:
        	Bac_Re = re.split("<|>|\n","".join('%s' %id for id in (Bac_Re_re.findall(res.text) )))[3]                     
        Temp_re=re.compile(r"Temperature</div>[\s\S]*?</li>")
        if Temp_re.findall(res.text) != []:
        	Temp = re.split("<|>|\n","".join('%s' %id for id in (Temp_re.findall(res.text) )))[3]
        Strain_re=re.compile(r"Strain\(s\)</div>[\s\S]*?</li>")
        if Strain_re.findall(res.text) != []:
        	Strain = re.split("<|>|\n","".join('%s' %id for id in (Strain_re.findall(res.text) )))[3]
        Copy_nu_re=re.compile(r"Copy\snumber</div>[\s\S]*?</li>")
        if Copy_nu_re.findall(res.text) != []:
        	Copy_nu= re.split("<|>|\n","".join('%s' %id for id in (Copy_nu_re.findall(res.text) )))[3]
        insert_name_re=re.compile(r"Gene/Insert\sname</div>[\s\S]*?</li>")
        if insert_name_re.findall(res.text) != []:
        	insert_name=re.split("<|>|\n","".join('%s' %id for id in (insert_name_re.findall(res.text))))[4]
        insert_type_re=re.compile(r"Species</div>[\s\S]*?</li>")
        if insert_type_re.findall(res.text) != []:
        	insert_type=re.split("<|>|\n","".join('%s' %id for id in (insert_type_re.findall(res.text))))[3]
        insert_size_re=re.compile(r"Insert\sSize\s\(bp\)</div>[\s\S]*?</li>")
        if insert_size_re.findall(res.text) != []:
        	insert_size=re.split("<|>|\n","".join('%s' %id for id in (insert_size_re.findall(res.text))))[3]
        Prom_re=re.compile(r"Promoter</span>[\s\S]*?</li>")
        if Prom_re.findall(res.text) != []:
        	Prom = re.split("<|>|\n","".join('%s' %id for id in (Prom_re.findall(res.text) )))[3]
        tag_re=re.compile(r"Fusion\sProtein</span>\s*\n\s*<ul class=\"addgene-document-list\">[\s\S]*?</ul>")
        if tag_re.findall(res.text) != []:
        	tag = re.split("<|>|\n","".join('%s' %id for id in (tag_re.findall(res.text) )))[9]
        mutation_re=re.compile(r"Mutation</div>[\s\S]*?</li>")
        if mutation_re.findall(res.text) != []:
        	mutation=re.split("<|>|\n","".join('%s' %id for id in (mutation_re.findall(res.text))))[3]
        pe5_re = re.compile(r"5\&#x2032;\ssequencing\sprimer</span>[\s\S]*?</li>")
        if pe5_re.findall(res.text) != []:
        	pe5 = re.split("<|>|\n","".join('%s' %id for id in (pe5_re.findall(res.text))))[3]
        pe3_re = re.compile(r"3\&#x2032;\ssequencing\sprimer</span>[\s\S]*?</li>")
        if pe3_re.findall(res.text) != []:
        	pe3 = re.split("<|>|\n","".join('%s' %id for id in (pe3_re.findall(res.text))))[3]
        Document_re= re.compile(r"Documents</div>[\s\S]*?</li>")
        if Document_re.findall(res.text) != []:
        	Document_url = re.split("<|>|\"|\n","".join('%s' %id for id in (Document_re.findall(res.text))))[13]
        	Document = re.split("<|>|\"|\n","".join('%s' %id for id in (Document_re.findall(res.text))))[15]
        License_re= re.compile(r"Licenses</div>[\s\S]*?</li>")
        if License_re.findall(res.text) != []:
        	License_url = "https://www.addgene.org"+re.split("<|>|\"|\n","".join('%s' %id for id in (License_re.findall(res.text))))[12]
        	License = re.split("<|>|\"|\n","".join('%s' %id for id in (License_re.findall(res.text))))[14]
        Cite_re= re.compile(r"Citing\sthis\sPlasmid</div>[\s\S]*?</li>")
        if Cite_re.findall(res.text) != []:
        	Cite_url = "https://www.addgene.org"+re.split("<|>|\"|\n","".join('%s' %id for id in (Cite_re.findall(res.text))))[12]
        	Cite = re.split("<|>|\"|\n","".join('%s' %id for id in (Cite_re.findall(res.text))))[14]
        Cite_it1_re = re.compile(r"Materials\s\&amp;\sMethods</strong>\ssection:</p>[\s\S]*?</small>")
        if Cite_it1_re .findall(res.text) != []:
        	Cite_it1 = re.split("<|>","".join('%s' %id for id in (Cite_it1_re .findall(res.text))))[8]
        Cite_it2_re  = re.compile(r"References</strong>\ssection:</p>[\s\S]*?<a\shref=")
        if Cite_it2_re .findall(res.text) != []:
        	Cite_it2 = re.split("<|>","".join('%s' %id for id in (Cite_it2_re .findall(res.text))))[12]+re.split("<|>","".join('%s' %id for id in (Cite_it2_re .findall(res.text))))[14]+re.split("<|>","".join('%s' %id for id in (Cite_it2_re .findall(res.text))))[16]
        
        out_put_file(out_file_total,name,PURPOSE,DP_LAB,LAB_link,pub,pub_link,seq_link,BB_vector,BB_manu,BB_size,Vector_size,Vector_type,Mod2BB,Bac_Re,Temp,Strain,Copy_nu,insert_name,insert_type,insert_size,Prom,mutation,tag,pe5,pe3,Document_url,Document,License,License_url,Cite,Cite_url,Cite_it1,Cite_it2)
