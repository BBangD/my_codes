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
#0. setting
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import datetime as dt 
import pandas as pd 
import re
import numpy as np

#TIME VARIABLES
LOADING = 3
SCROLL = 1

'''
2~4단계 : 점포명 & 점포별 url 크롤링
5단계 : 점포별 리뷰 크롤링
'''

df = pd.read_csv('시군구csv.csv',encoding='cp949')
geolist=df.columns.tolist()


path="chromedriver.exe"
browser = webdriver.Chrome(path)
language = "ko"
keyword = ['블루보틀']
LOADING = 3
SCROLL = 1
global time

#--------------------------------------------


#1. 활용할 함수 정의

#xpath(a)의 버튼을 누르는 함수
def btn_xpath(a) :

    button = browser.find_element_by_xpath(a)
    button.click()
    time.sleep(LOADING)

#selector(a)의 버튼을 누르는 함수
def btn_selector(a) :
    button = browser.find_element_by_css_selector(a)
    button.click()
    time.sleep(LOADING)

#--------------------------------------------
for keyword in keyword:
    name_list = []
    url_list = []

    #2. url_set - 전국 식당명(keyword) 검색
    for area in geolist:

        url = "https://www.google.com/maps/search/" + area +" 주변 "+ keyword
        browser.get(url)
        browser.implicitly_wait(3)


    #--------------------------------------------


    #3. Crawling - 전국 식당의 각 점포이름 및 상세페이지 url



        cnt = 0
        while (1) :
            try :
                #스크롤 다운
                print("Scrolling...")
                num_of_pagedowns = 5
                while (num_of_pagedowns > 0):
                    try:
                        scroll = browser.find_element_by_css_selector('#pane > div > div.Yr7JMd-pane-content.cYB2Ge-oHo7ed > div > div > div.siAUzd-neVct.section-scrollbox.cYB2Ge-oHo7ed.cYB2Ge-ti6hGc.siAUzd-neVct-Q3DXx-BvBYQ > div.siAUzd-neVct.section-scrollbox.cYB2Ge-oHo7ed.cYB2Ge-ti6hGc.siAUzd-neVct-Q3DXx-BvBYQ')
                        browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scroll)
                        time.sleep(SCROLL)
                        num_of_pagedowns -= 1
                    #time.sleep(1)
                    except:
                        break
                html = browser.page_source
                soup = BeautifulSoup(html,'html.parser')

                #3-1. 전국 식당의 각 점포이름 크롤링
                print("Crawling...")
                name = soup.find_all("div",{"class":"qBF1Pd gm2-subtitle-alt-1"})
                for n in name:
                    name_list.append(n.text)


                #3-2. 전국 식당의 각 상세페이지 url 크롤링
                url = soup.find_all("a",{"class":"a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd"})
                for u in url:
                    url_list.append(u.get("href"))
                print("# of name_list :", len(name_list))
                #print("name_list :",name_list)
                #print("url_list :",url_list)

                #다음 페이지 클릭
                print("Next Page...")
                btn_xpath('//*[@id="ppdPk-Ej1Yeb-LgbsSe-tJiF1e"]/img')

                #cnt += 1
            except :
                print("Crawling of Shop is Done")

                break


    print("Completely Crawled : Name & URL")
    print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")


    #--------------------------------------------


    #4. 정제 및 중복제거 - 해당 식당이 아닌 검색 결과들 정제 (eg.새마을닭발)

    num = []
    for idx in range(len(name_list)):
        if name_list[idx].find(keyword) >= 0:
            num.append(idx)

    filtered_shop = {}
    for x in num:
        filtered_shop[name_list[x]]=url_list[x]

    shop_name = list(filtered_shop.keys())
    shop_url = list(filtered_shop.values())

    print("number of shops : ",len(shop_name))
    print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
    #time.sleep(1)

    #-------------------------------------------------


    #5. Crawling - 방문자 리뷰
    review_list = []

    for i in range(len(shop_name)):
        url = shop_url[i]
        browser.get(url)
        time.sleep(LOADING)
        html = browser.page_source
        soup = BeautifulSoup(html,'html.parser')

        #리뷰 더보기 클릭

        if soup.find("span", {"class" : "BgrMEd BgrMEd-text"}) != None: #리뷰가 없어 리뷰 더보기 버튼이 없는 페이지 제외하기 위함

            try:
                review_more = browser.find_element_by_xpath('/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/span[1]/span/span[1]/span[2]/span[1]')
                if review_more.text.find('리뷰') >= 0:
                    #print("div is",j)
                    review_more.click()
                    time.sleep(LOADING)


            except:
                None


            #스크롤 다운

            html = browser.page_source
            soup = BeautifulSoup(html,'html.parser')

            try:
                review_num_txt = soup.find("div", {"class" : "gm2-caption"}).text
                review_num = int(re.sub(r'[^0-9]', '', review_num_txt))
                #print(review_num_txt)
                #print("review_num :",review_num)
                num_of_pagedowns = int(review_num/9)
            except:
                num_of_pagedowns = 20
                print("No Information of review_num")
            print("num of pagedowns :",num_of_pagedowns)

            #scroll
            while (num_of_pagedowns >0): 
                scroll = browser.find_element_by_xpath('/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]')
                browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scroll)

                time.sleep(SCROLL)
                num_of_pagedowns -= 1
            #time.sleep(5)


            html = browser.page_source
            soup = BeautifulSoup(html,'html.parser')

            #리뷰 크롤링
            review_num = 0
            review = soup.find_all("div",{"class":"ODSEW-ShBeI-content"})
            for j in review :
                user = j.find("div",{"class":"ODSEW-ShBeI-title"}) #유저 닉네임
                score = j.find("span",{"class":"ODSEW-ShBeI-H1e3jb"}) #별점
                content = j.find("span",{"class":"ODSEW-ShBeI-text"}) #리뷰 내용
                days = j.find('span', {"class" : "ODSEW-ShBeI-RgZmSc-date"})
                users = user.text
                days = days.text
                scores = score.get("aria-label")
                contents = content.text
                review_list.append([shop_name[i],users,days, scores, contents])
                review_num += 1   
            #print(review_num)
            #print("review_list :", review_list)

        else : #적거나 없는 리뷰

            #리뷰 크롤링
            review_num = 0
            review = soup.find_all("div",{"class":"ODSEW-ShBeI-content"})

            #적은 리뷰
            if review != []:
                for j in review :
                    user = j.find("div",{"class":"ODSEW-ShBeI-title"}) #유저 닉네임
                    score = j.find("span",{"class":"ODSEW-ShBeI-H1e3jb"}) #별점
                    content = j.find("span",{"class":"ODSEW-ShBeI-text"}) #리뷰 내용
                    days = j.find('span', {"class" : "ODSEW-ShBeI-RgZmSc-date"})
                    users = user.text
                    days = days.text
                    scores = score.get("aria-label")
                    contents = content.text
                    review_list.append([shop_name[i],users,days, scores, contents])
                    review_num += 1  

            #없는 리뷰
            else:
                print("No review")
                user = "No review"
                score = "No review"
                content = "No review"
                days = 'No review'
                review_list.append([shop_name[i],user, days,score, content])

        print("review_num :",review_num)
        print(i+1, " / ", len(shop_name))
    print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")



    #-------------------------------------------------


    #6. DataFrame - 각 행과 열에 맞게 데이터 구조화
    times = str(dt.datetime.now())[:str(dt.datetime.now()).index('.')]
    times= re.sub(' ', '_', times)
    times = re.sub(':', '_', times)
    review_list_np = np.array(review_list).reshape(-1, 5)
    review_visitor = pd.DataFrame(review_list_np, columns=["shop_name", "user", "time","score", "content"])
    review_visitor.to_excel("googlemap_" + keyword + "_Review_" + times + ".xlsx", index=False)

    print("Completely Crawled : Review of ", keyword)
#time.sleep(3)   




