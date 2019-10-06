import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import json
import pandas

file_name="/Users/url2.csv"
f=open(file_name,"r")
next(f)

def parseListLinks(url):
    res = requests.get(url)
    result={}
    res.encoding='utf-8'
    bs=BeautifulSoup(res.text,'html.parser')  
    pattern = re.compile(r'\d+') 
    re1=bs.find_all(attrs={'div':'item-main-col col-xs-9'})
    return re1
    
for line in f:
    link=line
    print(link)

    if link in web_list:
        pass
    else:
        web_list.append(enzyme_link)

        #to get the html
        request=urllib.request.Request(link)
        response=urllib.request.urlopen(request)
        content=response.read().decode('utf-8')

        newsary= parseListLinks(newsurl)
        news_total.extend(newsary)

print('抓取结束')                                 
df=pandas.DataFrame(news_total)
df.to_csv('pla.csv')
