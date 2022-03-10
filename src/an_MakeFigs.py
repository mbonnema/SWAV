#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 09:16:31 2021

@author: mbonnema
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.lines as mlines
import matplotlib.colors as colors
import matplotlib.ticker as ticker
from matplotlib import cm
import datetime
import pandas as pd
import geopandas as geo
import numpy as np
import contextily as ctx
from InterpS1 import InterpS1
import scipy
from shapely.geometry import shape
from SumArea import SumArea
from SumArea import SumAreaSq
from Smooth import Smooth
import ee
ee.Initialize()

def add_basemap(ax, zoom, url='http://tile.stamen.com/terrain/tileZ/tileX/tileY.png'):
    xmin, xmax, ymin, ymax = ax.axis()
    basemap, extent = ctx.bounds2img(xmin, ymin, xmax, ymax, zoom=zoom)
    ax.imshow(basemap, extent=extent, interpolation='bilinear')
    # restore original x/y limits
    ax.axis((xmin, xmax, ymin, ymax))
    
    
#--Figure 1a-------------------------------------------------------------------
def Fig1a(lat,lon,Ltype,A_d):
    area = A_d
    fig = plt.figure(figsize=(8,5), dpi=300)
    ax = fig.add_subplot()

    ax.set_aspect('equal')
    world = geo.read_file(geo.datasets.get_path('naturalearth_lowres'))
    worldPlot=world.plot(ax=ax, color='white', edgecolor='black', linewidth=0.5)
    Lakesdf = pd.DataFrame(
        {'LakeType': Ltype,
         'Latitude': lat,
         'Longitude': lon})
    Lakesgdf = geo.GeoDataFrame(
        Lakesdf, geometry=geo.points_from_xy(Lakesdf.Longitude, Lakesdf.Latitude))
    
    colorMapmax = []
    for t in Ltype:
        if t == 2:
            colorMapmax.append('#ff0000')
        elif t == 1:
            colorMapmax.append('#0000ff')
                               
    markerSize = []
    for a in area:
        if a < 10:
            markerSize.append(0.1)
        elif a < 100 and a >= 10:
            markerSize.append(1)
        elif a < 1000 and a >= 100:
            markerSize.append(5)
        elif a < 10000 and a >=1000:
            markerSize.append(10)
        elif a >= 10000:
            markerSize.append(20)
    
    LakePlot = Lakesgdf.plot(ax=ax, c=colorMapmax, markersize=markerSize, linewidths=0, marker='o')
    BlueLake = mlines.Line2D([], [], color='blue', marker='o',markersize=3, label='Lakes', linewidth = 0)
    RedRes = mlines.Line2D([], [], color='Red', marker='o',markersize=3, label='Reservoirs', linewidth = 0)
    lakesize0 = mlines.Line2D([], [], color='grey', marker='o',markersize=np.sqrt(0.1), label='1 $\mathregular{km^{2}}$', linewidth = 0)
    lakesize1 = mlines.Line2D([], [], color='grey', marker='o',markersize=np.sqrt(1), label='10 $\mathregular{km^{2}}$', linewidth = 0)
    lakesize2 = mlines.Line2D([], [], color='grey', marker='o',markersize=np.sqrt(5), label='100 $\mathregular{km^{2}}$', linewidth = 0)
    lakesize3 = mlines.Line2D([], [], color='grey', marker='o',markersize=np.sqrt(10), label='1000 $\mathregular{km^{2}}$', linewidth = 0)
    lakesize4 = mlines.Line2D([], [], color='grey', marker='o',markersize=np.sqrt(20), label='>10000 $\mathregular{km^{2}}$', linewidth = 0)
    plt.legend(handles=[BlueLake,RedRes,lakesize0,lakesize1,lakesize2,lakesize3,lakesize4], loc="lower left", fontsize=8)
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.ylim([-60,90])
    plt.xlim([-180,180])
    plt.show()

