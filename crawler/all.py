import urllib.request
import urllib
import re

web=[]
temp1=''
pro=[]
temp2=''
euk=[]
url="https://www.genome.jp/kegg-bin/show_pathway?map=map00720&show_description=show"
request=urllib.request.Request(url)
response=urllib.request.urlopen(request)
content=response.read().decode('utf-8')
pattern=re.compile('<option value="(.*?)">.*?</option>',re.S)
items3=re.findall(pattern,content)
#print('原核生物：')
for i in items3:
    #print(i)
    temp1='http://rest.kegg.jp/get/'+i+'00720/kgml'
    pro.append(temp1)
    #print(temp1)#储存原核生物的固氮物种kgml的网址
    
url='https://www.genome.jp/kegg-bin/show_pathway?org_name=crb&mapno=00710&mapscale=&show_description=show'
request=urllib.request.Request(url)
response=urllib.request.urlopen(request)
content=response.read().decode('utf-8')
pattern=re.compile('<option value="(.*?)">.*?</option>',re.S)
items4=re.findall(pattern,content)
#print('固氮器官：')
for i in items4:
    #print(i)
    temp2='http://rest.kegg.jp/get/'+i+'00710/kgml'
    euk.append(temp2)
    #print(temp2)#储存相关固氮器官的kgml的网址

all=pro[6::]+euk[10::]#存放了所有光合作用相关生物的kgml网址



#needed libraries, pip install them.
from requests_html import HTMLSession

#modify another url if you need
#url="http://rest.kegg.jp/get/mox00710/kgml"

url=url[0:2:]
for url in all:
    session = HTMLSession()
    r = session.get(url)

    if url[27]=='0':
        name=url[24:27]
    else:
        name=url[24:28]#存取物种名字的简写
        
    #get pathway information
    pathway_name = ""
    pathway_org = ""
    pathway_number = ""
    pathway_title = ""
    pathway_image = ""
    pathway_link = ""

    def write_special_tag(output):
        print("pathway name,pathway org,pathway number,pathway title,pathway image,pathway link",file=output)

    def write_special_content(output):
        print("{0},{1},{2},{3},\"{4}\",\"{5}\"".format(pathway_name, pathway_org, pathway_number, pathway_title,pathway_image, pathway_link),file=output)



    if True:
        pathway = r.html.find("pathway",first=True)
        if pathway is not None:
            pathway_attrs = pathway.attrs
            pathway_name = pathway_attrs["name"]
            pathway_org = pathway_attrs["org"]
            pathway_number = pathway_attrs["number"]
            pathway_title = pathway_attrs["title"]
            pathway_image = pathway_attrs["image"]
            pathway_link = pathway_attrs["link"]

    #get entry information
    filename=name+"_entry_list.csv"
    with open(filename, "w") as output:
        print("entry id,name,type,link,graphics name,fgcolor,bgcolor,type,x,y,width,height,",file=output, end="")
        write_special_tag(output)
        current_list = r.html.find("entry")
        for cur in current_list :
            cur_attrs = cur.attrs
            print("{0},{1},{2},\"{3}\",".format(cur_attrs["id"],cur_attrs["name"],cur_attrs["type"],cur_attrs["link"]),  end="",file=output)
            graphics = cur.find("graphics", first=True)
            if graphics is not None:
                graphics_attrs = graphics.attrs
                print("\"{0}\",{1},{2},{3},{4},{5},{6},{7},".format(graphics_attrs["name"], graphics_attrs["fgcolor"], graphics_attrs    ["bgcolor"], graphics_attrs["type"], graphics_attrs["x"], graphics_attrs["y"], graphics_attrs["width"],     graphics_attrs["height"]),end="",file=output)
            else:
                print(",,,,,,,,",end="",file=output)
    
            write_special_content(output)

    #get relation information
    filename=name+"_relation_list.csv"
    with open(filename, "w") as output:
        print("relation entry1,entry2,type,subtype name,value,",end="",file=output)
        write_special_tag(output)
        current_list = r.html.find("relation")
        for cur in current_list :
            cur_attrs = cur.attrs
            print("{0},{1},{2},".format(cur_attrs["entry1"],cur_attrs["entry2"],cur_attrs["type"]),  end="",file=output)
            subtype = cur.find("subtype", first=True)
            if subtype is not None:
                subtype_attrs = subtype.attrs
                print("{0},{1},".format(subtype_attrs["name"], subtype_attrs["value"]),end="",file=output)
            else:
                print(",,",end="",file=output)
            write_special_content(output)
            

    max_substract_count = 1
    max_product_count = 1

    if True:
        current_list = r.html.find("reaction")
        for cur in current_list :
            substrate_list = cur.find("substrate")
            if substrate_list is not None and len(substrate_list) > max_substract_count:
                max_substract_count = len(substrate_list)
            product_list = cur.find("product")
            if product_list is not None and len(product_list) > max_product_count:
                max_product_count = len(product_list)

    #get reaction information
    filename=name+"_reaction_list.csv"
    with open(filename, "w") as output:
        print("reaction id,name,type,",file=output, end="")
        for i in range(max_substract_count):
            print("substrate id{0},substrate name{1},".format(i+1, i+1),end="",file=output)
        for i in range(max_product_count):
            print("product id{0},product name{1},".format(i+1, i+1),end="",file=output)
        write_special_tag(output)

        current_list = r.html.find("reaction")
        for cur in current_list :
            cur_attrs = cur.attrs
            print("{0},{1},{2},".format(cur_attrs["id"],cur_attrs["name"],cur_attrs["type"]),  end="",file=output)
            substrate_list = cur.find("substrate")
            product_list = cur.find("product")
    
            if substrate_list is not None:
                for s in substrate_list:
                    sa = s.attrs
                    print("{0},{1},".format(sa["id"],sa["name"]), end="",file=output)

            for i in range(max_substract_count - len(substrate_list)):
                print(",,", end="",file=output)
                
            if product_list is not None:
                for p in product_list:
                    pa = p.attrs
                    print("{0},{1},".format(pa["id"],pa["name"]), end="",file=output)
    
            for i in range(max_product_count - len(product_list)):
                print(",,", end="",file=output)
            
            write_special_content(output)
