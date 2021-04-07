# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 15:33:54 2021

@author: kariln

SPATIAL FEATURES
"""
from scipy.spatial import distance
from datetime import datetime
from functions import column_check

def euclidean(data):
    now = datetime.now()
    print('Euclidean: ' + str(now))
    column_check(data,['Q_x','Q_y','Q_z','x','y','z'])
    data['euclidean_d_Q'] = None
    for index, row in data.iterrows():
      a = (row['Q_x'], row['Q_y'], row['Q_z'])
      b = (row['x'], row['y'], row['z'])
      dst = distance.euclidean(a, b)
      data['euclidean_d_Q'].iloc[index] = dst
    data.to_csv('disp_Pint.csv',encoding='utf-8',  index=False) 
    return data

def manhattan(data):
    now = datetime.now()
    print('Manhattan: ' + str(now))
    column_check(data,['Q_x','Q_y','Q_z','x','y','z'])
    data['manh_d_Q'] = None
    for index, row in data.iterrows():
      a = (row['Q_x'], row['Q_y'], row['Q_z'])
      b = (row['x'], row['y'], row['z'])
      dst = distance.cityblock(a, b)
      data['manh_d_Q'].iloc[index] = dst
    data.to_csv('disp_Pint.csv',encoding='utf-8',  index=False) 
    return data

def euclid_grad(data):
    now = datetime.now()
    print('Euclidean gradient: ' + str(now))
    column_check(data,['euclidean_d_Q'])
    data['euclid_grad'] = None
    num_i = data['i'].nunique()
    i = data['i'].unique()
    for j in range(0,num_i):
      data_i = data[data['i'] == i[j]] 
      indexes = data_i.index
      num = 0
      for index,row in data_i.iterrows():
        if num == 0: 
          data['euclid_grad'].iloc[index] = 0
        else:
          data['euclid_grad'].iloc[index] = data_i['euclidean_d_Q'].iloc[indexes[num]]-data_i['euclidean_d_Q'].iloc[indexes[num-1]]
        num += 1
    data.to_csv('disp_Pint.csv',encoding='utf-8',  index=False) 
    return data

def laser_dir(data):
    now = datetime.now()
    print('Laser direction: ' + str(now))
    column_check(data,['euclid_grad'])
    data['laser_dir'] = None
    for index,row in data.iterrows():
      if row['euclid_grad'] > 0: 
        data['laser_dir'].iloc[index] = 1
      else:
        data['laser_dir'].iloc[index] = 0
    data.to_csv('disp_dir.csv',encoding='utf-8',  index=False) 
    return data

def layerNum(data, nr_layers: int, layer_thickness: float, base_height: float):
    now = datetime.now()
    print('Layer number: ' + str(now))
    column_check(data,['z'])
    data['layerNum'] = None
    
    #Finding layer numbers and heights
    layers = []
    heights = []
    height = base_height
    for i in range(1,nr_layers + 1): 
        layers.append(i)
        height = height+layer_thickness
        heights.append(height)
        
    #Inserting layer numbers
    for index,row in data.iterrows():
        if row['z'] == base_height:
            data['layerNum'].iloc[index] = 1
        layer = 0
        for height in heights:
            if row['z'] == height:
                layer += 1
                data['layerNum'].iloc[index] = layer
                break
    data.to_csv('disp_layer.csv',encoding='utf-8',  index=False) 
    return data

def spatial(data, nr_layers: int, layer_thickness: float, base_height: float):
    now = datetime.now()
    print('Spatial: ' + str(now))
    data = layerNum(data, nr_layers, layer_thickness, base_height)
    data = euclidean(data)
    data = manhattan(data)
    data = euclid_grad(data)
    data = laser_dir(data)
    return data