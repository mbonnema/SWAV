#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 15:37:18 2020

@author: mbonnema
"""
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from InterpAreas_Ver2 import InterpolateAreas
import ee
ee.Initialize()


#----controls------------------------------------------------------------------
allWorld = 1
allLake = 1
allRes = 1
contLake = 0
contRes = 0

PlotType = 2


#S1ResultsPath = '../../Results/World_gt100_lt1000/'
S1ResultsPath = '../../Results/World_Ver2/'
lakes = ee.FeatureCollection('users/matthewbonnema/HydroLAKES')
largeLakes = lakes.filter(ee.Filter.gt('Lake_area',100)) \
    .filter(ee.Filter.lt('Lake_area',1000)) 
    #.filter(ee.Filter.eq('system:index','00000000000000003db1'))
    #.filter(ee.Filter.neq('Continent','North America'))
    
lakeID = largeLakes.aggregate_array('system:index').getInfo()
lakeType = largeLakes.aggregate_array('Lake_type').getInfo()
lakeName = largeLakes.aggregate_array('Lake_name').getInfo()
lakeContinent = largeLakes.aggregate_array('Continent').getInfo()

plt.figure(figsize=(10,5))

#### World Total################################################################
if allWorld == 1:
    
    IDlist = []
    for ID, Cont, Type in zip(lakeID,lakeContinent,lakeType):
        if Cont != 'null':
            if Type == 1 or Type == 2 or Type == 3:
                IDlist.append(ID)
    label = 'World Total SWBs'        
    color = 'purple'
    IDs, Dates, Areas, Werror, Lerror = InterpolateAreas(S1ResultsPath,IDlist)
    print(len(IDs))
    if PlotType == 0:
        Asum = np.sum(Areas,0)
        WerrorSum = np.sum(Werror,0)
        LerrorSum = np.sum(Lerror,0)
        AsumUp = Asum + WerrorSum
        AsumLow = Asum - LerrorSum
    elif PlotType == 1:
        Asum = np.sum(Areas,0)
        Asum = (Asum - np.mean(Asum))
        Amean = np.mean(Asum)
        WerrorSum = np.sum(Werror,0)
        LerrorSum = np.sum(Lerror,0)
        AsumUp = Asum + WerrorSum
        AsumLow = Asum - LerrorSum
    elif PlotType == 2:
        Asum = np.sum(Areas,0)
        Amean = np.mean(Asum)
        WerrorSum = np.sum(Werror,0)
        LerrorSum = np.sum(Lerror,0)
        AsumUp = Asum + WerrorSum
        AsumLow = Asum - LerrorSum
        Asum = (Asum - Amean)/Amean*100
        AsumUp = (AsumUp - Amean)/Amean*100
        AsumLow = (AsumLow - Amean)/Amean*100
    myFmt = mdates.DateFormatter("%Y-%m-%d")
    plt.plot(Dates,Asum, label=label, marker=".", color=color, linewidth=1)
    plt.plot(Dates,AsumUp, linestyle=":", color=color, linewidth=0.5)
    plt.plot(Dates,AsumLow, linestyle=":", color=color, linewidth=0.5)
    plt.fill_between(Dates,AsumUp,AsumLow,color=color,alpha=0.1)
    plt.gca().xaxis.set_major_formatter(myFmt)

#### World Lakes################################################################
if allLake == 1:    
    IDlist = []
    for ID, Cont, Type in zip(lakeID,lakeContinent,lakeType):
        if Cont != 'null':
            if Type == 1:
                IDlist.append(ID)
    
    label = 'World Natural Lakes' 
    color = 'blue'
    IDs, Dates, Areas, Werror, Lerror = InterpolateAreas(S1ResultsPath,IDlist)
    print(len(IDs))
    if PlotType == 0:
        Asum = np.sum(Areas,0)
        WerrorSum = np.sum(Werror,0)
        LerrorSum = np.sum(Lerror,0)
        AsumUp = Asum + WerrorSum
        AsumLow = Asum - LerrorSum
    elif PlotType == 1:
        Asum = np.sum(Areas,0)
        Asum = (Asum - np.mean(Asum))
        Amean = np.mean(Asum)
        WerrorSum = np.sum(Werror,0)
        LerrorSum = np.sum(Lerror,0)
        AsumUp = Asum + WerrorSum
        AsumLow = Asum - LerrorSum
    elif PlotType == 2:
        Asum = np.sum(Areas,0)
        Amean = np.mean(Asum)
        WerrorSum = np.sum(Werror,0)
        LerrorSum = np.sum(Lerror,0)
        AsumUp = Asum + WerrorSum
        AsumLow = Asum - LerrorSum
        Asum = (Asum - Amean)/Amean*100
        AsumUp = (AsumUp - Amean)/Amean*100
        AsumLow = (AsumLow - Amean)/Amean*100
    myFmt = mdates.DateFormatter("%Y-%m-%d")
    plt.plot(Dates,Asum, label=label, marker=".", color=color, linewidth=1)
    plt.plot(Dates,AsumUp, linestyle=":", color=color, linewidth=0.5)
    plt.plot(Dates,AsumLow, linestyle=":", color=color, linewidth=0.5)
    plt.fill_between(Dates,AsumUp,AsumLow,color=color,alpha=0.1)
    plt.gca().xaxis.set_major_formatter(myFmt)



#### World Reservoirs###########################################################
if allRes == 1:    
    IDlist = []
    for ID, Cont, Type in zip(lakeID,lakeContinent,lakeType):
        if Cont != 'null':
            if Type == 2 or Type == 3:
                IDlist.append(ID)

    color = 'red'
    label = 'World Artificial Reservoirs'
    IDs, Dates, Areas, Werror, Lerror = InterpolateAreas(S1ResultsPath,IDlist)
    print(len(IDs))
    if PlotType == 0:
        Asum = np.sum(Areas,0)
        WerrorSum = np.sum(Werror,0)
        LerrorSum = np.sum(Lerror,0)
        AsumUp = Asum + WerrorSum
        AsumLow = Asum - LerrorSum
    elif PlotType == 1:
        Asum = np.sum(Areas,0)
        Asum = (Asum - np.mean(Asum))
        Amean = np.mean(Asum)
        WerrorSum = np.sum(Werror,0)
        LerrorSum = np.sum(Lerror,0)
        AsumUp = Asum + WerrorSum
        AsumLow = Asum - LerrorSum
    elif PlotType == 2:
        Asum = np.sum(Areas,0)
        Amean = np.mean(Asum)
        WerrorSum = np.sum(Werror,0)
        LerrorSum = np.sum(Lerror,0)
        AsumUp = Asum + WerrorSum
        AsumLow = Asum - LerrorSum
        Asum = (Asum - Amean)/Amean*100
        AsumUp = (AsumUp - Amean)/Amean*100
        AsumLow = (AsumLow - Amean)/Amean*100
    myFmt = mdates.DateFormatter("%Y-%m-%d")
    plt.plot(Dates,Asum, label=label, marker=".", color=color, linewidth=1)
    plt.plot(Dates,AsumUp, linestyle=":", color=color, linewidth=0.5)
    plt.plot(Dates,AsumLow, linestyle=":", color=color, linewidth=0.5)
    plt.fill_between(Dates,AsumUp,AsumLow,color=color,alpha=0.1)
    plt.gca().xaxis.set_major_formatter(myFmt)
    

#### North America Reservoirs###########################################################
if contRes == 1:
    IDlist = []
    for ID, Cont, Type in zip(lakeID,lakeContinent,lakeType):
        if Cont == 'North America':
            if Type == 2 or Type == 3:
                IDlist.append(ID)
    
    IDs, Dates, Areas, Werror, Lerror = InterpolateAreas(S1ResultsPath,IDlist)
    Asum = np.sum(Areas,0)
    Asum = (Asum - np.mean(Asum))
    #WerrorSum = np.sum(Werror,0)
    WerrorSum = np.sqrt(np.sum(np.square(Werror),0))
    #LerrorSum = np.sum(Lerror,0)
    LerrorSum = np.sqrt(np.sum(np.square(Lerror),0))
    AsumUp = Asum + WerrorSum
    AsumLow = Asum - LerrorSum
    #Asum = (Asum - np.mean(Asum))/np.mean(Asum)*100
    myFmt = mdates.DateFormatter("%Y-%m-%d")
    plt.plot(Dates,Asum, label='World Reservoirs', marker=".", color='tab:blue')
    plt.plot(Dates,AsumUp, linestyle=":", color='tab:blue', linewidth=0.5)
    plt.plot(Dates,AsumLow, linestyle=":", color='tab:blue', linewidth=0.5)
    plt.fill_between(Dates,AsumUp,AsumLow,color='tab:blue',alpha=0.1)
    plt.gca().xaxis.set_major_formatter(myFmt)


#### South America Reservoirs###########################################################
if contRes == 1:
    IDlist = []
    for ID, Cont, Type in zip(lakeID,lakeContinent,lakeType):
        if Cont == 'South America':
            if Type == 2 or Type == 3:
                IDlist.append(ID)
    
    IDs, Dates, Areas, Werror, Lerror = InterpolateAreas(S1ResultsPath,IDlist)
    Asum = np.sum(Areas,0)
    Asum = (Asum - np.mean(Asum))
    #WerrorSum = np.sum(Werror,0)
    WerrorSum = np.sqrt(np.sum(np.square(Werror),0))
    #LerrorSum = np.sum(Lerror,0)
    LerrorSum = np.sqrt(np.sum(np.square(Lerror),0))
    AsumUp = Asum + WerrorSum
    AsumLow = Asum - LerrorSum
    #Asum = (Asum - np.mean(Asum))/np.mean(Asum)*100
    myFmt = mdates.DateFormatter("%Y-%m-%d")
    plt.plot(Dates,Asum, label='World Reservoirs', marker=".", color='tab:orange')
    plt.plot(Dates,AsumUp, linestyle=":", color='tab:orange', linewidth=0.5)
    plt.plot(Dates,AsumLow, linestyle=":", color='tab:orange', linewidth=0.5)
    plt.fill_between(Dates,AsumUp,AsumLow,color='tab:orange',alpha=0.1)
    plt.gca().xaxis.set_major_formatter(myFmt)

#### Asia Reservoirs###########################################################
if contRes == 1:
    IDlist = []
    for ID, Cont, Type in zip(lakeID,lakeContinent,lakeType):
        if Cont == 'Asia':
            if Type == 2 or Type == 3:
                IDlist.append(ID)
    
    IDs, Dates, Areas = InterpolateAreas(S1ResultsPath,IDlist)
    Asum = np.sum(Areas,0)
    Asum = (Asum - np.mean(Asum))
    #Asum = (Asum - np.mean(Asum))/np.mean(Asum)*100
    myFmt = mdates.DateFormatter("%Y-%m-%d")
    plt.plot(Dates,Asum, label='Asia Reservoirs', marker=".", color='tab:green')
    plt.gca().xaxis.set_major_formatter(myFmt)


#### Africa Reservoirs###########################################################
if contRes == 1:
    IDlist = []
    for ID, Cont, Type in zip(lakeID,lakeContinent,lakeType):
        if Cont == 'Africa':
            if Type == 2 or Type == 3:
                IDlist.append(ID)
    
    IDs, Dates, Areas = InterpolateAreas(S1ResultsPath,IDlist)
    Asum = np.sum(Areas,0)
    Asum = (Asum - np.mean(Asum))
    #Asum = (Asum - np.mean(Asum))/np.mean(Asum)*100
    myFmt = mdates.DateFormatter("%Y-%m-%d")
    plt.plot(Dates,Asum, label='Africa Reservoirs', marker=".", color='tab:red')
    plt.gca().xaxis.set_major_formatter(myFmt)


#### Europe Reservoirs###########################################################
if contRes == 1:
    IDlist = []
    for ID, Cont, Type in zip(lakeID,lakeContinent,lakeType):
        if Cont == 'Europe':
            if Type == 2 or Type == 3:
                IDlist.append(ID)
    
    IDs, Dates, Areas = InterpolateAreas(S1ResultsPath,IDlist)
    Asum = np.sum(Areas,0)
    Asum = (Asum - np.mean(Asum))
    #Asum = (Asum - np.mean(Asum))/np.mean(Asum)*100
    myFmt = mdates.DateFormatter("%Y-%m-%d")
    plt.plot(Dates,Asum, label='Europe Reservoirs', marker=".", color='tab:purple')
    plt.gca().xaxis.set_major_formatter(myFmt)

#### Oceania Reservoirs###########################################################
if contRes == 1:
    IDlist = []
    for ID, Cont, Type in zip(lakeID,lakeContinent,lakeType):
        if Cont == 'Oceania':
            if Type == 2 or Type == 3:
                IDlist.append(ID)
    
    IDs, Dates, Areas = InterpolateAreas(S1ResultsPath,IDlist)
    Asum = np.sum(Areas,0)
    Asum = (Asum - np.mean(Asum))
    #Asum = (Asum - np.mean(Asum))/np.mean(Asum)*100
    myFmt = mdates.DateFormatter("%Y-%m-%d")
    plt.plot(Dates,Asum, label='Oceania Reservoirs', marker=".", color='tab:brown')
    plt.gca().xaxis.set_major_formatter(myFmt)



#### Lakes###########################################################
#### North America Lakes###########################################################
if contLake == 1:
    IDlist = []
    for ID, Cont, Type in zip(lakeID,lakeContinent,lakeType):
        if Cont == 'North America':
            if Type == 1 or Type == 1:
                IDlist.append(ID)
    
    IDs, Dates, Areas = InterpolateAreas(S1ResultsPath,IDlist)
    Asum = np.sum(Areas,0)
    Asum = (Asum - np.mean(Asum))
    #Asum = (Asum - np.mean(Asum))/np.mean(Asum)*100
    myFmt = mdates.DateFormatter("%Y-%m-%d")
    plt.plot(Dates,Asum, label='North America Lakes', marker=".", color='tab:blue')
    plt.gca().xaxis.set_major_formatter(myFmt)


#### South America Lakes###########################################################
if contLake == 1:
    IDlist = []
    for ID, Cont, Type in zip(lakeID,lakeContinent,lakeType):
        if Cont == 'South America':
            if Type == 1 or Type == 1:
                IDlist.append(ID)
    
    IDs, Dates, Areas = InterpolateAreas(S1ResultsPath,IDlist)
    Asum = np.sum(Areas,0)
    Asum = (Asum - np.mean(Asum))
    #Asum = (Asum - np.mean(Asum))/np.mean(Asum)*100
    myFmt = mdates.DateFormatter("%Y-%m-%d")
    plt.plot(Dates,Asum, label='South America Lakes', marker=".", color='tab:orange')
    plt.gca().xaxis.set_major_formatter(myFmt)

#### Asia Lakes###########################################################
if contLake == 1:
    IDlist = []
    for ID, Cont, Type in zip(lakeID,lakeContinent,lakeType):
        if Cont == 'Asia':
            if Type == 1 or Type == 1:
                IDlist.append(ID)
    
    IDs, Dates, Areas = InterpolateAreas(S1ResultsPath,IDlist)
    Asum = np.sum(Areas,0)
    Asum = (Asum - np.mean(Asum))
    #Asum = (Asum - np.mean(Asum))/np.mean(Asum)*100
    myFmt = mdates.DateFormatter("%Y-%m-%d")
    plt.plot(Dates,Asum, label='Asia Lakes', marker="." ,color='tab:green')
    plt.gca().xaxis.set_major_formatter(myFmt)


#### Africa Lakes###########################################################
if contLake == 1:
    IDlist = []
    for ID, Cont, Type in zip(lakeID,lakeContinent,lakeType):
        if Cont == 'Africa':
            if Type == 1 or Type == 1:
                IDlist.append(ID)
    
    IDs, Dates, Areas = InterpolateAreas(S1ResultsPath,IDlist)
    Asum = np.sum(Areas,0)
    Asum = (Asum - np.mean(Asum))
    #Asum = (Asum - np.mean(Asum))/np.mean(Asum)*100
    myFmt = mdates.DateFormatter("%Y-%m-%d")
    plt.plot(Dates,Asum, label='Africa Lakes', marker=".",color='tab:red')
    plt.gca().xaxis.set_major_formatter(myFmt)


#### Europe Lakes###########################################################
if contLake == 1:
    IDlist = []
    for ID, Cont, Type in zip(lakeID,lakeContinent,lakeType):
        if Cont == 'Europe':
            if Type == 1 or Type == 1:
                IDlist.append(ID)
    
    IDs, Dates, Areas = InterpolateAreas(S1ResultsPath,IDlist)
    Asum = np.sum(Areas,0)
    Asum = (Asum - np.mean(Asum))
    #Asum = (Asum - np.mean(Asum))/np.mean(Asum)*100
    myFmt = mdates.DateFormatter("%Y-%m-%d")
    plt.plot(Dates,Asum, label='Europe Lakes', marker=".",color='tab:purple')
    plt.gca().xaxis.set_major_formatter(myFmt)


#### Oceania Lakes###########################################################
if contLake == 1:
    IDlist = []
    for ID, Cont, Type in zip(lakeID,lakeContinent,lakeType):
        if Cont == 'Oceania':
            if Type == 1 or Type == 1:
                IDlist.append(ID)
    
    IDs, Dates, Areas = InterpolateAreas(S1ResultsPath,IDlist)
    Asum = np.sum(Areas,0)
    Asum = (Asum - np.mean(Asum))
    #Asum = (Asum - np.mean(Asum))/np.mean(Asum)*100
    myFmt = mdates.DateFormatter("%Y-%m-%d")
    plt.plot(Dates,Asum, label='Oceania Lakes', marker=".",color='tab:brown')
    plt.gca().xaxis.set_major_formatter(myFmt)
    
    
years = mdates.YearLocator()  
months = mdates.MonthLocator()  
years_fmt = mdates.DateFormatter('%Y')

plt.gca().xaxis.set_major_formatter(years_fmt)
plt.gca().xaxis.set_major_locator(years)
plt.gca().xaxis.set_minor_locator(months)
plt.gca().set_xlim(datetime.date(2017,1,1),datetime.date(2020,1,1))

if PlotType == 0:
    plt.gca().set_ylabel('Total Water Surface Area $\mathregular{km^{2}}$', fontsize = 16) 
    plt.title('World Lake and Reservoir Surface Area')
    plt.gca().set_ylim(0,300000)
elif PlotType == 1:
    plt.gca().set_ylabel('Water Surface Area Anomalies $\mathregular{km^{2}}$', fontsize = 16)
    plt.title('World Lake and Reservoir Surface Area Anomaly')
elif PlotType == 2:
    plt.gca().set_ylabel('Water Surface Area Anomalies [%]', fontsize = 16)
    plt.title('World Lake and Reservoir Surface Area Anomaly')
    plt.gca().set_ylim(-4,4)


plt.gca().format_xdata = mdates.DateFormatter('%Y-%m-%d')
plt.gca().format_ydata = lambda x: '$%1.2f' % x  # format the price.
plt.gca().grid(True)
leg = plt.gca().legend(frameon=False, loc='upper left', ncol=1)


