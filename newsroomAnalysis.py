
# coding: utf-8

# In[58]:

import requests
from bs4 import BeautifulSoup


# In[59]:

locationDictionary={}
categoryDictionary={}
tagsDictionary={}


# In[60]:

dateInput=raw_input("Enter a VALID date in MM-DD-YYYY format. Example: 01-31-2018\n")
print(dateInput)
month=int(dateInput.split("-")[0])
date=int(dateInput.split("-")[1])
year=int(dateInput.split("-")[2])
# print(date)
# print(month)
# print(year)


# In[61]:

page = requests.get("https://www.newswire.com/newsroom")    
if page.status_code==200:   
    soup = BeautifulSoup(page.content, 'html.parser') 


# In[70]:

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
    
    locList=soupArticle.select("p strong.date-line.color-pr")[0].get_text().strip().lower().split(",")[:-2]
    location=[]
    for loc in locList:
        loc=loc.encode('ascii').lstrip().rstrip()
        location.append(loc)
    for loc in location:     
        if loc in locationDictionary.keys():
            locationDictionary[loc]+=1
        else:
            locationDictionary[loc]=1
        
    catSoup=soupArticle.select("p[class=mb-0]")[0]
    catListLen=len(catSoup.select("a"))
    for i in range(0,catListLen):
        catList=str(catSoup.select("a")[i].get_text().encode('ascii').lower()).split(",")
        for cat in catList:
            cat=cat.lstrip()
            if cat in categoryDictionary.keys():
                categoryDictionary[cat]+=1
            else:
                categoryDictionary[cat]=1

    
    tagSoup=soupArticle.select("p[class=mb-0]")[1]
    tagListLen=len(tagSoup.select("a"))
    for i in range(0,tagListLen):
        tagList=str(tagSoup.select("a")[i].get_text().encode('ascii').lower()).split(",")
        for tag in tagList:
            if tag in tagsDictionary.keys():
                tagsDictionary[tag]+=1
            else:
                tagsDictionary[tag]=1


# In[71]:

nextPageTraverse=True
while(nextPageTraverse):
    divs=soup.select("div.news-item-body")
    for div in divs:
        p=div.select("time.ln-date")[0]
        articleDate=p.get_text().split(" ")
        articleDay=int(str(articleDate[1]).replace(',',''))
    #     print "Day:", articleDay
        articleMonth=int(monthToIntMonth(str(articleDate[0]).strip()))
    #     print "Month:", articleMonth
        articleYear=int(articleDate[2])
    #     print "Year:", articleYear
        print str(articleMonth) + "/" + str(articleDay) + "/" + str(articleYear)
        if(articleYear>=year):
            if(articleMonth>=month):
                if(articleDay>=date):
                    url="https://www.newswire.com/"+div.select("a.content-link")[0]['href']
                    print url
                    soupArticle=getSoupArticle(url)
                    getArticleData(soupArticle)
                else:
                    break
            else:
                break
        else:
            break
        

    print locationDictionary
    print "\n\n\n"
    print categoryDictionary
    print "\n\n\n"
    print tagsDictionary


# In[73]:




# In[ ]:



