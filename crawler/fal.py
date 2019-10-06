import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import json
import pandas
file_name="/Users/url.csv"
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
        s = str(news_total[i]).replace('[','').replace(']','')
        s = s.replace("'",'').replace(',','') +'\n'   
        file.write(s)
file.close()
print('odk')  
