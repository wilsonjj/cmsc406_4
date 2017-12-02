#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from Porter_Stemmer_Python import PorterStemmer
from ctypes import *

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

	#populate feature vector
	words = line.split()
	for word in words:
		if word not in FV:
			FV.append(word)

	#add to processed list
	processedSentences.append(line)

#print FV
#print processedSentences

#stem words
for line in processedSentences:

	line_words = line.split(" ")

	stemmed_words = ''

	for word in line_words:
		stemmed = porterstemmer.stem(word, 0, len(word) - 1)
		if len(stemmed_words) == 0:
			stemmed_words = stemmed
		else:
			stemmed_words = stemmed_words + " " + stemmed
	print(stemmed_words)