#--Figure 1b------------------------------------------------------------------- 
def Fig1b(lat, lon, Amin, Amax, A_d, Ltype):
    area = A_d
    markerScale = 1
    fig = plt.figure(figsize=(8,5), dpi=300)
    ax = fig.add_subplot()

    ax.set_aspect('equal')
    world = geo.read_file(geo.datasets.get_path('naturalearth_lowres'))
    worldPlot=world.plot(ax=ax, color='white', edgecolor='black', linewidth=0.5)
    states = geo.read_file('MapData/usa-states-census-2014.shp')
    statePlot=states.plot(ax=ax, color='white', edgecolor='black', linewidth=0.5)
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
        markerSizemin.append(a*markerScale)
        #markerSizemin.append((a/markerScale)**3)
    
    
    colorMapmax = []
    for t in Ltype:
        if t == 2:
            colorMapmax.append('#ff0000')
        elif t == 1:
            colorMapmax.append('#0000ff')
    markerSizemax = []
    for a in Amax:
        markerSizemax.append(a*markerScale)
        #markerSizemax.append((a/markerScale)**3)
    
    LakePlotmax = Lakesgdf.plot(ax=ax, c=colorMapmax, markersize=markerSizemax, marker='.', linewidth=1.5)
    LakePlotmin = Lakesgdf.plot(ax=ax, c=colorMapmin, markersize=markerSizemin, marker='.')
    BlueLake = mlines.Line2D([], [], color='blue', marker='o',markersize=3, label='Lakes', linewidth = 0)
    RedRes = mlines.Line2D([], [], color='Red', marker='o',markersize=3, label='Reservoirs', linewidth = 0)
    lakesize0 = mlines.Line2D([], [], color='grey', marker='o',markersize=np.sqrt(1), label='1 $\mathregular{km^{2}}$', linewidth = 0)
    lakesize1 = mlines.Line2D([], [], color='grey', marker='o',markersize=np.sqrt(5), label='5 $\mathregular{km^{2}}$', linewidth = 0)
    lakesize2 = mlines.Line2D([], [], color='grey', marker='o',markersize=np.sqrt(10), label='10 $\mathregular{km^{2}}$', linewidth = 0)
    lakesize3 = mlines.Line2D([], [], color='grey', marker='o',markersize=np.sqrt(20), label='20 $\mathregular{km^{2}}$', linewidth = 0)
    lakesize_blank = mlines.Line2D([], [], color='white', marker='o',markersize=0, label='', linewidth = 0)
    lakesize4 = mlines.Line2D([], [], color='grey', marker='o',markersize=np.sqrt(100), label='100 $\mathregular{km^{2}}$', linewidth = 0)
    plt.legend(handles=[BlueLake,RedRes,lakesize0,lakesize1,lakesize2,lakesize3,lakesize_blank,lakesize4, lakesize_blank], loc="lower left", fontsize=4)
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.ylim([32,50])
    plt.xlim([-125,-115])
    plt.show()
    
