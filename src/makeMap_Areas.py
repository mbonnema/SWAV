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
import matplotlib.lines as mlines

markerScale = 50
fig, ax = plt.subplots()

ax.set_aspect('equal')
world = geo.read_file(geo.datasets.get_path('naturalearth_lowres'))
worldPlot=world.plot(ax=ax, color='white', edgecolor='black')

S1ResultsPath = '../../Results/World_Ver2/'
#S1ResultsPath = '../../Results/World_gt100_lt1000/'
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
            
IDs, Dates, Areas, Werror, Lerror = InterpolateAreas(S1ResultsPath,IDlist)
Avar = []
Amin = []
Amax = []
Aavg = []
for a in Areas:
    maxa = np.max(a)
    mina = np.min(a)
    Amin.append(mina)
    Amax.append(maxa)
    Avar.append(maxa-mina)
    Aavg.append(np.mean(a))
normMinA = np.array(Amin)/np.array(Aavg)
normMaxA = np.array(Amax)/np.array(Aavg)
Avar_perc = np.array(Avar)/np.array(Aavg)
lat = []
lon = []
Ltype = []
Larea = []
for key in IDs:
    index = lakeID.index(key)
    lat.append(lakeLat[index])
    lon.append(lakeLon[index])
    lt = lakeType[index]
    Larea.append(lakeArea[index])
    if lt == 3:
        lt = 2 
    Ltype.append(lt)

Lakesdf = pd.DataFrame(
    {'LakeType': Ltype,
     'Latitude': lat,
     'Longitude': lon})
Lakesgdf = geo.GeoDataFrame(
    Lakesdf, geometry=geo.points_from_xy(Lakesdf.Longitude, Lakesdf.Latitude))
colorMapmin = []
for t in Ltype:
    if t == 2:
        colorMapmin.append('#ff8888')
    elif t == 1:
        colorMapmin.append('#8888ff')
markerSizemin = []
for a in Amin:
    markerSizemin.append((a/markerScale)**1.5)


colorMapmax = []
for t in Ltype:
    if t == 2:
        colorMapmax.append('#ff0000')
    elif t == 1:
        colorMapmax.append('#0000ff')
markerSizemax = []
for a in Amax:
    markerSizemax.append((a/markerScale)**1.5)

LakePlotmax = Lakesgdf.plot(ax=ax, c=colorMapmax, markersize=markerSizemax, linewidths=3)
LakePlotmin = Lakesgdf.plot(ax=ax, c=colorMapmin, markersize=markerSizemin)

BlueLake = mlines.Line2D([], [], color='blue', marker='o',markersize=10, label='Lakes', lineWidth = 0)
RedRes = mlines.Line2D([], [], color='Red', marker='o',markersize=10, label='Reservoirs', lineWidth = 0)
lakesize100 = mlines.Line2D([], [], color='grey', marker='o',markersize=(100/markerScale), label='100 $\mathregular{km^{2}}$', lineWidth = 0)
lakesize300 = mlines.Line2D([], [], color='grey', marker='o',markersize=(300/markerScale), label='300 $\mathregular{km^{2}}$', lineWidth = 0)
lakesize500 = mlines.Line2D([], [], color='grey', marker='o',markersize=(500/markerScale), label='500 $\mathregular{km^{2}}$', lineWidth = 0)
lakesize700 = mlines.Line2D([], [], color='grey', marker='o',markersize=(700/markerScale), label='700 $\mathregular{km^{2}}$', lineWidth = 0)
lakesize900 = mlines.Line2D([], [], color='grey', marker='o',markersize=(900/markerScale), label='900 $\mathregular{km^{2}}$', lineWidth = 0)
plt.legend(handles=[BlueLake,RedRes,lakesize100,lakesize300,lakesize500,lakesize700,lakesize900], loc="upper right")
plt.gca().axes.get_xaxis().set_visible(False)
plt.gca().axes.get_yaxis().set_visible(False)
plt.show()
'''
legend1 = LakePlot.legend(*ax.legend_elements(),
                    loc="lower left", title="Water Body Type")
handles, labels = LakePlot.legend_elements(prop="sizes", alpha=0.6)
legend2 = ax.legend(handles, labels, loc="upper right", title="Lake Area")
'''
