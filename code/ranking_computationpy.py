# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 19:32:47 2021

@author: Jason
"""
import os
import pickle
import datetime
import pandas as pd
import numpy as np

# load data
result_path = '../data/processed/re-kaichen-change'
outbreak_df = pd.read_excel('../data/pork_export_import.xlsx')
natural_dist_array = pickle.load(open(os.path.join(result_path, 
    'natural_distance_array.pkl'), 'rb'))
trafic_dist_array = pickle.load(open(os.path.join(result_path,
    'transportation_distance_array.pkl'), 'rb'))
demand_dist_array = pickle.load(open(os.path.join(result_path,
    'demand-adjusted_distance_array.pkl'), 'rb'))
province_map_df = pd.read_excel('../data/code_mainland.xlsx')

# preprocess
outbreak_df['outbreak'] = pd.to_datetime(outbreak_df['outbreak']) 
index2province_map = {row['FID']: row['PINYIN_NAM'] for _, row in province_map_df.iterrows()}
province2index_map = {row['PINYIN_NAM']: row['FID'] for _, row in province_map_df.iterrows()}
province_order = list(outbreak_df['name'])
province_outbreak = list(outbreak_df['outbreak'])

# ranking computation
def get_rank(infected_province, suspectible_province_index, current_province_index):
    # dist_current = dist_from_province[current_province_index]
    # dist_suspectible = dist_from_province[suspectible_province_index]
    # current_province_reindex = np.where(dist_suspectible == dist_current)[0][0]
    # dist_suspectible_order = dist_suspectible.argsort().argsort()
    # return dist_suspectible_order[current_province_reindex], dist_current
    pass
    # dist_from_province_order = dist_from_province.argsort().argsort()
    # return dist_from_province_order[current_province_index]-1, dist_current

def get_prediction(current_province, dist_array, infected_province, suspectible_province):
    current_province_index = province2index_map[current_province]
    infected_province_index = np.array([province2index_map[ip] for ip in infected_province])
    suspectible_province_index = np.array([province2index_map[sp] for sp in suspectible_province])
    
    # distance from infected to suspectible
    dist = dist_array[infected_province_index[:,None], suspectible_province_index]
    dist = dist.reshape(
        len(infected_province_index), len(suspectible_province_index)).T
    min_dist = np.min(dist, axis=1) # min distance for each suspectible province
    min_from = np.argmin(dist, axis=1) # from province for each min distance
    
    current_province_dist = min_dist[0]
    from_index = infected_province_index[min_from[0]]
    
    min_dist_order = min_dist.argsort().argsort()
    rank = min_dist_order[0]
    
    return rank, from_index, current_province_dist
    
def generate_rank(dist_array, order_list):
    rank_list, from_list, dist_list = [0], [0], [0]
    infected_province = [order_list[0]]
    for current_idx in range(1, len(order_list)):
        # print(current_p)
        current_p = order_list[current_idx]
        current_outbreak = province_outbreak[current_idx]
        infected_latest_outbreak = current_outbreak - datetime.timedelta(7)
        # infected_latest_outbreak = current_outbreak
        infected_province = list(outbreak_df[
            outbreak_df['outbreak'] <= infected_latest_outbreak]['name'])
        
        suspectible_province = order_list[current_idx:]
        
        rank, from_index, dist = get_prediction(current_p, dist_array, 
                                                infected_province, suspectible_province)
        
        rank_list.append(rank+1)
        from_list.append(from_index)
        dist_list.append(dist)
        infected_province.append(current_p)
    code_list = [province2index_map[p] for p in order_list]
    result_pd = pd.DataFrame({'code': code_list,
                              'province': order_list,
                              'rank': rank_list,
                              'from': from_list,
                              'dist': dist_list})
    return result_pd

natural_dist_result_pd = generate_rank(natural_dist_array, province_order)
travel_dist_result_pd = generate_rank(trafic_dist_array, province_order)  
demand_dist_result_pd = generate_rank(demand_dist_array, province_order)

print('natural', sum(natural_dist_result_pd['rank']))
print('travel', sum(travel_dist_result_pd['rank']))
print('demand', sum(demand_dist_result_pd['rank']))

# save_path = '../result/re-kaichen-change'
# natural_dist_result_pd.to_csv(os.path.join(save_path, 'res_NDS.csv'), 
#                               index=False, encoding='utf_8_sig')
# travel_dist_result_pd.to_csv(os.path.join(save_path, 'res_TDS.csv'), 
#                              index=False, encoding='utf_8_sig')
# demand_dist_result_pd.to_csv(os.path.join(save_path, 'res_DaTDS.csv'), 
#                              index=False, encoding='utf_8_sig')

se = ['江苏', '上海', '浙江', '福建', '江西', '安徽', '广东', '广西', '海南']
print('SE-natural', sum(natural_dist_result_pd[natural_dist_result_pd['province'].isin(
    se)]['rank'])/3)
print('SE-travel', sum(travel_dist_result_pd[travel_dist_result_pd['province'].isin(
    se)]['rank'])/3)
print('SE-demand', sum(demand_dist_result_pd[demand_dist_result_pd['province'].isin(
    se)]['rank'])/3)

# t-test
from scipy import stats
(statistic, pvalue) = stats.ttest_ind(demand_dist_result_pd['rank'], 
                                      natural_dist_result_pd['rank'])