#--Figure 3a------------------------------------------------------------------- 
def Fig3a(D_int,A_int,WE_int,LE_int,Type, D_int_jrc, A_int_jrc):
    Asum,Dates = SumArea(A_int,D_int)
    Asum_jrc_raw, Dates_jrc = SumArea(A_int_jrc,D_int_jrc)
    Asum_jrc = []
    for a in Asum_jrc_raw:
        a = float(a)
        Asum_jrc.append(a)
    Asum_jrc = np.array(Asum_jrc)
    #WEsum,Dates = SumArea(WE_int,D_int)
    #LEsum,Dates = SumArea(LE_int,D_int)
    #AsumUp = np.array(Asum) + np.array(WEsum)
    #AsumDown = np.array(Asum) - np.array(LEsum)
    formatDates = []
    for d in Dates:
        formatDates.append(datetime.datetime.fromtimestamp(d/1000))
    lake_ids = []
    res_ids = []
    for key in Type:
        if Type[key] == 1:
            lake_ids.append(key)
        else: 
            res_ids.append(key)
    
    D_int_lake = {k: D_int[k] for k in D_int.keys() & lake_ids }
    D_int_res = {k: D_int[k] for k in D_int.keys() & res_ids }
    A_int_lake = {k: A_int[k] for k in A_int.keys() & lake_ids }
    A_int_res = {k: A_int[k] for k in A_int.keys() & res_ids }
    #WE_int_lake = {k: WE_int[k] for k in WE_int.keys() & lake_ids }
    #WE_int_res = {k: WE_int[k] for k in WE_int.keys() & res_ids }
    #LE_int_lake = {k: LE_int[k] for k in LE_int.keys() & lake_ids }
    #LE_int_res = {k: LE_int[k] for k in LE_int.keys() & res_ids }
    Asum_lake, Dates_lake = SumArea(A_int_lake,D_int_lake)
    #WEsum_lake, Dates_lake = SumArea(WE_int_lake,D_int_lake)
    #LEsum_lake, Dates_lake = SumArea(LE_int_lake,D_int_lake)
    Asum_res, Dates_res = SumArea(A_int_res,D_int_res)
    #WEsum_res, Dates_res = SumArea(WE_int_res,D_int_res)
    #LEsum_res, Dates_res = SumArea(LE_int_res,D_int_res)
    
    print(np.mean(Asum_res))
    print(np.mean(Asum_lake))
    '''
    AsumUp_lake = np.array(Asum_lake) + np.array(WEsum_lake)
    AsumDown_lake = np.array(Asum_lake) - np.array(LEsum_lake)
    AsumUp_res = np.array(Asum_res) + np.array(WEsum_res)
    AsumDown_res = np.array(Asum_res) - np.array(LEsum_res)
    '''
    
    fig = plt.figure(figsize=(4,2), dpi=300)
    ax = fig.add_subplot()
    '''
    ax.plot(formatDates,Asum,c='purple',label='All SWB',linewidth=1)
    #plt.fill_between(formatDates,AsumUp,AsumDown,color='purple',alpha=0.1)
    ax.plot(formatDates,Asum_lake,c='blue',label='Natural Lakes',linewidth=1)
    #plt.fill_between(formatDates,AsumUp_lake,AsumDown_lake,color='blue',alpha=0.1)
    ax.plot(formatDates,Asum_res,c='red',label='Artificial Reservoirs',linewidth=1)
    #plt.fill_between(formatDates,AsumUp_res,AsumDown_res,color='red',alpha=0.1)
    ax.plot(formatDates,Asum_jrc,c='black',label='Lakes > 10,000 km2',linewidth=1)
    '''
    A1 = Asum_jrc
    A2 = Asum_jrc + Asum_lake
    A3 = A2 + Asum_res
    plt.fill_between(formatDates,A1,color='black',alpha=0.3)
    plt.fill_between(formatDates,A2, A1, color='blue',alpha=0.3)
    plt.fill_between(formatDates,A3, A2, color='red',alpha=0.3)
    plt.gca().set_ylabel('Total Water Surface Area $\mathregular{km^{2}}$', fontsize = 12) 
    plt.title('World Lake and Reservoir Surface Area')
    plt.gca().set_ylim(0,2500000)
    
    years = mdates.YearLocator()  
    months = mdates.MonthLocator()  
    years_fmt = mdates.DateFormatter('%Y')
    
    plt.gca().xaxis.set_major_formatter(years_fmt)
    plt.gca().xaxis.set_major_locator(years)
    plt.gca().xaxis.set_minor_locator(months)
    plt.gca().set_xlim(datetime.date(2017,1,1),datetime.date(2020,1,1))
    plt.gca().format_xdata = mdates.DateFormatter('%Y-%m-%d')
    #plt.gca().format_ydata = lambda x: '$%0.9f' % x  # format the price.
    #plt.gca().y_labels = ax.get_yticks()
    #plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1e'))
    plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0), useMathText=True)
    #plt.gca().grid(True)
    #plt.gca().legend(frameon=False, loc='upper right', ncol=1)
    
    
