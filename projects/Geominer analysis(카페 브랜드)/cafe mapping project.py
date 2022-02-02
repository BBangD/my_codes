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

# 브랜드 지역 주소(위도,경도)를 포함한 리뷰 데이터를 받아 지도에 볼륨을 색으로, 리뷰 워드클라우드를 팝업으로 보여주는 코드입니다.
# 1. 

import folium
import numpy as np
import json
import requests
import pandas as pd
import branca
import geojson
import base64

pip install base64


# +
#geojson file load
path_to_file = 'HangJeongDong_ver20210701.geojson'
with open(path_to_file, 'r',encoding='utf-8') as f:
    json_data = geojson.load(f)
    

m = folium.Map(location=[37.56642229866859, 126.97797397798712])
#서울을 기반으로 맵을 만들어서 folium 모듈이 잘 임포트 되었는지 테스트 해봅니다


m

# +
#colormap 정의 - 지금은 필요 없음
# from branca.colormap import linear
# freq = pd.read_csv('폴바셋 빈도.csv')
# colormap = linear.Blues_09.scale(
#     freq['freq'].min(),
#     freq['freq'].max()
# )

# +
#지역별 빈도 dict 만들기
#먼저 column이 shopname, freq, 시군구로 정의된 file 생성해야함 - 이건 나중에 맵 크롤링에 주소 추가해서 시군구로 끝나는
#text 가져오는 것으로 자동화 코딩 예정
#해당 파일은 column이 shop,freq,지역으로 구성됨
df = pd.read_csv('폴바셋 지역별 빈도.csv')
areafreq = {}

# df.iloc[0,2] = 지역, 1이 빈도
for k in range(len(df)):
    area = df.iloc[k,2]
    freq = df.iloc[k,1]
    if df.iloc[k,2] in areafreq.keys():
        areafreq[area] += freq
    else:
        areafreq[area] = freq

for k in range(len(json_data['features'])):
    areaname = json_data['features'][k]['properties']['sggnm']
    if areaname not in areafreq.keys():
        areafreq[areaname] = 1 #map에 전체적인 색을 주기 위해 아무것도 없는 곳도 1로 설정 - 0이면 folium에서 검은 색으로 표시되기 때문인데,
        #나중에 수정할 예정입니다.
#지역명(시군구) : 빈도 로 구성된 데이터프레임을 생성합니다
freqformap = pd.DataFrame({'area' : areafreq.keys(),'freq' : areafreq.values()})


# +
#지도 volume으로 색칠하기
#지역별 빈도를 생성한 파일로 컬러를 지정하고 색칠한 후 레이어를 지도 위에 덮어씌웁니다.
m = folium.Map([37.56642229866859, 126.97797397798712], zoom_start=12)
folium.Choropleth(
    geo_data = json_data,
    data = freqformap,
    columns = ['area','freq'],
    key_on = 'feature.properties.sggnm',
    fill_color='YlOrBr',
    fill_opacity = 0.6,
    line_opacity=0.2,
    legend_name = 'Paul Basset Volume',
    
).add_to(m)
folium.LayerControl().add_to(m)
m
# -

cafedict = pd.read_excel('googlemap_폴바셋_Review_2021-12-01_02_33_09.xlsx')

# +
#wordcloud 만들기
# 팝업에 사용할 워드클라우드를 만드는 코드입니다. 
from konlpy.tag import Okt
from collections import Counter
import csv
import pandas as pd
import itertools
from collections import Counter
from wordcloud import WordCloud
wc = WordCloud(font_path ='C:/Windows/Fonts/a고딕14.ttf', 
              background_color = "white", \
              width = 300,
              height = 300, \
              max_words = 30, \
              max_font_size = 30)
path = pd.read_csv('정재학교수의 경영불용어사전.csv', encoding= 'cp949')
# 불용어 사전 데이터 열 불러오기
stopwords = path.loc[:,'word']
stoplist = list(stopwords)
okt = Okt()
#----------------------------------------------------------


#cafedict는 상점명, 리뷰(content)를 포함하는 리뷰 크롤링 엑셀 파일입니다
for shop in set(cafedict['shop_name']):
    condition = (cafedict.shop_name == shop)
    content = cafedict[condition]['content']
    content = content.str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
    data = content.values
    datalist = list(data)
    wordlist=[]
    for a in datalist:
        if str(a) != 'nan':
            
            word = okt.morphs(a)
            wordlist.append(word)
    allwords = list(itertools.chain.from_iterable(wordlist))
    
    clean_words = []
    i=0
    for j in allwords:
    
        if j not in stoplist:
            clean_words.append(j)
        i+=1
        if i % 100000 == 0:
            leftnum = len(allwords)-i
            print('{}개 남음'.format(leftnum))
    
    counts = Counter(clean_words)
    sumlist = counts.most_common(1000)
    try:
        wc.generate_from_frequencies(dict(sumlist))
        wc.to_file('%s wordcloud.png'%shop)
    except:
        continue
    print('%s 완료'%shop)
    #상점별로 전체 워드클라우드를 생성합니다..
    

# +
# marker 찍기, popup은 워드클라우드, tooltip은 지점명으로 하기
cafedict = pd.read_excel('googlemap_폴바셋_Review_2021-12-01_02_33_09.xlsx')
coor = pd.read_excel('폴바셋 위도경도.xlsx')





import base64
for shop in set(cafedict['shop_name']):
     

    try:
        pic = base64.b64encode(open('%s wordcloud.png'%shop[1:] ,'rb').read()).decode()
    except:
        continue # cafedict에서 리뷰가 없는(워드클라우드가 없는) 매장들에서 오류가 나기 때문에 예외처리 하였습니다
    image_tag = '<img src="data:image/jpeg;base64,{}">'.format(pic) #이미지를 base64 형식의 텍스트로 변환해 팝업에 띄울 수 있게 합니다
    iframe = folium.IFrame(image_tag, width=300, height=300)
    popup = folium.Popup(iframe, max_width=650)
    index = coor[coor['장소명']==shop].index.tolist()
    position = coor['위경도'][index[0]].split(',')
    folium.Marker(position,
                  popup=popup,
                  tooltip=shop).add_to(m)

m


# +

for k in coor['위경도']:
    folium.Marker(k.split(','),  tooltip=shop).add_to(m)
# -

pic = base64.b64encode(open('%s wordcloud.png'%shop ,'rb').read()).decode()

index = coor[coor['장소명']==shop].index.tolist()

m.save('Geometric 폴바셋 연습.html')
