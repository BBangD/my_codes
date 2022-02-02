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
def Linear_Regression(username,prname):
    import os, re
    from tqdm import tqdm
    from utils import Read_Arg_, Read_Sheet_, import_dataframe, export_dataframe
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd 
    from sklearn.linear_model import LinearRegression
    import math
    from statsmodels.formula.api import ols
    
    plt.rcParams['figure.figsize'] = (10.0, 8.0) # set default size of plots
    plt.rcParams['image.interpolation'] = 'nearest'
    plt.rcParams['image.cmap'] = 'gray'

    
    try:
        input_directory = "/".join([username, prname])  #/username/prname으로 변함
    except:
        input_directory = None
    tqdm.pandas()

    ref, input_, output_ = Read_Arg_(username,prname,"Linear_Regression")

    input_name = os.path.join(input_directory, input_)  
    input_data = import_dataframe(input_name) #input file/information 열에 있는 것들을 dataframe으로 변환하여 가져오는 함수
    variable = list(input_data.columns)
    Y = input_data[variable[0]] # 첫 열을 종속변수로 할당
    X = input_data[variable[1:]] #다음 열 부터는 독립변수로 할당

    IV = input_data.columns[1]
    for k in input_data.columns[2:]: #독립변수명들을 IV라는 리스트에 저장
        IV = IV+ '+'+k

    res = ols('{} ~ {}'.format(input_data.columns[0],IV), data=input_data).fit() #전체 정보를 보기 위해 정보 출력
    print(res.summary())
    lm = LinearRegression()
    multiplelm = lm.fit(X,Y) #텍스트파일 만들기 위해서 다중회귀분석 모델 생성(ols에는 베타값, 절편값 없음)

    for x in variable[1:]:                #각 독립변수별 산포도, 예측선 이미지 생성
        X = input_data[[x]]
        lm.fit(X,Y)
        plt.title('{}~{}'.format(variable[0],x))
        plt.xlabel(x)
        plt.ylabel(variable[0])
        plt.scatter(X,Y, label = 'real data')
        predict = lm.predict(X)
        plt.plot(X,predict, label='predicted linear model', color = 'red')
        plt.legend()

        plt.savefig('out_{}_{}.png'.format(variable[0],x))
        plt.clf()

    #text file 만들기
    f = open(r'linear regression summary text.txt', 'w')

    modelname = str(res.model).partition('linear_model.')[2].split(' ')[0]
    model = '사용된 모델명은 '+str(modelname)+' 입니다. \n'
    f.write(str(model))
    f.write('변수의 개수는 {} 개 이며, observation의 수는 {} 개 입니다. \n' .format(len(input_data),len(variable)-1))
    f.write('조정된 R-squared 지수는 {}이고, BIC 값은 {}입니다.\n'. format(res.rsquared_adj,res.bic))
    for j in range(len(res.pvalues)):
        if j==0:
            pass
        else:
            line = str(res.pvalues.axes[0][j])+' 의 p값 : '+ str(res.pvalues[j])+'\n'
            f.write(str(line))
    f.write('\n\n')
    f.write('-----------------------------------------------------------\n')
    f.write('-----------------------------------------------------------')
    f.write('\n\n')
    Y = input_data[variable[0]]
    X = input_data[variable[1:]]
    multiplelm = lm.fit(X,Y)
    f.write('절편값은 {}입니다. \n'.format(multiplelm.intercept_))
    for k in range(len(multiplelm.coef_)):
        beta = str(list(X.columns)[k])+'의 베타값은 '+str(multiplelm.coef_[k])+'입니다.\n'
        f.write(beta)

    f.write('\n\n')
    f.write('-----------------------------------------------------------\n')
    f.write('-----------------------------------------------------------')
    f.write('\n\n')

    f.close()

#첫섹션에는 어떤 모델로 돌렸는가하는 정보. observation 수, 변수 개수, 방식(OLS)
#조정된 R^2, BIC지수(변수가 많아짐에따라 올라가는 설명력을 보정하는 지수 - 변수의 수에 따라 penalty 증가)
#두번째에는 coef,intercept, p값만 
#세 번째에는 해석한 내용



# +
#local
import os, re
from utils import Read_Arg_, Read_Sheet_, import_dataframe, export_dataframe
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
from sklearn.linear_model import LinearRegression
import math
from statsmodels.formula.api import ols

plt.rcParams['figure.figsize'] = (10.0, 8.0) # set default size of plots
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

    
try:
    input_directory = "/".join([username, prname])  #/username/prname으로 변함
except:
    input_directory = None


# ref, input_, output_ = Read_Arg_(username,prname,"Linear_Regression")

#     input_name = os.path.join(input_directory, input_)  -web기반
#     input_data = import_dataframe(input_name) #input file/information 열에 있는 것들을 dataframe으로 변환하여 가져오는 함수
input_data = import_dataframe('보스턴 데이터.xlsx')
variable = list(input_data.columns)
Y = input_data[variable[0]]
X = input_data[variable[1:]]

IV = input_data.columns[1]
for k in input_data.columns[2:]:
    IV = IV+ '+'+k

res = ols('{} ~ {}'.format(input_data.columns[0],IV), data=input_data).fit()
print(res.summary())
lm = LinearRegression()
multiplelm = lm.fit(X,Y)

for x in variable[1:]:
    X = input_data[[x]]
    lm.fit(X,Y)
    plt.title('{}~{}'.format(variable[0],x))
    plt.xlabel(x)
    plt.ylabel(variable[0])
    plt.scatter(X,Y, label = 'real data')
    predict = lm.predict(X)
    plt.plot(X,predict, label='predicted linear model', color = 'red')
    plt.legend()
    
    plt.savefig('out_{}_{}.png'.format(variable[0],x))
    plt.clf()

#text file 만들기
f = open(r'C:\\Users\\qkd78\\Desktop\\방성현\\대학원 프로젝트\\교육\\linearregression\\linear regression summary text.txt', 'w')

modelname = str(res.model).partition('linear_model.')[2].split(' ')[0]
model = '사용된 모델명은 '+str(modelname)+' 입니다. \n'
f.write(str(model))
f.write('변수의 개수는 {} 개 이며, observation의 수는 {} 개 입니다. \n' .format(len(input_data),len(variable)-1))
f.write('조정된 R-squared 지수는 {}이고, BIC 값은 {}입니다.\n'. format(res.rsquared_adj,res.bic))
for j in range(len(res.pvalues)):
    if j==0:
        pass
    else:
        line = str(res.pvalues.axes[0][j])+' 의 p값 : '+ str(res.pvalues[j])+'\n'
        f.write(str(line))
f.write('\n\n')
f.write('-----------------------------------------------------------\n')
f.write('-----------------------------------------------------------')
f.write('\n\n')
Y = input_data[variable[0]]
X = input_data[variable[1:]]
multiplelm = lm.fit(X,Y)
f.write('절편값은 {}입니다. \n'.format(multiplelm.intercept_))
for k in range(len(multiplelm.coef_)):
    beta = str(list(X.columns)[k])+'의 베타값은 '+str(multiplelm.coef_[k])+'입니다.\n'
    f.write(beta)

f.write('\n\n')
f.write('-----------------------------------------------------------\n')
f.write('-----------------------------------------------------------')
f.write('\n\n')

f.close()

#첫섹션에는 어떤 모델로 돌렸는가하는 정보. observation 수, 변수 개수, 방식(OLS)
#조정된 R^2, BIC지수(변수가 많아짐에따라 올라가는 설명력을 보정하는 지수 - 변수의 수에 따라 penalty 증가)
#두번째에는 coef,intercept, p값만 
#세 번째에는 해석한 내용
# -

#text writing test
f = open(r'C:\\Users\\qkd78\\Desktop\\방성현\\대학원 프로젝트\\교육\\linearregression\\linear regression summary text.txt', 'w')
for j in range(len(res.pvalues)):
    if j==0:
        line = '절편값 : '+ str(res.pvalues[j])+'\n'
        f.write(str(line))
    else:
        line = str(res.pvalues.axes[0][j])+' 의 베타값 : '+ str(res.pvalues[j])+'\n'
        f.write(str(line))
modelname = str(res.model).partition('linear_model.')[2].split(' ')[0]
model = '사용된 모델명은 '+str(modelname)+' 입니다. \n'
f.write(str(model))
f.write('변수의 개수는 {} 개 이며, observation의 수는 {} 개 입니다. \n' .format(len(input_data),len(variable)-1))
f.write('조정된 R-squared 지수는 {}이고, BIC 값은 {}입니다.\n'. format(res.rsquared_adj,res.bic))
Y = input_data[variable[0]]
X = input_data[variable[1:]]
multiplelm = lm.fit(X,Y)
f.write('절편값은 {}입니다. \n'.format(multiplelm.intercept_))
for k in range(len(multiplelm.coef_)):
    beta = str(list(X.columns)[k])+'의 베타값은 '+str(multiplelm.coef_[k])+'입니다.\n'
    f.write(beta)
f.close()
