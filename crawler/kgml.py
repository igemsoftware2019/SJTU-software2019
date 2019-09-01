import urllib.request
import urllib
import re

web=[]
temp1=''
temp2=''
url="https://www.genome.jp/kegg-bin/show_pathway?map=map00720&show_description=show"
request=urllib.request.Request(url)
response=urllib.request.urlopen(request)
content=response.read().decode('utf-8')
pattern=re.compile('<option value="(.*?)">.*?</option>',re.S)
items3=re.findall(pattern,content)
print('原核生物：')
for i in items3:
    #print(i)
    temp1='http://rest.kegg.jp/get/'+i+'00720/kgml'
    print(temp1)#储存原核生物的固氮物种kgml的网址
    
url='https://www.genome.jp/kegg-bin/show_pathway?org_name=crb&mapno=00710&mapscale=&show_description=show'
request=urllib.request.Request(url)
response=urllib.request.urlopen(request)
content=response.read().decode('utf-8')
pattern=re.compile('<option value="(.*?)">.*?</option>',re.S)
items4=re.findall(pattern,content)
print('固氮器官：')
for i in items4:
    #print(i)
    temp2='http://rest.kegg.jp/get/'+i+'00710/kgml'
    print(temp2)#储存相关固氮器官的kgml的网址