#--Figure 3b------------------------------------------------------------------- 
def Fig3b(D_int,A_int,WE_int,LE_int,Type):
    Asum,Dates = SumArea(A_int,D_int)
    Avg = np.mean(Asum)
    Asum = np.array(Asum) - Avg
    WEsum,Dates = SumAreaSq(WE_int,D_int)
    LEsum,Dates = SumAreaSq(LE_int,D_int)
    
    AsumUp = Smooth(np.array(Asum) + np.array(WEsum))
    AsumDown = Smooth(np.array(Asum) - np.array(LEsum))
    Asum = Smooth(Asum)
    
    formatDates = []
    for d in Dates:
        formatDates.append(datetime.datetime.fromtimestamp(d/1000))
    lake_ids = []
    res_ids = []
    for key in Type:
        if Type[key] == 1:
            lake_ids.append(key)
        else: 
            res_ids.append(key)
    
    D_int_lake = {k: D_int[k] for k in D_int.keys() & lake_ids }
    D_int_res = {k: D_int[k] for k in D_int.keys() & res_ids }
    A_int_lake = {k: A_int[k] for k in A_int.keys() & lake_ids }
    A_int_res = {k: A_int[k] for k in A_int.keys() & res_ids }
    WE_int_lake = {k: WE_int[k] for k in WE_int.keys() & lake_ids }
    WE_int_res = {k: WE_int[k] for k in WE_int.keys() & res_ids }
    LE_int_lake = {k: LE_int[k] for k in LE_int.keys() & lake_ids }
    LE_int_res = {k: LE_int[k] for k in LE_int.keys() & res_ids }
    Asum_lake, Dates_lake = SumArea(A_int_lake,D_int_lake)
    WEsum_lake, Dates_lake = SumAreaSq(WE_int_lake,D_int_lake)
    LEsum_lake, Dates_lake = SumAreaSq(LE_int_lake,D_int_lake)
    Asum_res, Dates_res = SumArea(A_int_res,D_int_res)
    WEsum_res, Dates_res = SumAreaSq(WE_int_res,D_int_res)
    LEsum_res, Dates_res = SumAreaSq(LE_int_res,D_int_res)
    
    Avg_lake = np.mean(Asum_lake)
    Asum_lake = np.array(Asum_lake) - Avg_lake
    Avg_res = np.mean(Asum_res)
    Asum_res = np.array(Asum_res) - Avg_res
    
    AsumUp_lake = Smooth(np.array(Asum_lake) + np.array(WEsum_lake))
    AsumDown_lake = Smooth(np.array(Asum_lake) - np.array(LEsum_lake))
    AsumUp_res = Smooth(np.array(Asum_res) + np.array(WEsum_res))
    AsumDown_res = Smooth(np.array(Asum_res) - np.array(LEsum_res))
    Asum_lake = Smooth(Asum_lake)
    Asum_res = Smooth(Asum_res)
    fig = plt.figure(figsize=(6,3), dpi=200)
    ax = fig.add_subplot()
    ax.plot(formatDates,Asum,c='purple',label='All SWB',linewidth=1)
    #plt.fill_between(formatDates,AsumUp,AsumDown,color='purple',alpha=0.1)
    ax.plot(formatDates,Asum_lake,c='blue',label='Natural Lakes',linewidth=1)
    #plt.fill_between(formatDates,AsumUp_lake,AsumDown_lake,color='blue',alpha=0.1)
    ax.plot(formatDates,Asum_res,c='red',label='Artificial Reservoirs',linewidth=1)
    #plt.fill_between(formatDates,AsumUp_res,AsumDown_res,color='red',alpha=0.1)
    
    plt.gca().set_ylabel('Water Surface Area Anomalies $\mathregular{km^{2}}$', fontsize = 12) 
    plt.title('Global Lake and Reservoir Surface Area Anomalies')
    plt.gca().set_ylim(-15000,15000)
    
    years = mdates.YearLocator()  
    months = mdates.MonthLocator()  
    years_fmt = mdates.DateFormatter('%Y')
    
    plt.gca().xaxis.set_major_formatter(years_fmt)
    plt.gca().xaxis.set_major_locator(years)
    plt.gca().xaxis.set_minor_locator(months)
    plt.gca().set_xlim(datetime.date(2017,1,1),datetime.date(2020,1,1))
    plt.gca().format_xdata = mdates.DateFormatter('%Y-%m-%d')
    plt.gca().format_ydata = lambda x: '$%1.2f' % x  # format the price.
    plt.gca().grid(True)
    plt.gca().legend(frameon=False, loc='lower right', ncol=1,fontsize = 12)
    
