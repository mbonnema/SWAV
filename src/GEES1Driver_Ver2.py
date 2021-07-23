#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 11:49:53 2020

@author: mbonnema
"""

from Sentinel1LakeArea_Ver2 import GetS1ResTimeSeries
from writeS1ToFile_Ver2 import writeS1ToFile
from RunS1TimeSeries_Ver2 import RunS1TimeSeries
import os
import signal

class TimeoutException(Exception):   # Custom exception class
    pass

def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException
signal.signal(signal.SIGALRM, timeout_handler)

import ee
ee.Initialize()

outDir = './Results/World_Ver2/'
lakes = ee.FeatureCollection('users/matthewbonnema/HydroLAKES')

files = os.listdir(outDir)

largeLakes = lakes.filter(ee.Filter.gte('Lake_area',100)) \
    .filter(ee.Filter.lte('Lake_area',1000)) \
    
lakeID = largeLakes.aggregate_array('system:index').getInfo()
startIndex = lakeID.index('002300000000000002d6')
lakeID = lakeID[startIndex+1:]


for ID in lakeID:
    ee.Initialize()
    signal.alarm(2000)
    if ID+'.txt' in files:
        print(ID + '\tResults file already in output directory')
        continue
    
    try:
        lake = ee.Feature(largeLakes.filter(ee.Filter.eq('system:index',ee.String(ID))).first())
        print(ID + "\t" + ee.Feature(lake).get('Lake_name').getInfo())
        roi = lake.geometry()
        results, E = RunS1TimeSeries(roi)
        writeS1ToFile(ID, results, E, outDir)
    except Exception as e:
        print(ID + "\t" + ee.Feature(lake).get('Lake_name').getInfo() + '\tended in error: ' + str(e))
        continue
    else:
        signal.alarm(0)


