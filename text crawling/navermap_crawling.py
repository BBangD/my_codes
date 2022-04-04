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
'''
원래코드
밑은 지도 수정중
'''
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import datetime as dt 
import pandas as pd 
import re
import numpy as np

LOADING = 2.5
BTN = 0.2
SCROLL = 0.3

geolist=['서울특별시 종로구', '서울특별시 용산구', '서울특별시 성동구', '서울특별시 광진구', '서울특별시 중랑구', '서울특별시 강북구', '서울특별시 노원구', '서울특별시 서대문구', '서울특별시 마포구', '서울특별시 양천구', '서울특별시 강서구', '서울특별시 구로구', '서울특별시 영등포구', '서울특별시 관악구', '서울특별시 서초구', '서울특별시 강남구', '서울특별시 송파구', '서울특별시 강동구', '부산광역시 중구', '부산광역시 서구', '부산광역시 동구', '부산광역시 영도구', '부산광역시', '대구광역시 ', '인천광역시 중구', '인천광역시 연수구', '인천광역시 부평구', '인천광역시 계양구', '광주광역시', '대전광역시', '울산광역시', '세종시', '수원시', '성남시', '안양시', '광명시', '평택시', '동두천시', '안산시', '고양시', '과천시', '남양주시', '시흥시', '의왕시', '하남시', '용인시', '파주시', '이천시', '안성시', '김포시', '양주시', '포천시', '여주시', '강원도', '충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도', '제주시',
 '창원']


path="chromedriver.exe"
browser = webdriver.Chrome(path)
keyword = ['블루보틀'] #키워드 리스트


    #--------------------------------------------


    #1. 활용할 함수 정의

    #xpath(a)의 버튼을 누르는 함수
def btn_xpath(a) :
    button = browser.find_element_by_xpath(a)
    button.click()
    time.sleep(BTN)


    #--------------------------------------------

for keyword in keyword:
    name_list = []
    id_list = []
        #2. url_set - 식당명(keyword) 검색 
    for area in geolist:
        url = 'https://m.map.naver.com/search2/search.naver?query=' + area + ' '+ keyword
        browser.get(url)
        browser.implicitly_wait(LOADING)


        #--------------------------------------------


        #3. Crawling - 전국 식당의 각 점포이름 및 점포id

        html = browser.page_source
        soup = BeautifulSoup(html,'html.parser')

        #3-1. 점포이름
        try:
            name = soup.find_all("div",{"class":"item_tit _title"})
        except:
            continue

        for n in name:
            name_list.append(n.text)

        #3-2. 점포id
        try:
            info = soup.find("ul",{"class":"search_list _items"}).find_all("li",{"class":"_item _lazyImgContainer"})
        except:
            continue

        for i in info:
            id_list.append(i.get("data-sid"))

        print("Completely Crawled : Name & id")
        print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")


        #--------------------------------------------


        #4. 정제 - 해당 식당이 아닌 검색 결과들 정제 (eg.새마을닭발)
    num = []
    for name in range(len(name_list)):
        if name_list[name].find(keyword) >= 0:
            num.append(name)

    filtered_shop = {}
    for x in num:
        filtered_shop[name_list[x]]=id_list[x]

    shop_name = list(filtered_shop.keys())
    shop_id = list(filtered_shop.values())

    print("number of shops : ",len(shop_name))
    print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")


    #-------------------------------------------------
    #5. Crawling - 방문자 리뷰


    print("Visitor Crawling...")        

    review_visitor_list = []

    #5-1. url_set - 점포id 이용하여 각 점포의 방문자 리뷰 페이지 접속
    for id in range(len(shop_id)):
        url = "https://m.place.naver.com/restaurant/" + shop_id[id] + "/review/visitor?type=list"
        browser.get(url)
        time.sleep(LOADING)

        #5-2. 스크롤다운, 더보기 버튼 클릭
        cnt = 0
        noloop=0
        while True:
            try:
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(SCROLL)
                #print("scroll")
                browser.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/div[5]/div[4]/div[3]/div[2]/a').click()
                #스크롤 되지 않을 경우 더보기 button tag의 xpath 값 수정하여 입력
            
                time.sleep(BTN)
                cnt += 1
                if cnt >= 200:
                    print("더보기 에러, refresh")

                    cnt = 0
                    browser.close()
                    browser = webdriver.Chrome(path)
                    browser.get(url) 
                    noloop+=1
                if noloop >=5:
                    break
                 
            except:
                break
        #time.sleep(3)

        #5-3. Crawling - 방문자 리뷰의 유저명, 별점, 리뷰내용 크롤링
        html = browser.page_source
        soup = BeautifulSoup(html,'html.parser')
        review = soup.find("ul",{"class":"_1jVSG"})
        #print(review)
        #print(len(review))

        review_num = 0 
        if review != None:
            for rv in review:
                try:
                    user = rv.find("div",{"class":"_16RxQ"}) #유저 닉네임
                    content = rv.find("span",{"class":"WoYOw"}) #리뷰 내용
                    visitday = rv.find('time').text#작성시간
                   
                    star = rv.find('span',{'class':'_1fvo3 Sv1wj'})
                    user = user.text
                    
                    #5-4. 정제 - 방문자 리뷰의 내용이 없고 사진만 있는 경우 결측치 "No Contents"로 채우기
                    if content != None:
                        content = content.text
                    else:
                        content = "No Contents"
                    if star!= None:
                        star = star.text
                    else:
                        star = 'No score'
                    review_visitor_list.append([shop_name[id], user,visitday,star, content])
                    review_num += 1
                except:
                    print("Something Error")

        else:
            user = "No review" 
            content = "No review"
            star = 'no score'
            visitday = 'no date'
            review_visitor_list.append([shop_name[id], user, visitday, star, content])

        print("shop :", shop_name[id])
        print("review_num :",review_num)

        print(id+1, " / ", len(shop_name)) #진행상황 확인
        print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")


    #5-5. DataFrame - 각 행과 열에 맞게 데이터 구조화
    review_visitor_list_np = np.array(review_visitor_list).reshape(-1, 5)
    review_visitor = pd.DataFrame(review_visitor_list_np, columns = ["shop_name","user",'time','score',"content"])
    times = str(dt.datetime.now())[:str(dt.datetime.now()).index('.')]
    times= re.sub(' ', '_', times)
    times = re.sub(':', '_', times)
    review_visitor.to_csv("navermap_" + keyword + times+"_VisitorReview.csv", index = False)

    print("Completely Crawled : Visitor Review of ", keyword)
    #time.sleep(LOADING)
