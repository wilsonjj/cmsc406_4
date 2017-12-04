#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from Porter_Stemmer_Python import PorterStemmer
import numpy as np
reps = 10

porterstemmer = PorterStemmer()

#setup
sentenceFile = open("sentences.txt","r")
sentences = sentenceFile.readlines()
sentenceFile.close()

stopwordsFile = open("stop_words.txt","r")
stopwords = stopwordsFile.readlines()
stopwordsFile.close()

processedSentences = []
FV = [] #empty feature vector

#processing
for line in sentences:
	
	#remove punctuation, special characters, and numbers
	line = re.sub('[^A-Za-z ]', ' ', line)
	
	#convert to lower case
	line = line.lower()
	
	#remove stopwords (a little hacky - could be better)
	for word in stopwords:
		word = re.sub('[^A-Za-z]','',word)
		word1 = '\W' + word + '\W'
		line = re.sub(word1,' ',line)
		word2 = '^' + word + '\W'
		line = re.sub(word2,' ',line)
	
	#remove excess spaces
	line = re.sub('\s+',' ',line)
	line = re.sub('^\s','',line)

	#stem words
	words = line.split()
	temp = ''
	for word in words:
		stemmed = porterstemmer.stem(word, 0, len(word)-1)
		temp = temp + stemmed + " "
	line = temp

	#populate feature vector
	words = line.split()
	for word in words:
		if word not in FV:
			FV.append(word)

	#add to processed list
	processedSentences.append(line)

#print FV
#print processedSentences

#TDM Generation
w = len(FV)
h = len(processedSentences)

TDMatrix = [[0 for x in range(w)] for y in range(h)]

i=0
for line in processedSentences:
	for word in line.split():
		if word in FV:
			j = FV.index(word)
			TDMatrix[i][j]+=1
	i+=1

#print TDMatrix <- This looks horrible. Not a good visual representation but it looks like everything works.

#for i in range(h): #<- This is much better. Still ugly because the matrix is huge but lets you compare rows somewhat
#	print TDMatrix[i]

#This writes the TDM as a CSV in the format specified
tdmFile = open("tdm.csv","w")
temp = "Keyword Set,"
for word in FV:
		temp = temp + word + ','
tdmFile.write(temp + '\n')
i = 0
for line in processedSentences:
	temp = "Sentence " + str(i+1)
	j = 0
	for word in FV:
		temp = temp + ',' + str(TDMatrix[i][j])
		j += 1
	i += 1
	tdmFile.write(temp + '\n')
tdmFile.close()

## K-means clustering, competitive algorithm(WTA)

#number of clusters
k = 5

centroids = []

for i in range(k):
	centroid = []
	for j in range(w):
		centroid.append(np.random.uniform(low=0.0, high=.05, size=None)) #low values as TDM is sparse
	centroids.append(centroid)

# print centroids

#for i in range(k):
#	print(centroids[i])

## assign sentence to node

#each element represents sentence, number is which group it belongs to
cluster = []

# Eucladian distance
def distance(centroid):
	distance = []
	for i in range(h):
		dist = 0
		for word in range(w):
			dist += (TDMatrix[i][word] - centroid[word])*(TDMatrix[i][word] - centroid[word])
		distance.append(dist * .5)
	return distance

#for i in range(k):
#	print(cluster[i])

## assignment
node = []
for j in range(h):
	node.append(-1)

def assignUpdate():
	shortest_dist = []
	for j in range(h):
		shortest_dist.append(9999)

	for i in range(k):
		for j in range(h):
			if (shortest_dist[j] - cluster[i][j]) > 0:
				node[j] = i
				shortest_dist[j] = cluster[i][j]

## change centroids position

	for c in centroids:
		temp = []
		total = []
		for n in node:
			if n == centroids.index(c):
				temp.append(c)
		if len(temp) > 0:
			for i in range(len(temp[0])):
				total.append(0)
		for t in temp:
			for i in range(len(t)):
				total[i] += t[i]
			c[i] = total[i] / len(t)

for r in range(reps):
	cluster = []			
	for i in range(k):
		cluster.append(  distance(centroids[i])  )
	assignUpdate()
print(node)