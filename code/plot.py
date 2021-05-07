# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 16:37:06 2021

@author: Jason
"""
import pandas as pd
import matplotlib.pyplot as plt

precision_k = pd.read_csv('../result/re-kaichen-change/precision.csv')
recall_k = pd.read_csv('../result/re-kaichen-change/recall.csv')

select_k = ['2', '5', '10', '15', '20']

def plot(pd, ylabel, save_path):
    size = 15
    plt.plot(select_k, list(pd[pd['k'].isin(select_k)]['random']),
             label = 'Random', color='b', marker='o')
    plt.plot(select_k, list(pd[pd['k'].isin(select_k)]['NDS']),
             label = 'NDS', color='g', marker='x')
    plt.plot(select_k, list(pd[pd['k'].isin(select_k)]['TDS']),
             label = 'TDS', color='orange', marker='^')
    plt.plot(select_k, list(pd[pd['k'].isin(select_k)]['DaTDS']),
             label = 'DaTDS', color='r', marker='*')
    plt.xlabel('K',fontsize=size)
    plt.ylabel(ylabel,fontsize=size)
    plt.xticks(select_k,fontsize=size)
    plt.yticks(fontsize=size)
    plt.legend(fontsize=size)
    plt.grid()
    plt.savefig(save_path+ylabel+'.svg', bbox_inches='tight', dpi=600)
    plt.show()
    
save_path = '../result/re-kaichen-change/'
plot(precision_k, ylabel='Precision@K', save_path=save_path)
plot(recall_k, ylabel='Recall@K', save_path=save_path)

# comparison 
d1 = precision_k[precision_k['k']==5]['DaTDS'].values[0]
d2 = precision_k[precision_k['k']==5]['TDS'].values[0]



