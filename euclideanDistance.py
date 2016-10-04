#!/usr/bin/python3


#import struct; from struct import unpack_from
import math
import logging
import sys
import time
import cProfile
import numpy as np
import array 
import os
from itertools import zip_longest

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

def main():

    fn='points'
    ar1=array.array('h')
    #fromfile, as struct.unpack is not fast enough
    ar1.fromfile(open(fn,'rb'),int(os.path.getsize(fn)/ar1.itemsize))
    #To get the correct indian we biteswap
    ar1.byteswap()

    #I create a numpy array for performance reasons
    ar=np.array(ar1)
    #I slice the array to separate the x and y coordinates (x.shape and y.shape must
    #be identical!
    x=ar[::2]
    y=ar[1::2]

    #Validation test:
    #x=np.array([30,20,10,5,-1,-2,-3,-4,-5,-6,-7,-8,-10,-20,-30,-40,-50,-60,-70,-80,-90,-100,-110,-120,-130,-140,-150])
    #y=np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    
    #Euclidean distance calculation (throughout the whole array)
    #Firs point (-200,300)
    q1=np.subtract(x,-200)
    q2=np.subtract(y,300)
    #We squared the result, being careful in not casting to a too small type)
    z1=np.multiply(np.absolute(q1).astype('uint64'),np.absolute(q1).astype('uint64'))
    z2=np.multiply(np.absolute(q2).astype('uint64'),np.absolute(q2).astype('uint64'))
    #I calculate the distance. We don't sqrt as not needed for the comparisons. 
    dist1=np.add(z1,z2)
    
    #Second point (1000,25)
    t1=np.subtract(x,1000)
    t2=np.subtract(y,25)
    w1=np.multiply(np.absolute(t1).astype('uint64'),np.absolute(t1).astype('uint64'))
    w2=np.multiply(np.absolute(t2).astype('uint64'),np.absolute(t2).astype('uint64'))
    dist2=np.add(w1,w2)
    
    #We need to put together the x and y arrays together with the distances to the 
    #two points, so as to sort on the distance column
    array_el=np.column_stack((x,y))
    array_1=np.column_stack((dist1,array_el)) 
    array_2=np.column_stack((dist2,array_el))
    #We now sort the two arrays on the first column, the distance 
    fin_1=array_1[array_1[:, 0].argsort()]
    fin_2=array_2[array_2[:, 0].argsort()]
    #We print the first 10 elements of the sorted array for the nearest points to 
    #(-200,300), and we take the last 20 elements for the points the furtherest from 
    #(1000,25)
    print('10 nearest points to (-200,300), with the first point the nearest')
    print(fin_1[:10]) 
    print('********************************')
    print('20 furthest points from (1000,25), with the last point the furthest')
    print(fin_2[-20:])
    #We time the overall performance. cProfile can help improve the result.
    print("--- %s seconds ---" % (time.time() - start_time))     
#cProfile.run('main()')

if __name__ == "__main__":   
     main()