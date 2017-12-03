#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from Porter_Stemmer_Python import PorterStemmer
import numpy as np

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
		centroid.append(np.random.randint(0,3))
	centroids.append(centroid)

# print centroids

#for i in range(k):
#	print(centroids[i])

## assign sentence to cluster

# Eucladian distance
def distance(centroid):
	distance = []
	for i in range(h):
		dist = 0
		for word in range(w):
			dist += (TDMatrix[i][word] - centroid[word])*(TDMatrix[i][word] - centroid[word])
		print(dist * .5)

#each element represents sentence, number is which group it belongs to
cluster = []

for i in range(k):
	distance(centroids[i])