# else:
#     None
    #-------------------------------------------------

#     #6. Crawling - 블로그 리뷰
#     if Type == 2 or Type == 3:
#         print("Blog Crawling...")

#         review_blog_list = []

#         #6-1. url_set - 점포id 이용하여 각 점포의 블로그 리뷰 페이지 접속
#         for id in range(len(shop_id)):
#             url = "https://m.place.naver.com/restaurant/" + shop_id[id] + "/review/ugc?type=list"
#             browser.get(url)
#             time.sleep(LOADING)

#             #6-2. 스크롤다운, 더보기 버튼 클릭
#             cnt = 0 
#             while True:
#                 try:
#                     browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#                     time.sleep(SCROLL)
#                     #print("scroll")
#                     btn_xpath('/html/body/div[3]/div/div/div[2]/div[5]/div[4]/div[2]/div[2]')                                  
#                     #print("BTN Click")
                    
#                     cnt += 1
#                     if cnt >= 100:
#                         print("더보기 에러, refresh")
#                         cnt = 0
#                         browser.close()
#                         browser = webdriver.Chrome(path)
#                         browser.get(url)  
#                     print(cnt)
#                 except:
#                     #print("???")
#                     break

#             #6-3. Crawling - 방문자 리뷰의 유저명, 별점, 리뷰내용 크롤링
#             html = browser.page_source
#             soup = BeautifulSoup(html,'html.parser')
#             review_blog = soup.find_all("a",{"class":"_2HzSL"})
            
#             review_num = 0
#             for rv in review_blog:
#                 try:
#                     users = rv.find("span",{"class":"_2UOC9"}) #유저 닉네임
#                     title = rv.find("div",{"class":"_38bO0"}) #블로그 제목
#                     contents = rv.find("div",{"class":"_1BWM9"}) #내용 미리보기
#                     users = users.text
#                     title = title.text
#                     contents = contents.text
#                     review_blog_list.append([shop_name[id], users, title, contents])
#                     review_num += 1
#                 except:
#                     print("Something Error")

