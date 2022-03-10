#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 09:16:42 2022

@author: mbonnema
"""

import os
from netCDF4 import Dataset
import matplotlib.pyplot as plt
#import geopandas as geo
import datetime
import numpy as np
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import ee
ee.Initialize()
import shapely
import matplotlib.lines as mlines
import csv

from readCSV import readCSV
from FilterS1 import FilterS1
from FilterJRC import FilterJRC
from InterpS1 import InterpS1
from InterpJRC import InterpJRC

print('Preparing Data...')
dataDir = '../../Results/World_Ver3_CSV/'
print('\tReading data csv files...')
D,A,LE,WE,ND = readCSV(dataDir)
Ds1 = {}
As1 = {}
Dgsw = {}
Agsw = {}
#print(LE['1646'])
[Ds1, Dgsw] = map(lambda keys: {x: D[x] for x in keys}, [WE.keys(), ND.keys()])
[As1, Agsw] = map(lambda keys: {x: A[x] for x in keys}, [WE.keys(), ND.keys()])
print('\t\tComplete')

print('\tFiltering area data...')
Ds1,As1,WE,LE = FilterS1(Ds1,As1,WE,LE)
Dgsw,Agsw,ND = FilterJRC(Dgsw,Agsw,ND)
D = {}
A = {}
D.update(Ds1)
D.update(Dgsw)
A.update(As1)
A.update(Agsw)
print('\t\tComplete')

print('\tLoading Lake Database Fields...')
lakes = ee.FeatureCollection('users/matthewbonnema/HydroLAKES')
largeLakes = lakes.filter(ee.Filter.gte('Lake_area',1))
    
lakeID = largeLakes.aggregate_array('Hylak_id').getInfo()
lakeType = largeLakes.aggregate_array('Lake_type').getInfo()
lakeLat = largeLakes.aggregate_array('Pour_lat').getInfo()
lakeLon = largeLakes.aggregate_array('Pour_long').getInfo()
lakeArea = largeLakes.aggregate_array('Lake_area').getInfo()
print('\t\tComplete')

print('\tCompute Area Variations...')
Av = []
Avp = []
Am = []
A_database = []
Amin = []
Amax = []
lat = []
lon = []
Ltype = []
for key in D:
    try:
        a = A[key]
        stda = np.std(a)
        mina = np.nanmin(a)
        maxa = np.nanmax(a)
        vara = maxa - mina
        meana = np.nanmean(a)
        varap = vara/meana
        ad = lakeArea[lakeID.index(int(key))]
        index = lakeID.index(int(key))
        
        if np.isnan(mina) or np.isnan(maxa) or np.isnan(meana) or np.isnan(vara):
            continue
        Av.append(vara)
        Avp.append(varap)
        Am.append(meana)
        A_database.append(ad)
        Amin.append(mina)
        Amax.append(maxa)
        lat.append(lakeLat[index])
        lon.append(lakeLon[index])
        lt = lakeType[index]
        if lt == 3:
            lt = 2 
        Ltype.append(lt)
    except:
        continue

A_database = np.array(A_database)[np.isfinite(np.array(Avp))] 
Av = np.array(Av)[np.isfinite(np.array(Avp))] 
Am = np.array(Am)[np.isfinite(np.array(Avp))]
Amin = np.array(Amin)[np.isfinite(np.array(Avp))] 
Amax = np.array(Amax)[np.isfinite(np.array(Avp))]
lat = np.array(lat)[np.isfinite(np.array(Avp))] 
lon = np.array(lon)[np.isfinite(np.array(Avp))] 
Ltype = np.array(Ltype)[np.isfinite(np.array(Avp))]
Avp = np.array(Avp)[np.isfinite(np.array(Avp))] 

Av = np.array(Av)
Avp = np.array(Avp)
Avp = Avp*100
Am = np.array(Am)
A_d = np.array(A_database)
print('\t\tComplete')

print('\tInterpolate Areas...')
D_int,A_int,WE_int,LE_int = InterpS1(Ds1,As1,WE,LE)
D_int_jrc,A_int_jrc = InterpJRC(Dgsw,Agsw)

print('\t\tComplete')

print('\tGetting Lake Type Info for Interpolated Data...')
Type = {}
lakeID = largeLakes.aggregate_array('Hylak_id').getInfo()
for key in D_int:
    try:
        t = lakeType[lakeID.index(int(key))]
        Type[key] = t
    except:
        continue
print('\t\tComplete')
print('Finished Loading Data')

