#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Write S1 lake surface area results to file

@author: mbonnema
"""
import ee
ee.Initialize()

def writeS1ToFile(ID, results, E, path):
    fileName = path+ID+'.txt'
    
    Date = results[1]
    Water = results[0]
    WPixM = results[2]
    WPixS = results[3]
    LPixM = results[4]
    LPixS = results[5]
    wProbThresh = results[6]
    wThresh = results[7]
    wError = results[8]
    lError = results[9]

    f = open(fileName,'w')
    f.write("Date\tWaterArea\twPixelmean\twPixelStd\tlPixelmean\tlPixelStd\n")
    for x in list(range(0,len(Date))):
        d = Date[x]
        w = Water[x]
        wm = WPixM[x]
        ws = WPixS[x]
        lm = LPixM[x]
        lp = LPixS[x]
        wpt = wProbThresh[x]
        wt = wThresh[x]
        we = wError[x]
        le = lError[x]
        s = "\t".join([str(d),str(w),str(wm),str(ws),str(lm),str(lp), str(wpt), str(wt), str(we), str(le)+"\n"])#,str(im),str(Is),str(om),str(op)]) + "\n"
        f.write(s)

    if len(E) != 0:
        for e in E:
            f.write(e+'\n')
    f.close()