#             print("shop :",shop_name[id])
#             print("review_num :", review_num)
#             print(id+1, " / ", len(shop_name)) #진행상황 확인
#             print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
            
                
#         #6-4. DataFrame - 각 행과 열에 맞게 데이터 구조화
#         review_blog_list_np = np.array(review_blog_list).reshape(-1, 4)
#         review_visitor = pd.DataFrame(review_blog_list_np, columns = ["shop_name","user","title","contents"])
#         review_visitor.to_csv("navermap_" + keyword + "_BlogReview.csv", index = False)

#         print("Completely Crawling : Blog Review of ", keyword)





# +
#0. setting
'''0404 수정중'''
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import datetime as dt 
import pandas as pd 
import re
import numpy as np

LOADING = 2.5
BTN = 0.2
SCROLL = 0.3

geolist=['서울특별시 종로구', '서울특별시 용산구', '서울특별시 성동구', '서울특별시 광진구', '서울특별시 중랑구', '서울특별시 강북구', '서울특별시 노원구', '서울특별시 서대문구', '서울특별시 마포구', '서울특별시 양천구', '서울특별시 강서구', '서울특별시 구로구', '서울특별시 영등포구', '서울특별시 관악구', '서울특별시 서초구', '서울특별시 강남구', '서울특별시 송파구', '서울특별시 강동구', '부산광역시 중구', '부산광역시 서구', '부산광역시 동구', '부산광역시 영도구', '부산광역시', '대구광역시 ', '인천광역시 중구', '인천광역시 연수구', '인천광역시 부평구', '인천광역시 계양구', '광주광역시', '대전광역시', '울산광역시', '세종시', '수원시', '성남시', '안양시', '광명시', '평택시', '동두천시', '안산시', '고양시', '과천시', '남양주시', '시흥시', '의왕시', '하남시', '용인시', '파주시', '이천시', '안성시', '김포시', '양주시', '포천시', '여주시', '강원도', '충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도', '제주시',
 '창원']


path="chromedriver.exe"
browser = webdriver.Chrome(path)
keyword = ['블루보틀'] #키워드 리스트


    #--------------------------------------------


    #1. 활용할 함수 정의

    #xpath(a)의 버튼을 누르는 함수
def btn_xpath(a) :
    button = browser.find_element_by_xpath(a)
    button.click()
    time.sleep(BTN)


    #--------------------------------------------

