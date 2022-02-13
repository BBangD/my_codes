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
#주소 전처리
#주소에 빌딩 이름, 층수와 같은 쓸모 없는 문자열들이 포함되어 있으면 geocoding이 불가능하기에 그러한 데이터들을 지워주는 것
# 동, 로, 길 뒤에 숫자나 번지가 적혀 있으면 그 외 문자 token들은 전부 지우는 알고리즘 사용. 
# 구글 맵의 경우 KR, 번지와 같은 주소 불용어 / 영어 주소 / 주소 거꾸로 기재 등 주소 처리에 다양한 애로사항이 존재하여
# 무식 ver도 같이 사용해야 함
import pandas as pd

def Clean_address(address):
    
    if type(address) == float: 
        #주소가 crawling 되지 않고 Nan으로 남겨진 데이터들을 처리하는 것. 리뷰 크롤링 시 주소를 크롤링 했다면 상관 없을 것
        #해당 처리를 하는 이유는 주소를 리뷰와 같이 크롤링 하지 않고 추후에 보충했기 때문임
        token = 'No address'
    else:
        address = address.replace('번지','')
        token = address.split()

        if 'KR' in token:
            token.remove('KR')
        for n in range(len(token)):
            if token[n].endswith(('로','길','동')) == True:
                try:
                    int(token[n+1])
                    token = token[:n+2]
                    break
                except :
                    if n == len(token)-1:
                        break
                    if '-' in token[n+1]:
                        token = token[:n+2]
                        break
        token = ' '.join(token)
        print(token)
    return token



# +
navermap_df = pd.read_excel('카페 맵 리뷰 데이터/ 리뷰 결측제거.xlsx')
navermap_df['주소'] = navermap_df['주소'].apply(Clean_address)

navermap_df.to_excel('네이버맵 리뷰 결측제거 주소.xlsx')

# +

from tqdm.notebook import tqdm
tqdm.pandas()
# googlemap_df = pd.read_excel('카페 맵 리뷰 데이터/구글맵 리뷰 결측제거.xlsx)
googlemap_df['주소'] = googlemap_df['주소'].progress_apply(Clean_address)

googlemap_df.to_excel('구글맵 리뷰 결측제거 주소.xlsx')
# -

from geopy.geocoders import Nominatim
import pandas as pd
from tqdm.notebook import tqdm
#geopy를 통하여 위경도를 변환하는 함수입니다.
geolocoder = Nominatim(user_agent = 'South Korea')
def geocoding(address):
    geo = geolocoder.geocode(address)
    crd = [geo.latitude, geo.longitude]
#     print(crd)
    return crd


# +
df = pd.read_excel('구글맵 리뷰 결측제거 주소.xlsx')

tqdm.pandas()
address_list = list(set(df['주소']))

# crd_list = list(map(lambda x: geocoding(x),address_list)) -> 주소없는경우 해결어려움
address_dict = {'address' : [], 'crd' : []}
for address in tqdm(address_list):
    try:
        address_dict['crd'].append(geocoding(address))
        address_dict['address'].append((address))
    except:
        address_dict['crd'].append('failed')
        address_dict['address'].append(address)





# +
#원래 df에 좌표를 다시 할당해주는 함수입니다.
# 주소가 crd로 변환되지 않은 경우 crd 열에 'failed'를 기입합니다.
def Locate_crd(address):
    
    crdindex = address_dict['address'].index(address)
    crd = address_dict['crd'][crdindex]
    return crd

df['crd'] = df['주소'].progress_apply(Locate_crd)
    
# -

df.to_excel('구글맵 좌표입력.xlsx')

# !jt -t gruvboxd -f D2Coding -fs 12 -tf roboto -tfs 13 -nf opensans -nfs 12 -ofs 12 -dfs 12 -cellw 95% -lineh 150 -T -N
