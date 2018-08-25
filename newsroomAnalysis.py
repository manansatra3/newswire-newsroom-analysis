
# coding: utf-8

# In[85]:

import requests
from bs4 import BeautifulSoup


# In[158]:

locationDictionary={}
categoryDictionary={}
tagsDictionary={}


# In[86]:

dateInput=raw_input("Enter a VALID date in MM-DD-YYYY format. Example: 01-31-2018\t")
print(dateInput)
month=int(dateInput.split("-")[0])
date=int(dateInput.split("-")[1])
year=int(dateInput.split("-")[2])
print(date)
print(month)
print(year)


# In[87]:

page = requests.get("https://www.newswire.com/newsroom")    
if page.status_code==200:   
    soup = BeautifulSoup(page.content, 'html.parser') 


# In[159]:

def monthToIntMonth(articleMonth):
    switcher = {
            "Jan":1,
            "Feb":2,
            "Mar":3,
            "Apr":4,
            "May":5,
            "Jun":6,
            "Jul":7,
            "Aug":8,
            "Sep":9,
            "Oct":10,
            "Nov":11,
            "Dec":12
        }
    return switcher.get(articleMonth, "Invalid month")

def getSoupArticle(url):
    pageArticle = requests.get(url)    
    if pageArticle.status_code==200:   
        soupArticle = BeautifulSoup(pageArticle.content, 'html.parser')
    else:
        print "Error while parsing the Article Page with URL: "+url  
    return soupArticle

def getArticleData(soupArticle):
    category=""
    tags=""
    locList=soupArticle.select("p strong.date-line.color-pr")[0].get_text().strip().split(",")[:-2]
    location=""
    for loc in locList:
        location=(location+str(loc)).lower();
    print location
    if location in locationDictionary.keys():
        locationDictionary[location]=+1
    else:
        locationDictionary[location]=1


# In[160]:

divs=soup.select("div.news-item-body")
# print divs
for div in divs:
    p=div.select("time.ln-date")[0]
    articleDate=p.get_text().split(" ")
    articleDay=int(str(articleDate[1]).replace(',',''))
    print "Day:", articleDay
    articleMonth=int(monthToIntMonth(str(articleDate[0]).strip()))
    print "Month:", articleMonth
    articleYear=int(articleDate[2])
    print "Year:", articleYear
    if(articleYear>=year):
        if(articleMonth>=month):
            if(articleDay>=date):
                url="https://www.newswire.com/"+div.select("a.content-link")[0]['href']
                print url
                soupArticle=getSoupArticle(url)
                getArticleData(soupArticle)
                continue
            else:
                break
        else:
            break
    else:
        break
    
print locationDictionary


# In[ ]:



