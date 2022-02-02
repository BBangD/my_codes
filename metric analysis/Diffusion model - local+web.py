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

#web ver.
def BassModel(username,prname):
    import os, re
    from tqdm import tqdm
    from utils import Read_Arg_, Read_Sheet_, import_dataframe, export_dataframe
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd 
    from sklearn.linear_model import LinearRegression
    import math
    import itertools
    
    try:
        input_directory = "/".join([username, prname])  #/username/prname으로 변함
    except:
        input_directory = None
    tqdm.pandas()

    ref, input_, output_ = Read_Arg_(username,prname,"BassModel")

    input_name = os.path.join(input_directory, input_)  
    input_data = import_dataframe(input_name) #input file/information 열에 있는 것들을 dataframe으로 변환하여 가져오는 함수
    # input data는 period sales 를 담은 것
    # input data에서 cumulative sales, cumulative sales^2 만들고 m,p,q 추출 -> graph plotting

   
    sale = input_data['sales']

    sales = [0]
    for k in sale :
        sales.append(k)


    cumulative_sales = list(itertools.accumulate(sales))
    diff = pd.DataFrame({'sales' : sales[1:], 'cumulative sales' : cumulative_sales[:-1]})
    diff['cumulative sales^2'] = diff['cumulative sales']**2
    lr = LinearRegression()
    Y = diff['sales']
    X = diff[['cumulative sales','cumulative sales^2']]

    lm = lr.fit(X[:ref],Y[:ref])

    # intercept = pm ; b1 = q-p, b2=-q/m


    a = lm.intercept_
    b = lm.coef_[0]
    c = lm.coef_[1]

    # m = (-b + (b**2-4*c*a)**(1/2))/(2*c)
    m = (-b - (b**2-4*c*a)**(1/2))/(2*c)
    p = a/m
    q=-c*m

    predict = lm.predict(X)


    plt.rcParams['figure.figsize'] = (15.0, 8.0) # set default size of plots
    plt.rcParams['image.interpolation'] = 'nearest'
    plt.rcParams['image.cmap'] = 'gray'
    plt.rcParams["font.family"] = 'NanumGothic'
    plt.rcParams["font.size"] = 20
    plt.xlabel('period')
    plt.ylabel('sales')
    plt.axvline(ref, 0, 1, color='lightgray', linestyle='--', linewidth=2, label = 'reference')
    plt.plot(range(1,len(diff)+1),predict, linestyle = 'solid',marker = 'o',color='orange', label = 'predicted')
    plt.plot(range(1,len(diff)+1),Y, linestyle = 'solid',marker = 'o',color='red', label = 'actual')
    plt.legend()
    plt.title('최대시장규모 : {}, 혁신계수 : {}, 모방계수 : {}, 혁신지수 : {} '.format(round(m,3),round(p,3),round(q,3),round(p/q,3)))


    Y_true_is = Y[:ref]
    Y_pred_is = predict[:ref]
    Y_true_os= Y[ref:]
    Y_pred_os = predict[ref:]

    MSE_is = np.square(np.subtract(Y_true_is,Y_pred_is)).mean()
    MSE_os = np.square(np.subtract(Y_true_os,Y_pred_os)).mean()



    # return m,p,q, MSE_is, MSE_os

    df=pd.DataFrame({'최대시장규모(m)' : m,'혁신계수(p)' : p, '모방계수(q)' :q, '혁신지수(p/q)' : p/q, 'reference/total' : '{}/{}'.format(ref,len(Y)), 
                 'in_sample MSE' : MSE_is, 'out_sample MSE' : MSE_os},index = [0])
    plt.savefig('{}_Bassmodel.png'.format(input_[:input_.index('.')]))
    df.to_csv('{}_Bassmodel.csv'.format(input_[:input_.index('.')]))


#web test
def BassModel(username,prname):
    import os, re
    from tqdm import tqdm
    from utils import Read_Arg_, Read_Sheet_, import_dataframe, export_dataframe
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd 
    from sklearn.linear_model import LinearRegression
    import math
    import itertools
    
    try:
        input_directory = "/".join([username, prname])  #/username/prname으로 변함
    except:
        input_directory = None
    tqdm.pandas()

    ref, input_, output_ = Read_Arg_(username,prname,"BassModel")

    input_name = os.path.join(input_directory, input_)  
    input_data = import_dataframe(input_name) #input file/information 열에 있는 것들을 dataframe으로 변환하여 가져오는 함수
    # input data는 period sales 를 담은 것
    # input data에서 cumulative sales, cumulative sales^2 만들고 m,p,q 추출 -> graph plotting

   
    sale = input_data['sales']

    sales = [0]
    for k in sale :
        sales.append(k)


    cumulative_sales = list(itertools.accumulate(sales))
    diff = pd.DataFrame({'sales' : sales[1:], 'cumulative sales' : cumulative_sales[:-1]})
    diff['cumulative sales^2'] = diff['cumulative sales']**2
    lr = LinearRegression()
    Y = diff['sales']
    X = diff[['cumulative sales','cumulative sales^2']]

    lm = lr.fit(X[:ref],Y[:ref])

    # intercept = pm ; b1 = q-p, b2=-q/m


    a = lm.intercept_
    b = lm.coef_[0]
    c = lm.coef_[1]

    # m = (-b + (b**2-4*c*a)**(1/2))/(2*c)
    m = (-b - (b**2-4*c*a)**(1/2))/(2*c)
    p = a/m
    q=-c*m

    predict = lm.predict(X)


    plt.rcParams['figure.figsize'] = (15.0, 8.0) # set default size of plots
    plt.rcParams['image.interpolation'] = 'nearest'
    plt.rcParams['image.cmap'] = 'gray'
    plt.rcParams["font.family"] = 'NanumGothic'
    plt.rcParams["font.size"] = 20
    plt.xlabel('period')
    plt.ylabel('sales')
    plt.axvline(ref, 0, 1, color='lightgray', linestyle='--', linewidth=2, label = 'reference')
    plt.plot(range(1,len(diff)+1),predict, linestyle = 'solid',marker = 'o',color='orange', label = 'predicted')
    plt.plot(range(1,len(diff)+1),Y, linestyle = 'solid',marker = 'o',color='red', label = 'actual')
    plt.legend()
    plt.title('최대시장규모 : {}, 혁신계수 : {}, 모방계수 : {}, 혁신지수 : {} '.format(round(m,3),round(p,3),round(q,3),round(p/q,3)))


    Y_true_is = Y[:ref]
    Y_pred_is = performance[:ref]
    Y_true_os= Y[ref:]
    Y_pred_os = performance[ref:]

    MSE_is = np.square(np.subtract(Y_true_is,Y_pred_is)).mean()
    MSE_os = np.square(np.subtract(Y_true_os,Y_pred_os)).mean()



    # return m,p,q, MSE_is, MSE_os

    df=pd.DataFrame({'최대시장규모(m)' : m,'혁신계수(p)' : p, '모방계수(q)' :q, '혁신지수(p/q)' : p/q, 'reference/total' : '{}/{}'.format(ref,len(Y)), 
                 'in_sample MSE' : MSE_is, 'out_sample MSE' : MSE_os})
    plt.savefig('{}_Bassmodel.png'.format(input_[:input_.index('.')]))
    df.to_csv('{}_Bassmodel.csv'.format(input_[:input_.index('.')]))


# +
#local 함수
def BassModel(username,prname):
    import os, re
    from tqdm import tqdm
    from utils import Read_Arg_, Read_Sheet_, import_dataframe, export_dataframe
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd 
    from sklearn.linear_model import LinearRegression
    import math
    import itertools
    
    try:
        input_directory = "/".join([username, prname])  #/username/prname으로 변함
    except:
        input_directory = None
    tqdm.pandas()

#     ref, input_, output_ = Read_Arg_(username,prname,"BassModel")

#     input_name = os.path.join(input_directory, input_)  
#     input_data = import_dataframe(input_name) #input file/information 열에 있는 것들을 dataframe으로 변환하여 가져오는 함수
#     # input data는 period sales 를 담은 것
    # input data에서 cumulative sales, cumulative sales^2 만들고 m,p,q 추출 -> graph plotting

    input_ = 'test.xlsx'
    ref = 18
    input_data = pd.read_excel('diffusion.xlsx')
    sale = input_data['sales']

    sales = [0]
    for k in sale :
        sales.append(k)


    cumulative_sales = list(itertools.accumulate(sales))
    diff = pd.DataFrame({'sales' : sales[1:], 'cumulative sales' : cumulative_sales[:-1]})
    diff['cumulative sales^2'] = diff['cumulative sales']**2
    lr = LinearRegression()
    Y = diff['sales']
    X = diff[['cumulative sales','cumulative sales^2']]

    lm = lr.fit(X[:ref],Y[:ref])

    # intercept = pm ; b1 = q-p, b2=-q/m


    a = lm.intercept_
    b = lm.coef_[0]
    c = lm.coef_[1]

    # m = (-b + (b**2-4*c*a)**(1/2))/(2*c)
    m = (-b - (b**2-4*c*a)**(1/2))/(2*c)
    p = a/m
    q=-c*m

    predict = lm.predict(X)


    plt.rcParams['figure.figsize'] = (15.0, 8.0) # set default size of plots
    plt.rcParams['image.interpolation'] = 'nearest'
    plt.rcParams['image.cmap'] = 'gray'
    plt.rcParams["font.family"] = 'NanumGothic'
    plt.rcParams["font.size"] = 20
    plt.xlabel('period')
    plt.ylabel('sales')
    plt.axvline(ref, 0, 1, color='lightgray', linestyle='--', linewidth=2, label = 'reference')
    plt.plot(range(1,len(diff)+1),predict, linestyle = 'solid',marker = 'o',color='orange', label = 'predicted')
    plt.plot(range(1,len(diff)+1),Y, linestyle = 'solid',marker = 'o',color='red', label = 'actual')
    plt.legend()
    plt.title('최대시장규모 : {}, 혁신계수 : {}, 모방계수 : {}, 혁신지수 : {} '.format(round(m,3),round(p,3),round(q,3),round(p/q,3)))


    Y_true_is = Y[:ref]
    Y_pred_is = predict[:ref]
    Y_true_os= Y[ref:]
    Y_pred_os = predict[ref:]

    MSE_is = np.square(np.subtract(Y_true_is,Y_pred_is)).mean()
    MSE_os = np.square(np.subtract(Y_true_os,Y_pred_os)).mean()



    # return m,p,q, MSE_is, MSE_os

    df=pd.DataFrame({'최대시장규모(m)' : m,'혁신계수(p)' : p, '모방계수(q)' :q, '혁신지수(p/q)' : p/q, 'reference/total' : '{}/{}'.format(ref,len(Y)), 
                 'in_sample MSE' : MSE_is, 'out_sample MSE' : MSE_os},index = [0])
    plt.savefig('{}_Bassmodel.png'.format(input_[:input_.index('.')]))
    df.to_csv('{}_Bassmodel.csv'.format(input_[:input_.index('.')]))
