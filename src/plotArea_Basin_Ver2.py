#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 09:57:52 2020

@author: mbonnema
"""

import datetime
import numpy as np
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from InterpAreas_Ver2 import InterpolateAreas
import ee
ee.Initialize()

#----controls------------------------------------------------------------------
basinNumber = 8
totalFlag = 0
lakeFlag = 1
resFlag = 1

S1ResultsPath = '../../Results/World_Ver2/'
basins = ee.FeatureCollection('WWF/HydroSHEDS/v1/Basins/hybas_2') \
    .filter(ee.Filter.gte('PFAF_ID',10*basinNumber)) \
    .filter(ee.Filter.lt('PFAF_ID',10*(basinNumber+1)))

largeLakes = ee.FeatureCollection('users/matthewbonnema/HydroLAKES') \
    .filter(ee.Filter.gt('Lake_area',100)) \
    .filter(ee.Filter.lt('Lake_area',1000))  \
    .filterBounds(basins)

basinIDs = basins.aggregate_array('PFAF_ID').getInfo()
plt.figure(figsize=(10,5))
LakeA = 0
LakeAup = 0
LakeAlow = 0
ResA = 0
ResAup = 0
ResAlow = 0
for bID in basinIDs:
    basin = basins.filter(ee.Filter.eq('PFAF_ID',bID))
    # All water bodies

    try:
        if totalFlag == 1:
            lakes = largeLakes.filterBounds(basin)
            lakeID = lakes.aggregate_array('system:index').getInfo()
            IDlist = lakeID
            IDs, Dates, Areas, Werror, Lerror = InterpolateAreas(S1ResultsPath,IDlist)
            nLakes = str(len(Areas))
            totalA = np.sum(Areas,0)
            meanA = np.mean(totalA)
            totalAup = np.sum(Werror,0)
            totalAlow = np.sum(Lerror,0)
            totalAup = ((totalA + totalAup) - meanA)/meanA
            totalAlow = ((totalA + totalAlow) - meanA)/meanA
            totalA = (totalA - np.mean(totalA))/meanA
            pltLabel = 'BasinID: '+str(bID)+' ('+nLakes+')'
            plt.plot(Dates,totalA, label=pltLabel, marker=".")
            myFmt = mdates.DateFormatter("%Y-%m-%d")
            plt.gca().xaxis.set_major_formatter(myFmt)
        
        # Lakes
        if lakeFlag == 1:
            lakes = largeLakes.filterBounds(basin) \
                .filter(ee.Filter.eq('Lake_type',1))
            lakeID = lakes.aggregate_array('system:index').getInfo()
            IDlist = lakeID
            IDs, Dates, Areas, Werror, Lerror = InterpolateAreas(S1ResultsPath,IDlist)
            totalA = np.sum(Areas,0)
            totalAup = np.sum(Werror,0) + totalA
            totalAlow = totalA - np.sum(Lerror,0) 
            LakeA = LakeA + totalA
            LakeAup = LakeAup + totalAup
            LakeAlow = LakeAlow + totalAlow
            #plt.plot(Dates,totalA, label=str(bID), marker=".", color='blue')
            #myFmt = mdates.DateFormatter("%Y-%m-%d")
            #plt.gca().xaxis.set_major_formatter(myFmt)
        
        # Reservoir
        if resFlag == 1:
            lakes = largeLakes.filterBounds(basin) \
                .filter(ee.Filter.gte('Lake_type',2))
            lakeID = lakes.aggregate_array('system:index').getInfo()
            IDlist = lakeID
            IDs, Dates, Areas, Werror, Lerror = InterpolateAreas(S1ResultsPath,IDlist)
            totalA = np.sum(Areas,0)
            totalAup = np.sum(Werror,0) + totalA
            totalAlow = totalA - np.sum(Lerror,0)
            ResA = ResA + totalA
            ResAup = ResAup + totalAup
            ResAlow = ResAlow + totalAlow
            #plt.plot(Dates,totalA, label=str(bID), marker=".", color='red')
            #myFmt = mdates.DateFormatter("%Y-%m-%d")
            #plt.gca().xaxis.set_major_formatter(myFmt)
    except:
        print('Area calulcation ended in error for basin: '+str(bID))

'''
for key in Storage:
    s = Storage[key]
    plt.plot(Dates,s, label=key, marker=".")
'''
try:
    if lakeFlag == 1:
        #LakeA = LakeA - np.mean(LakeA)
        LakeAmean = np.mean(LakeA)
        LakeA = (LakeA - LakeAmean)/LakeAmean*100
        LakeAup = (LakeAup - LakeAmean)/LakeAmean*100
        LakeAlow = (LakeAlow - LakeAmean)/LakeAmean*100
        plt.plot(Dates,LakeA, label='Lakes', marker=".", color='blue')
        plt.plot(Dates,LakeAup, linestyle=":", color='blue', linewidth=0.5)
        plt.plot(Dates,LakeAlow, linestyle=":", color='blue', linewidth=0.5)
        plt.fill_between(Dates,LakeAup,LakeAlow,color='blue',alpha=0.1)
        myFmt = mdates.DateFormatter("%Y-%m-%d")
        plt.gca().xaxis.set_major_formatter(myFmt)
except:
    pass
try:
    if resFlag == 1:
        #ResA = ResA - np.mean(ResA)
        ResAmean = np.mean(ResA)
        ResA = (ResA - np.mean(ResA))/np.mean(ResA)*100
        ResAup = (ResAup - ResAmean)/ResAmean*100
        ResAlow = (ResAlow - ResAmean)/ResAmean*100
        plt.plot(Dates,ResA, label='Reservoirs', marker=".", color='red')
        plt.plot(Dates,ResAup, linestyle=":", color='red', linewidth=0.5)
        plt.plot(Dates,ResAlow, linestyle=":", color='red', linewidth=0.5)
        plt.fill_between(Dates,ResAup,ResAlow,color='red',alpha=0.1)
        myFmt = mdates.DateFormatter("%Y-%m-%d")
        plt.gca().xaxis.set_major_formatter(myFmt)
except:
    pass
#### Plot Options
years = mdates.YearLocator()  
months = mdates.MonthLocator()  
years_fmt = mdates.DateFormatter('%Y')

plt.gca().xaxis.set_major_formatter(years_fmt)
plt.gca().xaxis.set_major_locator(years)
plt.gca().xaxis.set_minor_locator(months)
plt.gca().set_xlim(datetime.date(2017,1,1),datetime.date(2020,1,1))
plt.gca().format_xdata = mdates.DateFormatter('%Y-%m-%d')
plt.gca().format_ydata = lambda x: '$%1.2f' % x  
plt.gca().grid(True)
leg = plt.gca().legend(frameon=False, loc='upper left', ncol=2)

'''
#Plot options for area
plt.gca().set_ylim(0,350)
plt.gca().set_ylabel('Water Surface Area [km^2]', fontsize = 16)
plt.title('Surface Area')
'''
'''
#Plot options for storage change
plt.gca().set_ylim(-1,1)
plt.gca().set_ylabel('Water storage change [km^3/month]', fontsize = 16)
plt.title('Storage Change')
'''
'''
#Plot options for cummulative storage
plt.gca().set_ylim(-2,2)
plt.gca().set_ylabel('Water storage [km^3]', fontsize = 16)
plt.title('Total Storage Relative to Initial')
'''

#Plot options for normalized storage
#plt.gca().set_ylim(-20,20)
#plt.gca().set_ylabel('Water Surface Area Anomaly [km^2]', fontsize = 16)
plt.gca().set_ylabel('Water Surface Area Anomaly [%]', fontsize = 16)
plt.title('Basin '+str(basinNumber)+' Water Surface Area Anomaly')


