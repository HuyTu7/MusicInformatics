__author__ = 'Huy Tu'
import math
import numpy 
import dirac
import copy
import matplotlib.pyplot as plt
from echonest.remix import audio
from scipy.spatial.distance import euclidean
import random

CM = numpy.array([0.51, 0.03, 0.12, 0.09, 0.3, 0.19, 0.07, 0.28, 0.09, 0.24, 0.06, 0.00])
Cm = numpy.array([0.47, 0.06, 0.07, 0.39, 0.03, 0.28, 0.00, 0.3, 0.25, 0.1, 0.06, 0.10])
Labels = ["CM", "C#M", "DM", "EbM", "EM", "FM", "F#M", "GM", "AbM", "AM", "BbM", "BM", "Cm", "C#m", "Dm", "Ebm", "Em", "Fm", "F#m", "Gm", "Abm", "Am", "Bbm", "Bm"]

metric = "euclidean"
m = 24
n = 20.0
r = n - 1.0 
limit = 360
c = 20.0
lrate = 0.02
notesBMU = numpy.zeros((24, 2))

#This method organize the 24 by 12 vector 
#for both 12 major triads and 12 minor triads 
def stackMm():
	k = 0.00
	s  = (24, 12)
	result = numpy.zeros(s)
	a = copy.copy(CM)
	temp = copy.copy(CM)

	for i in range(len(CM)):
		k = a[len(CM) - 1]
		result[i] = copy.copy(temp)
		#print k
		for j in range(len(a)):
			if(j != (len(CM)-1)):	
				temp[j+1] = a[j]
		temp[0] = k
		a = copy.copy(temp)
		
	a = copy.copy(Cm)
	temp = copy.copy(Cm)
	for i in range(len(Cm)):
		k = a[len(Cm) - 1]
		result[i+12] = copy.copy(temp)
		#print k
		for j in range(len(a)):
			if(j != (len(Cm)-1)):	
				temp[j+1] = a[j]
		temp[0] = k
		a = copy.copy(temp)
	return result

#This method calculate the standard deviation for neighborhood function
def SD(s):
	result = (1.0/3.0)*(r - (s/c))
	return result

#This method calculate the Euclidean Distance between 2 vectors
#given that those two vectors have the same dimensions
def EuclideanD(u, v):
    sumD = 0.0
    euclidD = 0.0
    for i in range(len(u)):
        sumD += (u[i]- v[i])**2
    euclidD = math.sqrt(sumD)
    return euclidD

#This method calculate the Distance between the (i,j)
#locations of u and v on the surface of a torus. 
def d(u, v):
	result1 = v[0] - u[0]
	result2 = v[1] - u[1]
	if(result1 > (c/2)):
		result1 = c - result1
	if(result2 > (c/2)):
		result2 = c - result2
	dist = math.sqrt((result1)**2 + (result2)**2)
	return dist

#This method calculate the neighboring function
def neighboringF(u, v, s):
	result = math.exp(-((d(u, v))**2)/(2*(SD(s))**2))
	return result

#This method find the best matching unit
#for the input vector on the 20 by 20 map
def BMU(WMap, ranInput):
	minD = 0
	minD = euclidean(WMap[0,0,:], ranInput)
	minIndex1 = 0
	minIndex2 = 0
	for i in range(20):
		for j in range(20):
			dist = euclidean(WMap[i,j,:], ranInput)
			if(minD > dist):
				minIndex1 = i
				minIndex2 = j
				minD = dist
	return minIndex1, minIndex2

#This method find the best matching unit
#for all 24 major and minor triads on the 20x20 map
#then graph the map while comparing the distance of C Major 
#to all the nodes on the maps
def graph(vector, WMap):
	result = numpy.zeros((20, 20))
	distance = 0
	minIndex1 = 0
	minIndex2 = 0
	for k in range(24):
		minIndex1, minIndex2 = BMU(WMap, vector[k])
		notesBMU[k, 0] = minIndex1
		notesBMU[k, 1] = minIndex2
	
	for i in range(20):
		for j in range(20):
			distance = euclidean(WMap[i,j,:], vector[0])
			result[i, j] = distance
	
	imgplot1 = plt.imshow(result, interpolation = 'nearest')
	imgplot1 = plt.gca()
	imgplot1.invert_yaxis()
	for i in range(24):	
		plt.text(notesBMU[i, 1], notesBMU[i, 0], Labels[i], color = 'magenta')
	plt.colorbar()
	plt.show()

#Self-organizing map function that from 1 to 360 iterations
#It would loop through 24 times while taking a random input vector from major&minor triad vector
#to find a best matching units for it and updated the neighboring nodes to the BMU node
def SOM():
	W = numpy.random.rand(n,n,12)
	a = stackMm()
	minI1 = 0 
	minI2 = 0
	for s in range(1, (limit+1)):
		print s
		for i in range(1, (m+1)):
			q = random.randrange(0, 24)
			d = copy.copy(a[q])
			
			minI1, minI2 = BMU(W, d)
			u = numpy.array([minI1, minI2])
			notesBMU[q, 0] = minI1
			notesBMU[q, 1] = minI2
			
			for p in range(20):
				for o in range(20):
					v = numpy.array([p, o])
					W[p, o, :] = W[p, o, :] + (neighboringF(u, v, s))* lrate * (d - W[p, o, :])
			
			if(s % 360 == 0):	
				graph(a, W)
			
			

	
def main():
	SOM()
	#imgplot1 = plt.imshow(a, interpolation = 'nearest')
	#imgplot1.set_cmap('hot')
	#plt.colorbar()
	#plt.show()
if __name__ == "__main__":
    main()