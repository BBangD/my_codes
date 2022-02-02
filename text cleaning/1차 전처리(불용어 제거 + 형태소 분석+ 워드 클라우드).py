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

# 불용어를 제거하고, 형태소 분석후 빈도 분석 자료와 워드클라우드 파일을 산출하는 코드입니다.
# web에서 작업하기에는 많은 양의 텍스트를 가지고 있는 파일의 불용어 제거를 local 환경에서 
# 편리하게 수행하기 위하여 작성하였습니다.
# 밑의 Delete_Characters(불용어 제거) 함수는  JlabMiner의 불용어 제거 함수를 토대로 만들어졌습니다.
#
# 작성자 : Jlab 연구원 방성현

# +
from konlpy.tag import Okt
from collections import Counter
import csv
import pandas as pd
import itertools
from collections import Counter
from wordcloud import WordCloud

#워드클라우드의 설정을 변경할 수 있습니다. 사용자의 사용 환경에 따라 font의 경로를 설정해주어야 합니다.
#font 경로를 비우고 default 폰트로 설정할 경우, 한글이 깨지는 오류가 발생합니다.
#background_color는 배경의 색을, width/height는 사진 파일의 폭과 높이를 의미합니다.
#max_words는 최대 단어 개수, max_font_size는 최대 폰트 사이즈를 의미합니다.
wc = WordCloud(font_path ='C:/Windows/Fonts/a고딕14.ttf', 
              background_color = "white", \
              width = 1000,
              height = 1000, \
              max_words = 150, \
              max_font_size = 150)
okt = Okt()


# -

#불용어를 제거하는 함수입니다.
#filename에는 처리할 파일의 이름을 넣어 주시면 되고, 파일은 코드와 같은 경로에 존재해야 합니다.
#불용어 사전 또한 코드가 있는 같은 경로에 csv파일 형태로 존재해야 합니다. 
#불용어 사전 파일 이름은 JDic_BizStopwords(경영불용어사전).csv 입니다. 파일 이름이 다르면 읽을 수 없습니다.
#처리할 파일 내의 text 열 제목(첫 열)은 content입니다. 열 이름이 다르면 읽을 수 없습니다.
def Delete_Characters(filename):
    import re,os
    from tqdm import tqdm
    import pandas as pd
    tqdm.pandas()
    path = pd.read_csv('JDic_BizStopwords(경영불용어사전).csv', encoding= 'utf-8')
    # 불용어 사전 데이터 열 불러오기
#     path = path.dropna() # 혹시 모를 결측치를 제거합니다.
    path['unit_length'] = path['word'].apply(lambda x:len(str(x))) #오류를 방지하기 위해 길이 기준 내림차순으로 불용어를 정렬합니다.
    path = path.sort_values(by = 'unit_length', ascending = False)

    stopwords = path.loc[:,'word']

    stoplist = list(stopwords)
    stoplist = str(stoplist).replace("[", "").replace("]", "").replace(", ''", "").replace(", ", "|").replace(
            "'", "")


    def Clean_stopwords(item):  # Clean_stopwords라는 사용자정의함수를 정의합니다.
            item_edited = re.sub(stoplist, " ", item)  # 이는 정규표현식을 통해 item(input_Message의 각행의 데이터)에 대해
            # stoplist에 해당하는 패턴이 나올 시 " "(공백)으로 치환해주는 함수입니다.
            item_edited = re.sub(" +", " ", item_edited)  # 다중공백도 제거해줍니다.
            return item_edited  # 이 함수의 리턴값을 치환된 데이터로 최신화된 데이터로 내보내도록 합니다.
    input_Message = pd.read_csv('{}.csv'.format(filename))
    input_Message = input_Message[input_Message['content'].notna()]
    input_Message['content'] = input_Message['content'].progress_apply(Clean_stopwords)

    output_name = str(filename) +' 불용어 처리.xlsx' # 원래 파일명 + 불용어 처리.xlsx로 엑셀 파일이 같은 경로에 저장됩니다.
    input_Message.to_excel(output_name)


Delete_Characters('구글맵 테스트 데이터셋')