#--Figure 3c------------------------------------------------------------------- 
def Fig3c(D_int,A_int,WE_int,LE_int,Type):
    Asum,Dates = SumArea(A_int,D_int)
    Avg = np.mean(Asum)
    Asum = np.array(Asum) - Avg
    WEsum,Dates = SumAreaSq(WE_int,D_int)
    LEsum,Dates = SumAreaSq(LE_int,D_int)
    
    AsumUp = Smooth((np.array(Asum) + np.array(WEsum))/Avg*100)
    AsumDown = Smooth((np.array(Asum) - np.array(LEsum))/Avg*100)
    Asum = Smooth(Asum/Avg*100)
    
    formatDates = []
    for d in Dates:
        formatDates.append(datetime.datetime.fromtimestamp(d/1000))
    lake_ids = []
    res_ids = []
    for key in Type:
        if Type[key] == 1:
            lake_ids.append(key)
        else: 
            res_ids.append(key)
    
    D_int_lake = {k: D_int[k] for k in D_int.keys() & lake_ids }
    D_int_res = {k: D_int[k] for k in D_int.keys() & res_ids }
    A_int_lake = {k: A_int[k] for k in A_int.keys() & lake_ids }
    A_int_res = {k: A_int[k] for k in A_int.keys() & res_ids }
    WE_int_lake = {k: WE_int[k] for k in WE_int.keys() & lake_ids }
    WE_int_res = {k: WE_int[k] for k in WE_int.keys() & res_ids }
    LE_int_lake = {k: LE_int[k] for k in LE_int.keys() & lake_ids }
    LE_int_res = {k: LE_int[k] for k in LE_int.keys() & res_ids }
    Asum_lake, Dates_lake = SumArea(A_int_lake,D_int_lake)
    WEsum_lake, Dates_lake = SumAreaSq(WE_int_lake,D_int_lake)
    LEsum_lake, Dates_lake = SumAreaSq(LE_int_lake,D_int_lake)
    Asum_res, Dates_res = SumArea(A_int_res,D_int_res)
    WEsum_res, Dates_res = SumAreaSq(WE_int_res,D_int_res)
    LEsum_res, Dates_res = SumAreaSq(LE_int_res,D_int_res)
    
    Avg_lake = np.mean(Asum_lake)
    Asum_lake = np.array(Asum_lake) - Avg_lake
    Avg_res = np.mean(Asum_res)
    Asum_res = np.array(Asum_res) - Avg_res
    
    AsumUp_lake = Smooth((np.array(Asum_lake) + np.array(WEsum_lake))/Avg_lake*100)
    AsumDown_lake = Smooth((np.array(Asum_lake) - np.array(LEsum_lake))/Avg_lake*100)
    AsumUp_res = Smooth((np.array(Asum_res) + np.array(WEsum_res))/Avg_res*100)
    AsumDown_res = Smooth((np.array(Asum_res) - np.array(LEsum_res))/Avg_res*100)
    
    Asum_lake = Smooth(Asum_lake/Avg_lake*100)
    Asum_res = Smooth(Asum_res/Avg_res*100)
    
    fig = plt.figure(figsize=(6,3), dpi=200)
    ax = fig.add_subplot()
    ax.plot(formatDates,Asum,c='purple',label='All SWB',linewidth=1)
    #plt.fill_between(formatDates,AsumUp,AsumDown,color='purple',alpha=0.1)
    ax.plot(formatDates,Asum_lake,c='blue',label='Natural Lakes',linewidth=1)
    #plt.fill_between(formatDates,AsumUp_lake,AsumDown_lake,color='blue',alpha=0.1)
    ax.plot(formatDates,Asum_res,c='red',label='Artificial Reservoirs',linewidth=1)
    #plt.fill_between(formatDates,AsumUp_res,AsumDown_res,color='red',alpha=0.1)
    
    plt.gca().set_ylabel('Relative Water Surface Area Anomalies [%]', fontsize = 12) 
    plt.title('Global Lake and Reservoir Surface Area Anomalies')
    plt.gca().set_ylim(-4,4)
    
    years = mdates.YearLocator()  
    months = mdates.MonthLocator()  
    years_fmt = mdates.DateFormatter('%Y')
    
    plt.gca().xaxis.set_major_formatter(years_fmt)
    plt.gca().xaxis.set_major_locator(years)
    plt.gca().xaxis.set_minor_locator(months)
    plt.gca().set_xlim(datetime.date(2017,1,1),datetime.date(2020,1,1))
    plt.gca().format_xdata = mdates.DateFormatter('%Y-%m-%d')
    plt.gca().format_ydata = lambda x: '$%1.2f' % x  # format the price.
    plt.gca().grid(True)
    plt.gca().legend(frameon=False, loc='lower right', ncol=1,fontsize = 12)
    
    
    
