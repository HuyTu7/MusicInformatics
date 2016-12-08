__author__ = 'Huy Tu'
import math
import numpy 
import dirac
import matplotlib.pyplot as plt
from echonest.remix import audio

#audioFile = audio.LocalAudioFile("lateralus.mp3")
#track_id = audioFile.analysis.identifier
#segments = audioFile.analysis.segments
segments = audio.AudioAnalysis('TRLCMRN1485B3F5150').segments

#This method calculate the Euclidean Distance between 2 vectors
#given that those two vectors have the same dimensions
def EuclideanD(u, v):
    sumD = 0.0
    euclidD = 0.0
    for i in range(len(u)):
        sumD += (u[i]- v[i])**2
    euclidD = math.sqrt(sumD)
    return euclidD

#This method calculate the Euclidean Distance Matrix
#for both timbre and pitches between segments of the song
def SimilarityMatrix():
    s = (len(segments), len(segments))
    euclidD = 0.0
    tsMatrix = numpy.zeros(s)
    psMatrix = numpy.zeros(s)
    for i in range(len(segments)):
        for j in range(len(segments)):
            euclidD = EuclideanD(segments[i].timbre, segments[j].timbre)
            tsMatrix[i][j] = euclidD
    for m in range(len(segments)):
        for n in range(len(segments)):
            euclidD = EuclideanD(segments[m].pitches, segments[n].pitches)
            psMatrix[m][n] = euclidD
    return tsMatrix, psMatrix


def main():
    # my code here
    #print track_id
    t,p = SimilarityMatrix()
    #print m
    imgplot1 = plt.imshow(t)
    imgplot1.set_cmap('hot')
    imgplot2 = plt.imshow(p)
    imgplot2.set_cmap('hot')
    plt.colorbar()
    plt.show()
if __name__ == "__main__":
    main()
