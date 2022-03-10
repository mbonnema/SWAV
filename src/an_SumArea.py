#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 11:37:11 2021

@author: mbonnema
"""
import numpy as np
def SumArea(A_int,D_int):
    A_total = 0
    Dates = 0
    for key in A_int:
        Ai = np.reshape(A_int[key],[37,1])
        A_total = A_total + Ai
        if len(D_int[key]) == 37:   
            Dates = D_int[key]
    Asum = []
    if hasattr(A_total, "__len__"):
        for a in A_total:
            try:
                Asum.append(a[0][0])
            except:
                Asum.append(a)   
    else:
        Asum = 0
        
    return Asum,Dates

def SumAreaSq(A_int,D_int):
    A_total = 0
    Dates = 0
    for key in A_int:
        Ai = np.reshape(A_int[key],[37,1])
        Ai = np.square(Ai)
        A_total = A_total + Ai
        if len(D_int[key]) == 37:   
            Dates = D_int[key]
    Asum = []
    if hasattr(A_total, "__len__"):
        for a in A_total:
            try:
                Asum.append(a[0][0])
            except:
                Asum.append(a)   
    else:
        Asum = 0
        
    return np.sqrt(Asum),Dates