#--Figure 3b------------------------------------------------------------------- 
def Fig3b_alt(D_int,A_int,LakesByBasin):
    fig = plt.figure(figsize=(8,5), dpi=300)
    ax = fig.add_subplot()

    ax.set_aspect('equal')
    world = geo.read_file(geo.datasets.get_path('naturalearth_lowres'))
    worldPlot=world.plot(ax=ax, color='white', edgecolor='black', linewidth=0.5)
    
    cmap = cm.get_cmap('Blues', 256)
    basins = ee.FeatureCollection("WWF/HydroSHEDS/v1/Basins/hybas_2")
    basinNumbers = basins.aggregate_array('PFAF_ID').getInfo()
    lakes = ee.FeatureCollection('users/matthewbonnema/HydroLAKES')
    lakes = lakes.filter(ee.Filter.gte('Lake_area',1))
    PolyList = []
    AV = []
    #basinNumbers = basinNumbers[0:2]
    #print(basinNumbers[-1])
    for N in basinNumbers:
        print('Loading geometry for basin: '+str(N))
        b = ee.Feature(basins.filter(ee.Filter.eq('PFAF_ID',N)).first())
        Geo= b.geometry().simplify(100)
        Geometry = Geo.getInfo()
        geo_shape = shape(Geometry)
        PolyList.append(geo_shape)
        print('\tGeometry loaded')
        print('Aggregating lake area for basin: '+str(N))
        lakeID = LakesByBasin[str(N)]
        #basinLakes = lakes.filterBounds(Geo)
        #lakeID = basinLakes.aggregate_array('Hylak_id').getInfo()
        A = {k: A_int[k] for k in A_int.keys() & lakeID }
        D = {k: D_int[k] for k in D_int.keys() & lakeID }
        Asum,Dates = SumArea(A,D)
        Asum = np.array(Asum)
        Amax = np.max(Asum)
        Amin = np.min(Asum)
        Avar = Amax-Amin
        AV.append(Avar)
        print('\tFinished aggregation')
    maxVar = np.max(AV)
    C = np.array(AV)/maxVar
    #print(C)
    n = len(PolyList)
    i = 0
    for P,c in zip(PolyList,C):
        i = i+1
        print('Drawing shape number '+str(i)+'/'+str(n))
        c = float(c)
        try:
            if P.geom_type == 'Polygon':
                plt.fill(*P.exterior.xy,c=cmap(c))
            elif P.geom_type == 'MultiPolygon':
                for geom in P.geoms:
                    plt.fill(*geom.exterior.xy,c=cmap(c))
            print('\tFinished drawing')
        except:
            print('\tFailed to draw polygon')
    
    norm = colors.Normalize(vmin=0, vmax=maxVar, clip=False)
    plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.ylim([-60,90])
    plt.xlim([-180,180])
    plt.show()

