
# coding: utf-8

# In[18]:

##Imports

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os
from datetime import date as dateClass, timedelta


# In[19]:

## Declaring dictionaries for storage of data

locationDictionary={}
categoryDictionary={}
tagsDictionary={}


# In[20]:

#Date Calculations

dateCorrect=False
while dateCorrect!=True:
    dateInput=raw_input("Enter a VALID date in MM-DD-YYYY format. Example: 01-31-2018 or LEAVE BLANK for DEFAULTof past 7 days\n")
    if(dateInput==''):
        print "No Date Provided. Using a default of past 7 days data."
        dateInput1=dateClass.today() - timedelta(days=7)
        year= dateInput1.year
        month= dateInput1.month
        date= dateInput1.day
        print "Starting to scrape newsroom data for analysis...."
        break
    else:
        month=int(dateInput.split("-")[0])
        date=int(dateInput.split("-")[1])
        year=int(dateInput.split("-")[2])
        dateInput1=dateClass(year,month,date)
        if (dateInput1 <= dateClass.today()):
            dateCorrect=True
            print "Starting to scrape newsroom data for analysis...."
        else:
            print "Date entered is after today's date. Enter today's date or past date"


# In[21]:

#Making a request to the webpage and getting beautiful soup object

page = requests.get("https://www.newswire.com/newsroom")    
if page.status_code==200:   
    soup = BeautifulSoup(page.content, 'html.parser')
else:
    print "HTTP Request Rejected by: https://www.newswire.com/newsroom\tTry again later"


# In[22]:

#function to map months to month number
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

#function to generate soup object for inidivual article page
def getSoupArticle(url):
    pageArticle = requests.get(url)    
    if pageArticle.status_code==200:   
        soupArticle = BeautifulSoup(pageArticle.content, 'html.parser')
    else:
        print "HTTP Request Rejected by: "+url+"\tTry again later"
    return soupArticle

#function to extract location, category and tag data from article URLs
def getArticleData(soupArticle):
    #getting location data
    locList=soupArticle.select("p strong.date-line.color-pr")[0].get_text().strip().lower().split(",")[:-2]
    location=[]
    for loc in locList:
        loc=loc.lstrip().rstrip()
        location.append(loc)
    for loc in location:     
        if loc in locationDictionary.keys():
            locationDictionary[loc]+=1
        else:
            locationDictionary[loc]=1
    
    #getting category data
    catSoup=soupArticle.select("p[class=mb-0]")[0]
    catListLen=len(catSoup.select("a"))
    for i in range(0,catListLen):
        catList=str(catSoup.select("a")[i].get_text().encode('utf-8').lower()).split(",")
        for cat in catList:
            cat=cat.lstrip()
            if cat in categoryDictionary.keys():
                categoryDictionary[cat]+=1
            else:
                categoryDictionary[cat]=1

    #getting tag data
    tagSoup=soupArticle.select("p[class=mb-0]")[1]
    tagListLen=len(tagSoup.select("a"))
    for i in range(0,tagListLen):
        tagList=str(tagSoup.select("a")[i].get_text().encode('utf-8').lower()).split(",")
        for tag in tagList:
            if tag in tagsDictionary.keys():
                tagsDictionary[tag]+=1
            else:
                tagsDictionary[tag]=1


# In[23]:

#traversing articles using beautiful soup until the appropriate date
nextPageTraverse=True
while(nextPageTraverse):
    divs=soup.select("div.news-item-body")
    for div in divs:
        p=div.select("time.ln-date")[0]
        articleDate=p.get_text().split(" ")
        articleDay=int(str(articleDate[1]).replace(',',''))
        articleMonth=int(monthToIntMonth(str(articleDate[0]).strip()))
        articleYear=int(articleDate[2])
        if(articleYear>=year):
            if(articleMonth>=month):
                if(articleDay>=date):
                    url="https://www.newswire.com/"+div.select("a.content-link")[0]['href']
                    print str(articleMonth) + "/" + str(articleDay) + "/" + str(articleYear)+" -- "+url
                    soupArticle=getSoupArticle(url)
                    getArticleData(soupArticle)
                else:
                    nextPageTraverse=False
                    break
            else:
                nextPageTraverse=False
                break
        else:
            nextPageTraverse=False
            break
    nextPage=soup.select("div.chunkination.chunkination-centered ul")[2]
    try:
        nextPage=str(nextPage.find("a")['href'])
        url="https://www.newswire.com/"+nextPage
        page = requests.get(url)    
        if page.status_code==200:   
            soup = BeautifulSoup(page.content, 'html.parser') 
    except:
        print 'No Next Page. End of results'
        nextPageTraverse=False


# In[24]:

print "Location Analysis Graph is save locally in your CWD: "+os.getcwd()+"\LocationAnalysis.png"
print "Printing the Location Analysis Table:\n"

#generating LocationAnalysis bar graph
fig, ax = plt.subplots(figsize=(35,12))
plt.bar(range(len(locationDictionary)), locationDictionary.values(), align='center')
plt.xticks(range(len(locationDictionary)), locationDictionary.keys(),rotation='vertical', fontsize='12')
plt.xlabel('Locations')
plt.ylabel('Number of Articles')
plt.savefig('LocationAnalysis.png')

#generating location analysis frequency table
locDict1={}
maxLen=0
for k,v in locationDictionary.iteritems():
    k=k.encode('ascii','ignore')
    locDict1[k]=v
    if(maxLen<len(k)):
        maxLen=len(k)
    
print "Location"+' '*(maxLen+2)+"| Number of Article"
print '-'*(maxLen+32)
for k,v in locDict1.iteritems():
    print k+' '*(maxLen-len(k)+10)+"|"+' '*10+str(v)


# In[25]:

print "Category Analysis Graph is save locally in your CWD: "+os.getcwd()+"\CategoryAnalysis.png"
print "Printing the Category Analysis Table:\n"

fig, ax = plt.subplots(figsize=(35,12))
plt.bar(range(len(categoryDictionary)), categoryDictionary.values(), align='center')
plt.xticks(range(len(categoryDictionary)), categoryDictionary.keys(),rotation='vertical', fontsize='12')
plt.xlabel('Categories')
plt.ylabel('Number of Articles')
plt.savefig('CategoryAnalysis.png')

maxLen=0
for k,v in categoryDictionary.iteritems():
#     k=k.encode('ascii','ignore')
#     locDict1[k]=v
    if(maxLen<len(k)):
        maxLen=len(k)

print "Category"+' '*(maxLen+2)+"| Number of Article"
print '-'*(maxLen+32)
for k,v in categoryDictionary.iteritems():
    print k+' '*(maxLen-len(k)+10)+"|"+' '*10+str(v)


# In[26]:

print "The Tags are mostly unique for each article and thus plotting a bar graph wouldn't be feasible/readble. We thus only have a table for the same\n\n"

maxLen=0
for k,v in tagsDictionary.iteritems():
    if(maxLen<len(k)):
        maxLen=len(k)

print "Tags"+' '*(maxLen+6)+"| Number of Article"
print '-'*(maxLen+32)
for k,v in tagsDictionary.iteritems():
    print k+' '*(maxLen-len(k)+10)+"|"+' '*10+str(v)
    
    
print "Please DONT FORGET to take a look at the LocationAnalysis and CategoryAnalysis plots saved locally in your CWD: "+os.getcwd()

