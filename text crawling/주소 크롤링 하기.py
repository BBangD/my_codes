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

# Idea = 기존 리뷰 데이터셋 병합된 파일에서 set으로 shop_name 불러오고, 그를 검색해서 주소를 크롤링하는 방식.

# +
#네이버맵버전
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

df = pd.read_excel('카페 맵 리뷰 데이터/네이버맵리뷰통합.xlsx')
shop_name = list(set(df['shop_name']))
address_dict = {'shop_name' : [], 'address' : []}

path="chromedriver.exe"
browser = webdriver.Chrome(path)

for shop in shop_name:
    url = 'https://m.map.naver.com/search2/search.naver?query='+shop
    browser.get(url)
    browser.implicitly_wait(2)
    try:    
        address =browser.find_element_by_xpath('/html/body/div[4]/div[2]/ul/li/div[1]/div[1]/div/a').text[5:]
    except:
        continue
    address_dict['address'].append(address)
    address_dict['shop_name'].append(shop)
pd.DataFrame(address_dict).to_excel('네이버맵 주소.xlsx')

# +
#구글맵버전

import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

#google_df = pd.read_excel('카페 맵 리뷰 데이터/구글맵리뷰통합.xlsx')
google_shop_name = list(set(google_df['shop_name']))
google_address_dict = {'shop_name' : [], 'address' : []}
path="chromedriver.exe"
browser = webdriver.Chrome(path)



for shop in google_shop_name[6218:]:
    url = "https://www.google.com/maps/search/" + shop
    browser.get(url)
    browser.implicitly_wait(2)
    html = browser.page_source
    soup = BeautifulSoup(html,'html.parser')
    shop_url = soup.find("a",{"class":"a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd"})
    try:
        browser.get(shop_url.get('href'))
        browser.implicitly_wait(2)
        html = browser.page_source
        soup = BeautifulSoup(html,'html.parser')
        address = soup.find('div',{'class' :'QSFF4-text gm2-body-2' }).text
        shop_name = soup.find('h1',{'class' :'x3AX1-LfntMc-header-title-title gm2-headline-5' }).text
       

    except:
        browser.implicitly_wait(2)
       
        #shop_name = browser.find_element_by_xpath('/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1/span[1]').text
        #address = browser.find_element_by_xpath('/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[9]/div[1]/button/div[1]/div[2]/div[1]').text
        html = browser.page_source
        soup = BeautifulSoup(html,'html.parser')
        address = soup.find('div',{'class' :'QSFF4-text gm2-body-2' }).text
        shop_name = soup.find('h1',{'class' :'x3AX1-LfntMc-header-title-title gm2-headline-5' }).text
    print(shop_name, address)
    google_address_dict['shop_name'].append(shop_name)
    google_address_dict['address'].append(address)
# -

pd.DataFrame(google_address_dict).to_excel('구글맵 주소 {}.xlsx'.format(google_shop_name.index(shop))) #중간에 끊길 경우, 그 때 부터 다시하기(아마 로딩 오류인 듯 - 귀찮아서 수정 안함)
print(google_shop_name.index(shop))
print(len(google_shop_name))