#--Figure 3c------------------------------------------------------------------- 
def Fig3c_alt(D_int,A_int,LakesByBasin):

    fig = plt.figure(figsize=(8,5), dpi=300)
    ax = fig.add_subplot()

    ax.set_aspect('equal')
    world = geo.read_file(geo.datasets.get_path('naturalearth_lowres'))
    worldPlot=world.plot(ax=ax, color='white', edgecolor='black', linewidth=0.5)
    
    cmap = cm.get_cmap('Blues', 256)
    basins = ee.FeatureCollection("WWF/HydroSHEDS/v1/Basins/hybas_2")
    basinNumbers = basins.aggregate_array('PFAF_ID').getInfo()
    lakes = ee.FeatureCollection('users/matthewbonnema/HydroLAKES')
    lakes = lakes.filter(ee.Filter.gte('Lake_area',1))
    PolyList = []
    AV = []
    #basinNumbers = basinNumbers[0:2]
    #print(basinNumbers[-1])
    for N in basinNumbers:
        print('Loading geometry for basin: '+str(N))
        b = ee.Feature(basins.filter(ee.Filter.eq('PFAF_ID',N)).first())
        Geo= b.geometry().simplify(100)
        Geometry = Geo.getInfo()
        geo_shape = shape(Geometry)
        PolyList.append(geo_shape)
        print('\tGeometry loaded')
        print('Aggregating lake area for basin: '+str(N))
        lakeID = LakesByBasin[str(N)]
        #basinLakes = lakes.filterBounds(Geo)
        #lakeID = basinLakes.aggregate_array('Hylak_id').getInfo()
        A = {k: A_int[k] for k in A_int.keys() & lakeID }
        D = {k: D_int[k] for k in D_int.keys() & lakeID }
        Asum,Dates = SumArea(A,D)
        Asum = np.array(Asum)
        Amax = np.max(Asum)
        Amin = np.min(Asum)
        Avar = Amax-Amin
        Amean = np.mean(Asum)
        AvarP = Avar/Amean*100
        AV.append(AvarP)
        print('\tFinished aggregation')
    maxVar = np.max(AV)
    C = np.array(AV)/maxVar
    #print(C)
    n = len(PolyList)
    i = 0
    for P,c in zip(PolyList,C):
        i = i+1
        print('Drawing shape number '+str(i)+'/'+str(n))
        c = float(c)
        try:
            if P.geom_type == 'Polygon':
                plt.fill(*P.exterior.xy,c=cmap(c),alpha=0.8)
            elif P.geom_type == 'MultiPolygon':
                for geom in P.geoms:
                    plt.fill(*geom.exterior.xy,c=cmap(c),alpha=0.8)
            print('\tFinished drawing')
        except:
            print('\tFailed to draw polygon')
    
    norm = colors.Normalize(vmin=0, vmax=maxVar, clip=False)
    plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.ylim([-60,90])
    plt.xlim([-180,180])
    plt.show()
