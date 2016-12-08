__author__ = 'Huy Tu'
# 4/14/2015
import os
import pickle
import math
import numpy 
import wave
import hashlib
import matplotlib.pyplot as plt

from scipy.signal import decimate
from scipy.io.wavfile import read

WAV_DIRECTORY = "db/"
DEBUG_SPEC = False

hash_dictionary = {}

def convert_to_mono(path):
	rate, waveF = read(path)
	return numpy.mean(waveF, 1), rate
	'''
	leftA = numpy.array(waveF[:, 0],dtype=float)
	leftA /= 32768.0
	rightA = numpy.array(waveF[:, 1],dtype=float)
	rightA /= 32768.0
	mono = ((leftA + rightA) / 2), rate
	#plt.plot(timeN, result)
	#Pxx, freqs, bins, im = plt.specgram(mono, NFFT=NFFT, noverlap=1984)
	return mono
	'''
	
	
	

def downsample(x, fs1, fs2):
	rate = fs1/fs2
	result = decimate(x, int(rate))
	#print result
	#print result.shape
	timeN = numpy.zeros(len(result))
	for m in range(len(result)):
		timeN[m] = ((1.0)*(m))/((1.0)*fs2)
	#plt.plot(timeN, result)
	NFFT = 2048
	Fs = fs2
	nover = 31.0 / 32 * .37 * fs2
	Pxx, freqs, bins, im = plt.specgram(result.copy(), NFFT=NFFT, Fs = Fs, noverlap = int(nover))
	#print "hiiiiiiiiiii"
	#print Pxx
	
	return Pxx, freqs, timeN

def get_bark_bounds(min_f, max_f, n):
	step = (math.log(max_f, 2) - math.log(min_f, 2))/(1.0*(n-1))
	bark_scale = numpy.zeros(n);
	for i in range(n):
		bark_scale[i] = math.log(min_f, 2) + step*i
		bark_scale[i] = 2**(bark_scale[i])
	
	return bark_scale

def get_hashes(arrayX, bark_regions, freqs):
	result = numpy.zeros((len(bark_regions)-1, arrayX.shape[1]))

	#print arrayX
	#print result.shape
	for y in range(arrayX.shape[1]):
		for x in range(arrayX.shape[0]):
			for z in range(len(bark_regions) - 1):
				if((freqs[x] >= bark_regions[z]) and (freqs[x] < bark_regions[z + 1])):
					result[z, y] += (abs(arrayX[x, y]))**2
		if(y % 1000 == 0):	
			print(y)
	return result
	
def getB(rawHash):
	B = numpy.zeros((rawHash.shape[0]-1, rawHash.shape[1]-1))
	D = numpy.zeros(32);
	for i in range(rawHash.shape[0]-1):
		for j in range(rawHash.shape[1]-1):
			if(rawHash[i,j] + rawHash[i+1,j+1] > rawHash[i,j+1] + rawHash[i+1,j]):
				B[i, j] = 1
			else:
				B[i, j] = 0
	B = numpy.flipud(B)
	for i in range(rawHash.shape[0]-1):
		D[i] += 2**i
	K = D.dot(B)
	return K
	
def db_add_hash(hash_value, md5, offset):
	global hash_dictionary

	hash_dictionary["lut"][int(hash_value)] = {}
	hash_dictionary["lut"][int(hash_value)][md5] = offset

def db_add_song(name, md5, hashes):
	global hash_dictionary
	hash_dictionary["songs"][md5] = {}
	hash_dictionary["songs"][md5]["hashes"] = hashes
	hash_dictionary["songs"][md5]["name"] = name

def Mdatabase(songs, bark_regions):
	global hash_dictionary
	hash_dictionary["songs"] = {}
	hash_dictionary["lut"] = {}
	for song in songs:
		print("Analyzing song: " + song)
		song_matrix, rate = convert_to_mono(WAV_DIRECTORY + song)
		song_matrix, freqs, timeN = downsample(song_matrix, rate, 5512)
		hashes = get_hashes(song_matrix, bark_regions, freqs)
		hashes = getB(hashes)
		md5 = hashlib.md5(open(WAV_DIRECTORY + song).read()).hexdigest()
		db_add_song(os.path.splitext(song)[0], md5, hashes)
		for offset in range(len(hashes)):
			db_add_hash(hashes[offset], md5, offset)
	
	pickle.dump(hash_dictionary, open( "saveD1.p", "wb" ) )
	
	from pprint import pprint
	pprint(hash_dictionary)

def get_song_list():
	return os.listdir(WAV_DIRECTORY)
	
def main():
	BS = get_bark_bounds(300, 2000, 34)
	plt.clf()
	songs = get_song_list()
	Mdatabase(songs, BS)
	
	#imgplot1 = plt.imshow(numpy.flipud(B), interpolation= 'nearest', extent = (0.0116, 2.61, 0, 32), cmap = 'gray')
	#plt.colorbar()
	#plt.axis('auto')
	#plt.show()

if __name__ == "__main__":
	main()