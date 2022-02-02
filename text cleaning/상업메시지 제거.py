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
import pandas as pd


deletewords=[]
with open('전기차 스팸.txt','r',encoding = 'utf-8') as dwords:
    dwords = dwords.read()
    dwords = dwords.split()
    
for x in dwords:
    deletewords.append(x)

analist = ['전기차 블로그 카페 중복제거 오름차순정렬']

for x in analist: 
    df=pd.read_csv('%s.csv'%x, encoding='utf-8')


    df=df.dropna().reset_index(drop=True)


    a = df.loc[:,'title']
    v= a.values
    c= list(v)


    b = df.loc[:,'text']
    p = b.values
    d = list(p)
    
    try:
        m = df.loc[:,'cafe']
        n = m.values
        o = list(n)
        for g in range(len(o)):
            if any(word in o[g] for word in deletewords):
                deleteindex.append(g)
    except:
        pass
    
    deleteindex=[]
    for k in range(len(c)):
        if any([word in c[k] for word in deletewords]):
            deleteindex.append(k)
            
    for j in range(len(d)):
        if any(word in d[j] for word in deletewords):
            deleteindex.append(j)
            
    
   
            



    nodup_index = list(set(deleteindex))
    nodup_index.sort()
    i=0
    total = len(nodup_index)
    print('%s 개 스팸 데이터 확인'%total)

    for a in nodup_index:
        leftwork = total - i   
        df = df.drop(a)
        i+=1
        if leftwork % 1000 ==0:
            print("{}개 남음".format(leftwork))
    try:
        df = df.drop('cafe',axis='columns')
    except:
        pass

    
    df.sort_values(by = 'date', axis = 0)
    df.to_csv('%s 스팸제거.csv'%x)
    print('%s 스팸제거 완료'%x)

