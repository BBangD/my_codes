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

from selenium import webdriver
#from selenium.webdriver.common.keys import keys
from bs4 import BeautifulSoup
import time
import datetime as dt
import pandas as pd
import re
import numpy as np
from selenium.webdriver.common.action_chains import ActionChains

driverpath = 'chromedriver.exe'
driver = webdriver.Chrome(driverpath)

# +
'''알고리즘 설명
해당 코드는 geopy로 좌표 획득이 불가능한 매장들에 한해 무식한 방법으로 위도, 경도를 알아내는 코드입니다.
시간이 많이 걸리니 많은 양의 데이터를 처리하지 않으시길 권장합니다

알고리즘은 간단합니다.
구글 맵에서는 어떤 장소를 검색하든 그 장소가 화면 상 항상 동일한 위치에 나타나게 되어 있습니다.
해당 장소를 selenium을 통해 우클릭하여 직접 위도,경도를 알아내는 방식입니다.
다만 어떤 장소를 검색햇을 때 바로 그 장소가 뜨는 경우가 있고 장소 목록에서 제일 위를 선택하는 경우가 있는데,
어떤 방식으로 매장 정보로 들어가냐에 따라 화면 상에 뜨는 장소 포인터의 위치가 달라지게 됩니다.
따라서 try를 이용한 예외처리를 통해 검색목록이 나올 경우에는 그렇지 않을 때보다 더 오른 쪽(offset +200만큼)을 클릭하게 하여
느리지만 정확한 좌표값을 찾아냅니다'''
# df = pd.read_excel('구글맵 좌표입력.xlsx',sheet_name = 'fail_sheet')
from tqdm.notebook import tqdm
tqdm.pandas()
url = "https://www.google.com/maps/search/" 
driver.get(url)
driver.maximize_window()
for k in tqdm(range(len(df['crd']))): #dataframe 내에 있는 장소명을 불러옵니다
    
    url = "https://www.google.com/maps/search/" + df['shop_name'][k]
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    try:
        shop_url = soup.find("a",{"class":"a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd"}) #장소 목록(세부url 정보들)이 있는 경우
        driver.get(shop_url.get('href'))
        time.sleep(2)
        actions = ActionChains(driver)
        actions.move_to_element_with_offset(driver.find_element_by_tag_name('body'), 0,0)
        actions.move_by_offset(200, 0).context_click().perform() # offset 200만큼 이동하기
        driver.implicitly_wait(1.5)
        coor = driver.find_element_by_css_selector('#action-menu > ul > li:nth-child(1) > div.nbpPqf-menu-x3Eknd-text-haAclf > div.nbpPqf-menu-x3Eknd-text').text
        df['crd'][k]=[coor]
    except:
        driver.implicitly_wait(2)
        actions = ActionChains(driver)
        actions.move_to_element_with_offset(driver.find_element_by_tag_name('body'), 0,0)
        actions.move_by_offset(0, 0).context_click().perform()
        driver.implicitly_wait(1.5)
        coor = driver.find_element_by_css_selector('#action-menu > ul > li:nth-child(1) > div.nbpPqf-menu-x3Eknd-text-haAclf > div.nbpPqf-menu-x3Eknd-text').text
        df['crd'][k]=[coor]
    print(coor)
    
#df.to_excel('좌표안긁힌거 구글맵.xlsx')

# +
#
