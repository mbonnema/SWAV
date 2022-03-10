#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
*******************************************************************************
Google Earth Engine Setninel-1 Lake Area

  o Purpose: Estimate surface are of lake from Sentinel-1 SAR date, using 
    Google Earth Engine cloud computing platform
  o Inputs:
      * ROI: Google Earth Engine geometry object describing the region of
        interest
  o Outputs:
      * Results: List containing 4 elements (GEE objects):
          1) List of lake surface areas from ascending passes
          2) List of lake surface areas from descending passes
          3) List of time steps ascoiated with ascending pass surface areas
          4) List of time steps ascoiated with descending pass surface areas
Written by: Matthew Bonnema, matthew.g.bonnema@jpl.nasa.gov
Version 0.3
*******************************************************************************
"""
import ee
ee.Initialize()

def GetS1ResTimeSeries(roi):
    ID = roi.get('ID')
    ROI = roi.geometry()
    ROI_Diff = ROI.difference(roi)
    Date_Start = ee.Date('2017-01-01');
    Date_End = ee.Date('2020-01-01');
    date_interval = ee.Number(1); #month
    angle_threshold_1 = ee.Number(45.4);
    angle_threshold_2 = ee.Number(31.66)
    AreaImg = ee.Image.pixelArea()
    
    #****Get WaterProb Threshold************************************************
    waterProb = ee.Image('JRC/GSW1_1/GlobalSurfaceWater').select('occurrence')
    wProbThresh = ee.Number(ee.Image.constant(0).blend(waterProb).rename('occurrence').reduceRegion(
            reducer = ee.Reducer.max(),
            geometry = ROI,
            scale = 100,
            maxPixels = 6098838800,
            tileScale = 16
            ).get('occurrence'))
    
    waterConfident = waterProb.gte(wProbThresh)
    landConfident = (ee.Image.constant(0).blend(waterProb)).Not().rename('occurrence')
  
    waterConfidentArea = ee.Number(waterConfident.multiply(AreaImg).reduceRegion(
            reducer = ee.Reducer.sum(),
            geometry = ROI,
            scale = 100,
            maxPixels = 6098838800,
            tileScale = 16,
            ).get('occurrence'))

    landConfidentArea = ee.Number(landConfident.multiply(AreaImg).reduceRegion(
            reducer = ee.Reducer.sum(),
            geometry = ROI,
            scale = 100,
            maxPixels = 6098838800,
            tileScale = 16,
            ).get('occurrence'))

    #****Create list of dates for time series********************************************
    n_steps = Date_End.difference(Date_Start,'month').divide(date_interval).round();
    dates = ee.List.sequence(0,n_steps,1);
    def make_datelist(n):
        return(Date_Start.advance(ee.Number(n).multiply(date_interval),'month'))
    dates = dates.map(make_datelist);
  
    #****Filter Edge Pixels**************************************************************
    def maskByAngle(img):
        I = ee.Image(img)
        angle = I.select('angle');
        mask1 = angle.lt(angle_threshold_1);
        mask2 = angle.gt(angle_threshold_2);
        I = I.updateMask(mask1)
        return(I.updateMask(mask2))
  
    #****Make S1 Image Collection********************************************************
    def create_collection(d):
        start = ee.Date(d);
        end = ee.Date(d).advance(date_interval,'month');
        date_range = ee.DateRange(start,end);
        S1 = ee.ImageCollection('COPERNICUS/S1_GRD') \
            .filterDate(date_range) \
            .filterBounds(ROI) \
            .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \
            .filter(ee.Filter.eq('instrumentMode', 'IW'))
        S1 = ee.ImageCollection(ee.Algorithms.If(
            condition = S1.size().gt(0),
            trueCase = S1.map(maskByAngle),
            falseCase = S1
            ))
        S1_median = ee.Image(S1.select('VV').mean()).clip(ROI)
        S1_median = S1_median.set('system:time_start',start.millis())
        S1_median = S1_median.set('Number_of_images',S1.size())
        return(S1_median)
        
    #****Calc ROI Area**********************************************************************
    def calcArea(img):
        I = ee.Image(img)
        area = I.select('VV').lt(99999999).multiply(AreaImg).reduceRegion(
            reducer = ee.Reducer.sum(),
            geometry = ROI,
            scale = 100,
            maxPixels = 6098838800,
            tileScale = 16,
            ).get('VV')
        return(I.set('ROI_area',area))

    #****Apply Filter**********************************************************************
    def focal_median(img):
        I = ee.Image(img)
        #fm = I.select('VV').rename('VV_smooth')
        fm = I.select('VV').focal_median(50,'circle','meters').rename('VV_smooth')
        return(I.addBands(fm))

    #****Make Water Mask****************************************************************
    def MakeWaterMask(img):
        I = ee.Image(img)
        wThresh = ee.Number(I.get('wThresh'))
        waterProb = ee.Image('JRC/GSW1_1/GlobalSurfaceWater').select('occurrence')
        Mask = I.select('VV_smooth').updateMask(waterProb).lt(wThresh).rename('WaterMask')
        Sum = Mask.multiply(AreaImg).reduceRegion(
            reducer = ee.Reducer.sum(),
            geometry = ROI,
            scale = 100,
            maxPixels = 6098838800,
            tileScale = 16
            )
        I = I.set('water_pixels',Sum.get('WaterMask'))
        I = I.set('Water_Area',ee.Number(Sum.get('WaterMask')))
        return I.addBands(Mask)
    #****Round time*********************************************************************
    def makeBackscatterStats(img):
        img = ee.Image(img)
        wMask = img.select('WaterMask')
        vv = img.select('VV_smooth')
        wPixelmean = vv.updateMask(wMask).reduceRegion(
            reducer = ee.Reducer.mean(),
            geometry = ROI,
            scale = 1000,
            maxPixels = 6098838800,
            tileScale = 16
            )
        wPixelStd = vv.updateMask(wMask).reduceRegion(
            reducer = ee.Reducer.stdDev(),
            geometry = ROI,
            scale = 1000,
            maxPixels = 6098838800,
            tileScale = 16
            )
        lPixelmean = vv.updateMask(wMask.Not()).reduceRegion(
            reducer = ee.Reducer.mean(),
            geometry = ROI,
            scale = 1000,
            maxPixels = 6098838800,
            tileScale = 16
            )
        lPixelStd =  vv.updateMask(wMask.Not()).reduceRegion(
            reducer = ee.Reducer.stdDev(),
            geometry = ROI,
            scale = 1000,
            maxPixels = 6098838800,
            tileScale = 16
            )
        inPixelmean = vv.reduceRegion(
            reducer = ee.Reducer.mean(),
            geometry = roi,
            scale = 1000,
            maxPixels = 6098838800,
            tileScale = 16
            )
        inPixelStd = vv.reduceRegion(
            reducer = ee.Reducer.stdDev(),
            geometry = roi,
            scale = 1000,
            maxPixels = 6098838800,
            tileScale = 16
            )
        outPixelmean = vv.reduceRegion(
            reducer = ee.Reducer.mean(),
            geometry = ROI_Diff,
            scale = 1000,
            maxPixels = 6098838800,
            tileScale = 16
            )
        outPixelStd =  vv.updateMask(wMask.Not()).reduceRegion(
            reducer = ee.Reducer.stdDev(),
            geometry = ROI_Diff,
            scale = 300,
            maxPixels = 6098838800,
            tileScale = 16
            )
        img = img.set('wPixelmean',wPixelmean.get('VV_smooth'))
        img = img.set('wPixelStd',wPixelStd.get('VV_smooth'))
        img = img.set('lPixelmean',lPixelmean.get('VV_smooth'))
        img = img.set('lPixelStd',lPixelStd.get('VV_smooth'))
        img = img.set('inPixelmean',inPixelmean.get('VV_smooth'))
        img = img.set('inPixelStd',inPixelStd.get('VV_smooth'))
        img = img.set('outPixelmean',outPixelmean.get('VV_smooth'))
        img = img.set('outPixelStd',outPixelStd.get('VV_smooth'))
        return img
    def makeBackScatterFromJRC(img):
        img = ee.Image(img)
        waterProb = ee.Image('JRC/GSW1_1/GlobalSurfaceWater').select('occurrence')
        waterConfident = waterProb.gte(wProbThresh)
        landConfident = (ee.Image.constant(0).blend(waterProb)).Not()
        vv = img.select('VV_smooth')
        wMean = vv.updateMask(waterConfident).reduceRegion(
            reducer = ee.Reducer.mean(),
            geometry = ROI,
            scale = 100,
            maxPixels = 6098838800,
            tileScale = 16
            )
        wStd = vv.updateMask(waterConfident).reduceRegion(
            reducer = ee.Reducer.stdDev(),
            geometry = ROI,
            scale = 100,
            maxPixels = 6098838800,
            tileScale = 16
            )
        lMean = vv.updateMask(landConfident).reduceRegion(
            reducer = ee.Reducer.mean(),
            geometry = ROI,
            scale = 100,
            maxPixels = 6098838800,
            tileScale = 16
            )
        lStd = vv.updateMask(landConfident).reduceRegion(
            reducer = ee.Reducer.stdDev(),
            geometry = ROI,
            scale = 100,
            maxPixels = 6098838800,
            tileScale = 16
            )
        img = img.set('wMean',wMean.get('VV_smooth')).set('lMean',lMean.get('VV_smooth'))
        img = img.set('wStd',wStd.get('VV_smooth')).set('lStd',lStd.get('VV_smooth'))
        return img
    #****Round time*********************************************************************
    def Roundtime(img):
        I = ee.Image(img)
        time = ee.Number(I.get('system:time_start')).round()
        return(I.set('system:time_start',time))
    #****Caclulate Threshold**************************************************************
    def calcThresh(img):
        img = ee.Image(img)
        wMean = ee.Number(img.get('wMean'))
        wStd = ee.Number(img.get('wStd'))
        lMean = ee.Number(img.get('lMean'))
        lStd = ee.Number(img.get('lStd'))
        x = (lMean.subtract(wMean)).divide(wStd.add(lStd))
        wThresh = wMean.add(wStd.multiply(x))
        return img.set('wThresh',wThresh)
    #****Caclulate Errors*************************************************************
    def calcError(img):
        img = ee.Image(img)
        waterProb = ee.Image('JRC/GSW1_1/GlobalSurfaceWater').select('occurrence')
        waterConfident = waterProb.gte(wProbThresh)
        landConfident = (ee.Image.constant(0).blend(waterProb)).Not()
        vv = img.select('VV_smooth')
        thresh = ee.Number(img.get('wThresh'))
        wError = ee.Number(vv.gt(thresh).updateMask(waterConfident).rename('wError').multiply(AreaImg).reduceRegion(
          reducer = ee.Reducer.sum(),
          geometry = ROI,
          scale = 100,
          maxPixels = 6098838800,
          tileScale = 16
        ).get('wError'))
        lError = ee.Number(vv.lt(thresh).updateMask(landConfident).rename('lError').multiply(AreaImg).reduceRegion(
          reducer = ee.Reducer.sum(),
          geometry = ROI,
          scale = 100,
          maxPixels = 6098838800,
          tileScale = 16
        ).get('lError'))
        #wError = wError.divide(waterConfidentArea.subtract(wError))
        #lError = lError.divide(landConfidentArea.subtract(lError))
        return img.set('wError',wError).set('lError',lError)
    def calcError2(img):
        img = ee.Image(img)
        wError = ee.Number(img.get('wError'))
        lError = ee.Number(img.get('lError'))
        wError = wError.divide(waterConfidentArea.subtract(wError))
        lError = lError.divide(landConfidentArea.subtract(lError))
        return img.set('wError2',wError).set('lError2',lError)
    #****Run Functions******************************************************************
    S1 = ee.ImageCollection(dates.map(create_collection,True))
    S1 = S1.set('wProbThresh',wProbThresh)
    S1 = S1.filter(ee.Filter.gt('Number_of_images',0))
    S1 = S1.map(calcArea)
    S1 = S1.filter(ee.Filter.gt('ROI_area',ee.Number(ROI.area().multiply(0.95))))
    S1 = S1.map(focal_median)
    #S1 = S1.map(Roundtime)
    S1 = S1.map(makeBackScatterFromJRC)
    S1 = S1.filter(ee.Filter.gt('wMean',-9999))
    S1 = S1.filter(ee.Filter.gt('lMean',-9999))
    S1 = S1.filter(ee.Filter.gt('wStd',-9999))
    S1 = S1.filter(ee.Filter.gt('lStd',-9999))
    S1 = S1.map(calcThresh)
    S1 = S1.map(calcError)
    S1 = S1.filter(ee.Filter.lt('wError',9999999999999))
    S1 = S1.filter(ee.Filter.lt('lError',9999999999999))
    S1 = S1.map(calcError2)
    S1 = S1.filter(ee.Filter.lt('wError2',9999999999999))
    S1 = S1.filter(ee.Filter.lt('lError2',9999999999999))
    S1 = S1.map(MakeWaterMask)
    #S1 = S1.map(makeBackscatterStats)
    
    #****Extract Time Series***************************************************************
    def extractTimeSeries(collection):
        WaterArea = ee.Array(collection.aggregate_array('Water_Area')).multiply(0.000001) #Conversion to km^2
        time = ee.Array(collection.aggregate_array('system:time_start'))
        wMean = ee.Array(collection.aggregate_array('wMean'))
        wStd = ee.Array(collection.aggregate_array('wStd'))
        lMean = ee.Array(collection.aggregate_array('lMean'))
        lStd = ee.Array(collection.aggregate_array('lStd'))
        wProbThresh = collection.get('wProbThresh')
        ROIArea = ee.Array(collection.aggregate_array('ROI_area')).multiply(0.000001)
        WThresh = ee.Array(collection.aggregate_array('wThresh'))
        WError = WaterArea.multiply(ee.Array(collection.aggregate_array('wError2')))
        LError = ee.Array(collection.aggregate_array('lError2')).multiply(ROIArea.subtract(WaterArea))
        exportDict = ee.Dictionary({
            'Date': time,
            'WaterArea': WaterArea,
            'WThresh': WThresh,
            'LakeID': ID,
            'WError': WError,
            'LError': LError
            })
        
        exportTable = ee.Feature(None, exportDict)
        return exportTable
    Export = ee.Algorithms.If(
        condition = S1.size().gt(0),
        trueCase = ee.Feature(extractTimeSeries(S1)),
        falseCase = None
        )
    return Export
    #return([WaterAreaA,WaterAreaD,timeA,timeD,wPixelmeanA, wPixelStdA, lPixelmeanA,  lPixelStdA, wPixelmeanD, wPixelStdD, lPixelmeanD,  lPixelStdD, inPixelmeanA, inPixelStdA, outPixelmeanA,  outPixelStdA, inPixelmeanD, inPixelStdD, outPixelmeanD,  outPixelStdD  ])