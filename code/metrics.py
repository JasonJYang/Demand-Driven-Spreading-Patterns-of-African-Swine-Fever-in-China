# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 14:33:57 2021

@author: Jason
"""
import os
import pandas as pd
import numpy as np
import ml_metrics as metrics
from tqdm import tqdm

# load data
result_path = '../result/re-kaichen-change'
res_NDS_pd = pd.read_csv(os.path.join(result_path, 'res_NDS.csv')).iloc[1:]
res_TDS_pd = pd.read_csv(os.path.join(result_path, 'res_TDS.csv')).iloc[1:]
res_DaTDS_pd = pd.read_csv(os.path.join(result_path, 'res_DaTDS.csv')).iloc[1:]

def precision(actual, predicted, k):
    act_set = set(actual)
    pred_set = set(predicted[:k])
    result = len(act_set & pred_set) / float(min(len(act_set), k))
    return result

def recall(actual, predicted, k):
    act_set = set(actual)
    pred_set = set(predicted[:k])
    result = len(act_set & pred_set) / float(len(act_set))
    return result

def precision_recall_k(pd, k):
    rank_list = list(pd['rank'])
    actual = []
    predicted = []
    for idx in range(len(rank_list)):
        actual.append([1.0])
        row = list(np.random.random(len(pd)))
        row[rank_list[idx]-1] = 1.0
        predicted.append(row)
    mean_k_precision = metrics.mapk(actual, predicted, k)
    recall_list = [recall(actual[idx], predicted[idx], k) for idx in range(len(actual))]
    mean_k_recall = np.mean(recall_list)
    return mean_k_precision, mean_k_recall

def random_precision_reall_k(k, repeated_times):
    mean_k_precision, mean_k_recall = [], []
    for _ in range(repeated_times):
        actual, predicted = [], []
        for idx in range(30):
            actual.append([1.0])
            row = list(np.random.random(30))
            row[np.random.choice(30, 1)[0]] = 1.0
            predicted.append(row)
        mean_k_precision.append(metrics.mapk(actual, predicted, k))
        recall_list = [recall(actual[idx], predicted[idx], k) for idx in range(len(actual))]
        mean_k_recall.append(np.mean(recall_list))
    return np.mean(mean_k_precision), np.mean(mean_k_recall)

random_precision, NDS_precision, TDS_precision, DaTDS_precision = [], [], [], [] 
random_recall, NDS_recall, TDS_recall, DaTDS_recall = [], [], [], [] 
for k in tqdm(range(1, 31)):
    r_p, r_r = random_precision_reall_k(k, 100)
    n_p, n_r = precision_recall_k(res_NDS_pd, k)
    t_p, t_r = precision_recall_k(res_TDS_pd, k)
    d_p, d_r = precision_recall_k(res_DaTDS_pd, k)
    
    random_precision.append(r_p)
    random_recall.append(r_r)
    NDS_precision.append(n_p)
    NDS_recall.append(n_r)
    TDS_precision.append(t_p)
    TDS_recall.append(t_r)
    DaTDS_precision.append(d_p)
    DaTDS_recall.append(d_r)
    
precision_k = pd.DataFrame({'k': list(range(1,31)),
                            'random': random_precision,
                            'NDS': NDS_precision,
                            'TDS': TDS_precision,
                            'DaTDS': DaTDS_precision})
recall_k = pd.DataFrame({'k': list(range(1,31)),
                         'random': random_recall,
                         'NDS': NDS_recall,
                         'TDS': TDS_recall,
                         'DaTDS': DaTDS_recall})

precision_k.to_csv(os.path.join(result_path, 'precision.csv'), index=False)
recall_k.to_csv(os.path.join(result_path, 'recall.csv'), index=False)