for keyword in keyword:
    name_list = []
    id_list = []
    address_list = []
        #2. url_set - 식당명(keyword) 검색 
    for area in geolist:
        url = 'https://m.map.naver.com/search2/search.naver?query=' + area + ' '+ keyword
        browser.get(url)
        browser.implicitly_wait(LOADING)


        #--------------------------------------------


        #3. Crawling - 전국 식당의 각 점포이름 및 점포id

        html = browser.page_source
        soup = BeautifulSoup(html,'html.parser')

        #3-1. 점포이름
        try:
            name = soup.find_all("div",{"class":"item_tit _title"})
        except:
            continue

        for n in name:
            name_list.append(n.find('strong').text)

        #3-2. 점포id
        try:
            info = soup.find("ul",{"class":"search_list _items"}).find_all("li",{"class":"_item _lazyImgContainer"})
        except:
            continue

        for i in info:
            id_list.append(i.get("data-sid"))
        #3-3. 주소
        try:
            address = soup.find_all('a',{'class' : 'item_address _btnAddress'})
        except:
            continue

        for add in address:
            address_list.append(add.text.replace('주소보기','').replace('  ',''))
                
    print("Completely Crawled : Name & id")
    print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
        
    for name in range(len(name_list)):
        if name_list[name].find(keyword) < 0:
            name_list.remove(name_list[name])
            id_list.remove(id_list[name])
            address_list.remove(address_list[name])

    #중복 제거
    
        

    shop_name = name_list
    shop_id = id_list

    shop_df = pd.DataFrame({'shop_name' : shop_name, 'shop_id' : shop_id, 
                          'address' : address_list}).drop_duplicates()
    shop_df.to_excel(keyword+'_url_주소.xlsx')
    
    shop_name = shop_df['shop_name'].tolist()
    shop_id = shop_df['shop_id'].tolist()

    print("number of shops : ",len(shop_df))
    print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
    

    #-------------------------------------------------
    #5. Crawling - 방문자 리뷰


    print("Visitor Crawling...")        

    review_visitor_list = []
    review_count = {'shop_name' : [],'text_review':[],'keyword_review' : []}
    #5-1. url_set - 점포id 이용하여 각 점포의 방문자 리뷰 페이지 접속 및 리뷰 개수 크롤링
    for id in range(len(shop_id[0:1])):
        url = "https://m.place.naver.com/restaurant/" + shop_id[id] + "/review/visitor?type=list"
        browser.get(url)
        time.sleep(LOADING)
        html = browser.page_source
        soup = BeautifulSoup(html,'html.parser')
        reviewnum = soup.find_all('span',{'class':'place_section_count'})
        if len(reviewnum) >=0:

            textreviewnum = int(reviewnum[0].text.replace(',',''))
            try:
                keywordreview = int(reviewnum[1].text.replace(',',''))
            except:
                keywordreview = 'no review'
        elif len(reviewnum) ==0:
            textreviewnum = 'no review'
            keywordreview = 'no review'


        review_count['shop_name'].append(shop_name[id])
        review_count['text_review'].append(textreviewnum)
        review_count['keyword_review'].append(keywordreview)
        
        #5-2. 스크롤다운, 더보기 버튼 클릭
        cnt = 0
        noloop=0
        while True:
            try:
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(SCROLL)
                #print("scroll")
                browser.find_element_by_css_selector(
                    '#app-root > div > div > div.place_detail_wrapper > div:nth-child(5) > div > div.place_section.cXO6M > div._2kAri > a').click()
                #스크롤 되지 않을 경우 더보기 button tag의 xpath 값 수정하여 입력
                
                time.sleep(BTN)
                cnt += 1
                if cnt >= 1000:
                    print("더보기 에러, refresh")

                    cnt = 0
                    browser.close()
                    browser = webdriver.Chrome(path)
                    browser.get(url) 
                    noloop+=1
                if noloop >=5:
                    break                 
            except:
                try:
                    
                    browser.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/div[5]/div/div[3]/div[2]/a').click()
                except:
                    break
        #time.sleep(3)

        #5-3. Crawling - 방문자 리뷰의 유저명, 별점, 리뷰내용 크롤링
        html = browser.page_source
        soup = BeautifulSoup(html,'html.parser')
        review = soup.find("ul",{"class":"_1jVSG"})
        #print(review)
        #print(len(review))

        review_num = 0 
        if review != None:
            for rv in review:
                try:
                    user = rv.find("div",{"class":"_16RxQ"}) #유저 닉네임
                    content = rv.find("span",{"class":"WoYOw"}) #리뷰 내용
                    visitday = rv.find('time').text#작성시간
                    star = rv.find('span',{'class':'_1fvo3 Sv1wj'})
                    user = user.text
                    
                    #5-4. 정제 - 방문자 리뷰의 내용이 없고 사진만 있는 경우 결측치 "No Contents"로 채우기
                    if content != None:
                        content = content.text
                    else:
                        content = "No Contents"
                    if star!= None:
                        star = star.text
                    else:
                        star = 'No score'
                    review_visitor_list.append([shop_name[id], user,visitday,star, content])
                    review_num += 1
                except:
                    print("Something Error")

        else:
            user = "No review" 
            content = "No review"
            star = 'no score'
            visitday = 'no date'
            review_visitor_list.append([shop_name[id], user, visitday, star, content])

        print("shop :", shop_name[id])
        print("review_num :",review_num)

        print(id+1, " / ", len(shop_name)) #진행상황 확인
        print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")


    #5-5. DataFrame - 각 행과 열에 맞게 데이터 구조화
    review_visitor_list_np = np.array(review_visitor_list).reshape(-1, 5)
    review_visitor = pd.DataFrame(review_visitor_list_np, columns = ["shop_name","user",'time','score',"content"])
    times = str(dt.datetime.now())[:str(dt.datetime.now()).index('.')]
    times= re.sub(' ', '_', times)
    times = re.sub(':', '_', times)
    review_visitor.to_csv("navermap_" + keyword + times+"_VisitorReview.csv", index = False)
    pd.DataFrame(review_count).to_excel('navermap_'+keyword+times+'reviewcount.xlsx',index=False)
    print("Completely Crawled : Visitor Review of ", keyword)


# -

name_list
