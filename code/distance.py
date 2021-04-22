# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 13:59:46 2021

@author: Jason
"""
import pickle
import numpy as np
import pandas as pd
import networkx as nx
from geopy.distance import great_circle

# load data
capital_df = pd.read_excel('../data/province_capital.xlsx')
province_map_df = pd.read_excel('../data/code.xlsx')
trafic_dist_df = pd.read_excel('../data/distance_all.xlsx')
slaughter_house_df = pd.read_csv('../data/sla_result.csv')
pork_export_import_df = pd.read_excel('../data/pork_export_import.xlsx')

# preprocess
index2province_map = {row['FID']: row['PINYIN_NAM'] for _, row in province_map_df.iterrows()}
capital_df.sort_values(by='FID', inplace=True)

# natural distance
natural_dist_list = []
for idx, row in capital_df.iterrows():
    location1 = (row['latitude'], row['longitude'])
    ndl = []
    for idx, row in capital_df.iterrows():
        location2 = (row['latitude'], row['longitude'])
        ndl.append(great_circle(location1, location2).meters/1000)
    natural_dist_list.append(ndl)
natural_dist_array = np.array(natural_dist_list)
# remove the data of Taiwan, Macao, and Hong Kong
natural_dist_array = np.delete(natural_dist_array, [30, 31, 32], 0)
natural_dist_array = np.delete(natural_dist_array, [30, 31, 32], 1)

def dijkstra_fill_array(array):
    G = nx.from_numpy_matrix(array)
    array_full = array.copy()
    row_num, col_num = array.shape
    for p1 in range(row_num):
        for p2 in range(col_num):
            array_full[p1, p2] = nx.dijkstra_path_length(G, p1, p2)
    return array_full
# trafic distance
trafic_dist_array = trafic_dist_df.to_numpy()[1:, 2:].astype(np.float64)
trafic_dist_array += trafic_dist_array.T
trafic_dist_array = np.delete(trafic_dist_array, [30, 31, 32], 0)
trafic_dist_array = np.delete(trafic_dist_array, [30, 31, 32], 1)
trafic_dist_array_full = dijkstra_fill_array(trafic_dist_array)

# demand-adjusted transport distance
# pork export and import
import_list = []
for p_idx in range(34):
    p_name = index2province_map[p_idx]
    p_data = pork_export_import_df[pork_export_import_df['name']==p_name] 
    if len(p_data) == 0:
        continue
    else:
        import_ratio = (p_data['Import Ratio (%)'].values[0] \
                        - p_data['Export Rate (%)'].values[0])/100
        import_list.append(import_ratio)

# slaughter hourse number
slaughter_house_array = slaughter_house_df.to_numpy()
slaughter_house_array = np.delete(slaughter_house_array, [30, 31, 32], 0)
slaughter_house_array = np.delete(slaughter_house_array, [30, 31, 32], 1)
slaughter_house_array_full = dijkstra_fill_array(slaughter_house_array)

# distance computation
demand_dist_list = []
for i in range(31):
    demand_list = []
    for j in range(31):
        if import_list[i] < 0 and import_list[j] > 0:
            d = trafic_dist_array_full[i,j] / np.log(slaughter_house_array_full[i,j]/\
                np.exp(import_list[i]+import_list[j]))
        elif import_list[i] < 0:
            d = trafic_dist_array_full[i,j] / np.log(slaughter_house_array_full[i,j])
        else:
            d = trafic_dist_array_full[i,j]
        demand_list.append(d)
    demand_dist_list.append(demand_list)
demand_dist_array = np.array(demand_dist_list)

with open('../data/processed/natural_distance_array.pkl', 'wb') as f:
    pickle.dump(natural_dist_array, f)
    
with open('../data/processed/transportation_distance_array.pkl', 'wb') as f:
    pickle.dump(trafic_dist_array_full, f)
    
with open('../data/processed/demand-adjusted_distance_array.pkl', 'wb') as f:
    pickle.dump(demand_dist_array, f)
        
    
    