# +
# 형태소 분석 후 빈도, 워드클라우드까지 추출하는 코드입니다.
# 파일은 같은 경로에 있어야 하며 위의 코드로 불용어 제거를 마친 파일을 그대로 넣어 사용합니다.

def morphs_analysis(filename):
    df = pd.read_excel('%s.xlsx'%filename)
    df = df.dropna(axis=0)
    df['content'] = df['content'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
#     contentlist = list(df.loc[:'content'])
    from tqdm.notebook import tqdm_notebook
    tqdm_notebook.pandas()
    def morphs(item):
        item_disassembled = okt.morphs(item) # okt의 형태소 분석기를 사용하여 형태소를 분리합니다.
        return item_disassembled

    df = df.dropna(axis=0) # 혹시 모를 결측치를 제거합니다
#     df['content'] = df['content'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
    df['content'] = df['content'].progress_apply(morphs)
    output_name = str(filename)+ ' 형태소 분리(okt).xlsx' # 형태소 분리 파일을 먼저 엑셀로 내보낸 후에, 빈도 분석 및 워드클라우드 생성을 진행합니다.
    print('saving...wait for few more seconds...')
    df.to_excel(output_name)
    print(output_name + ' 저장됨')
    allwords = list(itertools.chain.from_iterable(df['content']))
    freq = Counter(allwords).most_common()
    wc.generate_from_frequencies(dict(freq))
    
    wc.to_file('%s  wordcloud.png'%filename)
    print('%s 워드클라우드 생성됨'%filename)
    freqdict = pd.DataFrame(dict(freq), index = ['freq'])
    freqdict = freqdict.transpose()	#행 열 전환
    freqdict.to_excel('{} 빈도.xlsx'.format(filename))
    print('%s 빈도.xlsx 생성됨'%filename)


# -

morphs_analysis('구글맵 테스트 데이터셋 불용어 처리')


#콘텐츠가 리스트형식으로 변한 자료의 워드클라우드만 만드는 함수(ex. 위 코드들의 output)
def woc(filename):
    
    df = pd.read_excel('%s.xlsx'%filename)
    df['content']= df['content'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
    aa=[]
    for k in range(len(df['content'])):
        aa.append(df['content'][k].split())
    allwords = list(itertools.chain.from_iterable(aa))
    freq = Counter(allwords).most_common()
    wc.generate_from_frequencies(dict(freq))
    
    wc.to_file('%s  wordcloud.png'%filename)
    print('%s 워드클라우드 생성됨'%filename)
    freqdict = pd.DataFrame(dict(freq), index = ['freq'])
    freqdict = freqdict.transpose()	#행 열 전환
    freqdict.to_excel('{} 빈도.xlsx'.format(filename))
    print('%s 빈도.xlsx 생성됨'%filename)


# +
#test(no-stem)
from tqdm._tqdm_notebook import tqdm_notebook
tqdm_notebook.pandas()
df = pd.read_excel('구글맵 테스트 데이터셋 불용어 처리.xlsx')
def morphs(item):
    item_disassembled = okt.morphs(item)
    return item_disassembled

df = df.dropna(axis=0)
df['content'] = df['content'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
df['content'] = df['content'].progress_apply(morphs)
# output_name = '구글맵 테스트 데이터셋 불용어 처리 형태소 분리(okt).xlsx'
# df.to_excel(output_name)

df['content']
# -

#test(stem)
from tqdm._tqdm_notebook import tqdm_notebook
tqdm_notebook.pandas()
def morphs(item):
    item_disassembled = okt.morphs(item,stem=True)
    return item_disassembled
df = pd.read_excel('구글맵 테스트 데이터셋 불용어 처리.xlsx')
df = df.dropna(axis=0)
df['content'] = df['content'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
df['content'] = df['content'].progress_apply(morphs)
# output_name = '구글맵 테스트 데이터셋 불용어 처리 형태소 분리(okt_stem).xlsx'
# df.to_excel(output_name)


# ?utils

Read_Sheet(None,None,'JDic_BizStopwords(경영불용어사전)')