#--Figure 4a-------------------------------------------------------------------     
def Fig4a(Avp, A_d):
    Avp_subdiv = []
    labels = []
    positions = []
    sub = 2
    n_sub = range(sub*4)
    for n in n_sub:
        Avp_sel = Avp[np.array([A_d>=10**(n/2),A_d<10**((n+1)/2)]).all(axis=0)]
        Avp_subdiv.append(Avp_sel)
        positions.append(np.mean([10**(n/2),10**((n+1)/2)]))
        #positions.append(10**(n/2))
        if n % 2 == 0:
            labels.append('$10^{'+str(n//2)+'}$')
        else:
            labels.append('$10^{'+str(n)+'/2}$')
    Avp_subdiv.append(Avp[A_d>=10000])
    labels.append('>$10^4$')
    positions.append(np.mean([10**(8/2),10**(9/2)]))
    w = 0.42
    width = lambda p, w: 10**(np.log10(p)+w/2.)-10**(np.log10(p)-w/2.)
    widths = width(positions,w)
    #widths[-1] = width(positions[-1],w*1.4)
    fig = plt.figure(figsize=(8,5), dpi=300)
    ax = fig.add_subplot()
    ax.boxplot(Avp_subdiv,showfliers=False,positions=positions,widths=widths)
    ax.set_ylabel('Relative Water Surface Area Variability [%]', fontsize = 12) 
    ax.set_xlabel('Nominal Surface Area $\mathregular{km^{2}}$', fontsize = 12) 
    plt.title('Global SWB Area Variability')
    #ax.boxplot(Avp_subdiv,showfliers=False,labels=labels,widths=0.7)
    ax.set_xscale('log')
    ax.minorticks_off()

#--Figure 4b-------------------------------------------------------------------         
def Fig4b(Avp, A_d, Ltype):
    Avp_lake = Avp[Ltype==1]
    Avp_res = Avp[Ltype==2]
    A_d_lake = A_d[Ltype==1]
    A_d_res = A_d[Ltype==2]
    Avp_subdiv_lake = []
    Avp_subdiv_res= []
    labels = []
    positionsl = []
    positionsr = []
    sub = 2
    n_sub = range(sub*4)
    for n in n_sub:
        Avp_sel_l = Avp_lake[np.array([A_d_lake>=10**(n/2),A_d_lake<10**((n+1)/2)]).all(axis=0)]
        Avp_sel_r = Avp_res[np.array([A_d_res>=10**(n/2),A_d_res<10**((n+1)/2)]).all(axis=0)]
        #t,p = scipy.stats.ttest_ind(Avp_sel_l ,Avp_sel_r, equal_var=0)
        #print(n/2,t,p)
        Avp_subdiv_lake.append(Avp_sel_l)
        Avp_subdiv_res.append(Avp_sel_r)
        '''
        positionsl.append(np.mean([np.mean([10**(n/2),10**((n+1)/2)]),10**(n/2)]))
        positionsr.append(np.mean([np.mean([10**(n/2),10**((n+1)/2)]),10**((n+1)/2)]))
        '''
        positionsl.append(np.mean([10**(n/2),10**((n+1)/2)]))
        positionsr.append(np.mean([10**(n/2),10**((n+1)/2)]) - 0.02*np.mean([10**(n/2),10**((n+1)/2)]))
        #positions.append(10**(n/2))
        if n % 2 == 0:
            labels.append('>$10^{'+str(n//2)+'}$')
        else:
            labels.append('>$10^{'+str(n)+'/2}$')
    Avp_subdiv_lake.append(Avp[A_d>=10000])
    #labels.append('>$10^4$')
    positionsl.append(np.mean([10**(8/2),10**(9/2)]))
    w = 0.38
    width = lambda p, w: 10**(np.log10(p)+w/2.)-10**(np.log10(p)-w/2.)
    widthsl = width(positionsl,w)
    widthsr = width(positionsr,w)*0.92
    #widths[-1] = width(positions[-1],w*1.4)
    fig = plt.figure(figsize=(8,5), dpi=300)
    ax = fig.add_subplot()
    bpl = ax.boxplot(Avp_subdiv_lake,showfliers=False,positions=positionsl,widths=widthsl,notch=True)
    bpr = ax.boxplot(Avp_subdiv_res,showfliers=False,positions=positionsr,widths=widthsr,notch=True)
    for element in ['boxes', 'whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(bpl[element], color='blue')
    for element in ['boxes', 'whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(bpr[element], color='red')
    ax.set_ylabel('Relative Water Surface Area Variability [%]', fontsize = 12) 
    ax.set_xlabel('Nominal Surface Area $\mathregular{km^{2}}$', fontsize = 12) 
    plt.title('Global Lake and Reservoir Area Variability')
    ax.set_xscale('log')
    ax.minorticks_off()
    
#--Figure 4c-------------------------------------------------------------------
def Fig4c(Av, A_d, Ltype):
    Av_lake = Av[Ltype==1]
    Av_res = Av[Ltype==2]
    A_d_lake = A_d[Ltype==1]
    A_d_res = A_d[Ltype==2]
    Av_total_lake = []
    Av_total_res= []
    Av_total = []
    positions = []
    sub = 2
    n_sub = range(sub*4)
    for n in n_sub:
        Av_sel_l = Av_lake[np.array([A_d_lake>=10**(n/2),A_d_lake<10**((n+1)/2)]).all(axis=0)]
        Av_sel_r = Av_res[np.array([A_d_res>=10**(n/2),A_d_res<10**((n+1)/2)]).all(axis=0)]
        Av_total_lake.append(np.sum(Av_sel_l))
        Av_total_res.append(np.sum(Av_sel_r))
        Av_total.append(np.sum(Av_sel_l)+np.sum(Av_sel_r))
        positions.append(np.mean([10**(n/2),10**((n+1)/2)]))
    
    Av_total_gt = np.sum(Av[A_d>=10000])
    
    fig = plt.figure(figsize=(8,5), dpi=300)
    ax = fig.add_subplot()
    w = 0.42
    width = lambda p, w: 10**(np.log10(p)+w/2.)-10**(np.log10(p)-w/2.)
    widths = width(positions,w)
    ax.bar(x=positions,height=Av_total_res, width=widths, bottom=Av_total_lake, color='red')
    print(np.sum(Av_total_res))
    positions.append(np.mean([10**(8/2),10**(9/2)]))
    widths = width(positions,w)
    Av_total_lake.append(Av_total_gt)
    ax.bar(x=positions,height=Av_total_lake, width=widths, color='blue')
    print(np.sum(Av_total_lake))
    ax.set_ylabel('Total Surface Area Amplitude $\mathregular{km^{2}}$', fontsize = 12) 
    ax.set_xlabel('Nominal Surface Area $\mathregular{km^{2}}$', fontsize = 12) 
    plt.title('Total Lake and Reservoir Area Amplitude')
    ax.set_xscale('log')
    ax.minorticks_off()