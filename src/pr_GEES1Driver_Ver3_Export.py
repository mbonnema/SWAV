#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 11:49:53 2020

@author: mbonnema
"""

from Sentinel1LakeArea_Ver3_Export import GetS1ResTimeSeries

import ee
ee.Initialize()

lakes = ee.FeatureCollection('users/matthewbonnema/HydroLAKES')

largeLakes = lakes.filter(ee.Filter.gte('Lake_area',1000)) \
    .filter(ee.Filter.lt('Lake_area',10000)) \
    
lakeID = largeLakes.aggregate_array('system:index').getInfo()
nLakes = len(lakeID)
lakeLists = []
tempList = []
groupSize = 1
remainder = nLakes%groupSize
if remainder > 0:
    lastLakes = lakeID[-remainder:]
i = 1
for ID in lakeID:
    tempList.append(ID)
    if i >= groupSize:
        lakeLists.append(tempList)
        tempList = []
        i = 0
    i = i+1
if remainder > 0:
    lakeLists.append(lastLakes)

i = 1
nBatch = len(lakeLists)
lakeLists=lakeLists[i-1:]
for batch in lakeLists:
    print('Starting Batch #'+str(i)+' of '+str(nBatch))
    roiList = []
    for ID in batch:
        lake = ee.Feature(largeLakes.filter(ee.Filter.eq('system:index',ee.String(ID))).first())
        hyLakeID = str(lake.get('Hylak_id').getInfo())
        #print('\tID: ' + hyLakeID)
        roi = ee.Feature(lake.geometry().buffer(500)).set('ID',hyLakeID)
        roiList.append(roi)
    batchFeature = ee.FeatureCollection(roiList)
    outFeature = ee.FeatureCollection(batchFeature.map(GetS1ResTimeSeries,True))
    task = ee.batch.Export.table.toDrive(
        collection = outFeature,
        description = str(i),
        folder = 'S1_1000_10000',
        fileFormat = 'CSV'
        )
    task.start()
    i = i+1
    print('\tTask Exported')


