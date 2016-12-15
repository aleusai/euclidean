#!/usr/local/bin/python3


#import struct; from struct import unpack_from
import math
import logging
import sys
import time
import cProfile
import numpy as np
import array 
import os
import pandas as pd


#Notice: all the relevant packages have been installed with pip
#Logging not needed, used to replace print statements
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)
#Logging to stdout disabled, we are not using it
logging.disable(logging.CRITICAL)

start_time = time.time()

fn='points'
ar1=array.array('h')
#fromfile, as struct.unpack is not fast enough
ar1.fromfile(open(fn,'rb'),int(os.path.getsize(fn)/ar1.itemsize))
#To get the correct indian we byteswap
ar1.byteswap()

#We create a numpy array for performance reasons
ar=np.array(ar1).astype(float)
#I slice the array to separate the x and y coordinates (x.shape and y.shape must
#be identical!)
x=ar[::2]
y=ar[1::2]

dataframe = pd.DataFrame()
dataframe['x']=x
dataframe['y']=y

x1 = -200.0
y1 = 300.0

x2 = 1000.0
y2 = 25.0

dataframe['x - x1']=dataframe['x'] - x1
dataframe['y - y1']=dataframe['y'] - y1

dataframe['(x - x1)^2']=(dataframe['x'] -x1)**2
dataframe['(y - y1)^2']=(dataframe['y'] - y1)**2

dataframe['x - x2']=dataframe['x'] -x2
dataframe['y - y2']=dataframe['y'] - y2

dataframe['(x - x2)^2']=(dataframe['x'] - x2)**2
dataframe['(y - y2)^2']=(dataframe['y'] - y2)**2

dataframe['dist1'] = dataframe['(x - x1)^2'] + dataframe['(y - y1)^2']
dataframe['dist2'] = dataframe['(x - x2)^2'] + dataframe['(y - y2)^2']

#Validation test:
#x=np.array([30,20,10,5,-1,-2,-3,-4,-5,-6,-7,-8,-10,-20,-30,-40,-50,-60,-70,-80,-90,-100,-110,-120,-130,-140,-150])
#y=np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

resultNearest = pd.DataFrame()

nearest = dataframe.sort_values('dist1',ascending=True)

resultNearest['x'] = nearest['x']
resultNearest['y'] = nearest['y']
resultNearest['dist1'] = nearest['dist1']

furtherst =  dataframe.sort_values('dist2',ascending=False)

resultFurthest = pd.DataFrame()

resultFurthest['x'] = furtherst['x']
resultFurthest['y'] = furtherst['y']
resultFurthest['dist2'] = furtherst['dist2']

print('10 nearest points to (-200,300), with the first point the nearest')
print(resultNearest.head(10)) 
print('********************************')
print('20 furthest points from (1000,25), with the last point the nearest')
print(resultFurthest.head(20))
#We time the overall performance. cProfile can help improve the result.
print("--- %s seconds ---" % (time.time() - start_time))     
#cProfile.run('main()')

