#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 09:29:05 2021

@author: mbonnema
"""

import os
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import geopandas as geo
import datetime
import numpy as np
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from InterpAreas_Ver2 import InterpolateAreas
import pandas as pd
import ee
ee.Initialize()
import shapely

markerScale = 50
fig, ax = plt.subplots()


S1ResultsPath = '../../Results/World_Ver2/'
lakes = ee.FeatureCollection('users/matthewbonnema/HydroLAKES')
largeLakes = lakes.filter(ee.Filter.gt('Lake_area',100)) \
    .filter(ee.Filter.lt('Lake_area',1000)) 
    
lakeID = largeLakes.aggregate_array('system:index').getInfo()
lakeType = largeLakes.aggregate_array('Lake_type').getInfo()
lakeName = largeLakes.aggregate_array('Lake_name').getInfo()
lakeContinent = largeLakes.aggregate_array('Continent').getInfo()
lakeLat = largeLakes.aggregate_array('Pour_lat').getInfo()
lakeLon = largeLakes.aggregate_array('Pour_long').getInfo()
lakeElevation = largeLakes.aggregate_array('Elevation').getInfo()
lakeSlope = largeLakes.aggregate_array('Slope_100').getInfo()
lakeVol = largeLakes.aggregate_array('Vol_total').getInfo()
lakeArea = largeLakes.aggregate_array('Lake_area').getInfo()


#### World Total################################################################
IDlist = []
for ID, Cont, Type in zip(lakeID,lakeContinent,lakeType):
    if Cont != 'null':
        
        if Type == 1 or Type == 2 or Type == 3:
            IDlist.append(ID)
IDlist = lakeID            
IDs, Dates, Areas, Werror, Lerror = InterpolateAreas(S1ResultsPath,IDlist)
Avar = []
Amin = []
Amax = []
Aavg = []
LT = []
for a,ID in zip(Areas,IDs):
    maxa = np.max(a)
    mina = np.min(a)
    Amin.append(mina)
    Amax.append(maxa)
    Avar.append(maxa-mina)
    Aavg.append(np.mean(a))
    
    lt = lakeType[lakeID.index(ID)]
    if lt == 3:
        lt = 2
    LT.append(lt)

LT = np.array(LT)
normMinA = np.array(Amin)/np.array(Aavg)
normMaxA = np.array(Amax)/np.array(Aavg)
Avar_perc = np.array(Avar)/np.array(Aavg)*100
Ifilt = Avar_perc < 110
Avar_perc = Avar_perc[Ifilt]
LT = LT[Ifilt]
x_sort = np.sort(Avar_perc)

#plt.plot(x_sort,np.arange(len(x_sort))/len(x_sort),c='purple')

Avar_percL = Avar_perc[LT==1]
Avar_percR = Avar_perc[LT==2]
x_sortL = np.sort(Avar_percL)
x_sortR = np.sort(Avar_percR)
plt.plot(x_sortL,np.arange(len(x_sortL))/len(x_sortL),c='blue')
plt.plot(x_sortR,np.arange(len(x_sortR))/len(x_sortR),c='red')
plt.gca().set_ylabel('Cumulative Distribution Function', fontsize = 24)
plt.gca().set_xlabel('Surface Area Variation [%]', fontsize = 24)