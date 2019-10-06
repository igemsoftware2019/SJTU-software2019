import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import json
import pandas
file_name="/Users/sion/url.csv"
news_total=[]

f=open(file_name,"r")
next(f)
re0=re.compile(r'/\d+/') 

#for every line execute the code
for line in f:
    if re0.search(line):
        output_link="".join(re0.findall(line))
        print(output_link)
        real_link="https://www.addgene.org"+output_link
        news_total.append(real_link)


print('抓取结束')                                 
file= open("/Users/sion/url2.csv","w")
for i in range(len(news_total)):
        s = str(news_total[i]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择
        s = s.replace("'",'').replace(',','') +'\n'   #去除单引号，逗号，每行末尾追加换行符
        file.write(s)
file.close()
print('odk')  