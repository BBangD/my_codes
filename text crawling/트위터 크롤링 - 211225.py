# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.6
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as condition
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import datetime as dt
import re
#import traceback #디버깅용
browser = webdriver.Chrome('chromedriver.exe')

date = []
user = []
text = []
tags = []
def scrape():
    html= browser.page_source
    parsed = bs(html,'html.parser')
    tweets = parsed.find_all('article')
    for tweet in tweets:
        global date
        global user
        global text
        global tags

        try:
            date.index(tweet.time['datetime'])
        except:
            try:
                date.append(tweet.time['datetime'])
                user.append(tweet.a['href'].replace('/','',1))
                string = tweet.find('div', attrs = {'lang':'ko'}).text     #변경
                splitted = string.replace('\n',' ').split('#')
                cleansed = ''
                extracted = []

                for chunk in splitted:
                    if chunk == splitted[0]:
                        cleansed += chunk
                    else:
                        if chunk.find(' ') != -1:
                            extracted.append((chunk.split(' ', 1))[0])
                            cleansed += ' ' + (chunk.split(' ', 1))[1]
                        else:
                            extracted.append(chunk)

                while cleansed.find('  ') != -1:
                    cleansed = cleansed.replace('  ',' ')

                text.append(cleansed)
                if extracted != []:
                    tags.append(' '.join(extracted))
                else:
                    tags.append('')
            except:
                date = date[0:len(tags)]
                user = user[0:len(tags)]
                text = text[0:len(tags)]
                tags = tags[0:len(tags)]

times = str(dt.datetime.now())[:str(dt.datetime.now()).index('.')]
times= re.sub(' ', '-', times)
times = re.sub(':', '-', times)
search = '케타포' #변경
endWhenNumb = 10000000
stopWhenDelay = 50
alertEvery = 50
fileName = search+'_'+times + '.csv'
timespace = 2 #변경
startdate = dt.date(year=2021,month=12,day=13) #변경
enddate = dt.date(year=2021, month=12, day=15) #변경
untildate = startdate + dt.timedelta(days=timespace)


while not enddate <= startdate:

    url = 'https://twitter.com/search?q=' + search + '%20until%3A'+str(untildate)+'%20since%3A'+str(startdate)+'&src=typed_query&f=live'

    browser.get(url)
    try:
        
        WebDriverWait(browser,10).until(condition.presence_of_element_located((By.TAG_NAME,'article')))
    except:
        continue
    alertNumb = alertEvery
    delayCount = stopWhenDelay
    while len(text) + 1 <= endWhenNumb:
        scrollBefore = browser.execute_script('return window.scrollY')
        browser.execute_script('window.scrollTo(0, window.scrollY + 1000)')
        scrollAfter = browser.execute_script('return window.scrollY')
        if scrollBefore == scrollAfter:
            time.sleep(0.1)
            delayCount -= 1
            if delayCount == 0:
                scrape()
                break
                
        else:
            delayCount = stopWhenDelay
            numbOfDataBefore = len(text) + 1
            scrape()
            numbOfDataAfter = len(text) + 1
            if(numbOfDataBefore <= alertNumb <= numbOfDataAfter):
                print(str(numbOfDataAfter) + '/' + str(endWhenNumb) + ' datas scraped')
                alertNumb += alertEvery
    startdate = untildate+dt.timedelta(days=1)
    untildate += dt.timedelta(days = timespace+1)
    
print("Finishing the application... The data will be saved as '" + fileName + "'")
pd.DataFrame({'date':date, 'user':user, 'text':text, 'tags':tags}).reset_index(drop = True).to_csv(fileName, index = False)
