from __future__ import absolute_import
from __future__ import print_function
import six

import rake
import readTxt
import operator
import io
import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
import re
import os
import os.path
import spacy
from spacy.lang.en import English
lemmatizer = WordNetLemmatizer()
nlp = spacy.load("en")
stoppath = "SmartStoplist.txt"
dirpath = r"data\40companies"

rake_object = rake.Rake(stoppath, 3, 3, 2)
merge =readTxt.fileMerge()



#去非英文和规范化
def preprocess(text,onlyEnglish=True,normalize=True):
	lemmatizer = WordNetLemmatizer()
	if onlyEnglish==True:
		text = re.sub('[^a-zA-z]',' ',text)
	if normalize==True:
		words = []
		text = text.split()
		for _ in text:
			words.append(lemmatizer.lemmatize(_))
		text = ' '.join(words)
	return text


#提取关键词中的名词
def postprocess(words,delAdj=True):
	nlp = spacy.load('en')
	if delAdj==True:
		for i in range(len(words)):
			doc = nlp(words.loc[i,0])
			for chunk in doc.noun_chunks:
				words.loc[i,0]=chunk.text
	return words


#人工处理关键词
def newprocess(words):
	nlp = spacy.load('en')
	for i in range(len(words)):
		doc = nlp(words.loc[i,0])
		if len(doc)==3:
			if doc[1].pos_==("NOUN"):
				if doc[2].pos_==("NOUN"):
					if doc[0].pos_==("NOUN"):
						pass
					else:
						words.set_value(i,0,doc[-2:])
				else:
					words.set_value(i,0,doc[:2])
			elif doc[2].pos_==("NOUN"):
				words.set_value(i,0,doc[-2:])
			elif doc[0].pos_ ==("NOUN"):
				words.set_value(i,0,doc[0])
			else:
				pass
		elif len(doc)==2:
			if doc[1].pos_!=("NOUN"):
				if doc[0].pos_==("NOUN"):
					words.loc[i,0]=doc[0]
		else:
			pass
	return words


# 3. print results
# print("Keywords:", keywords)

#提取关键词
def keywordsExa(text,pre=True,post=True,new=True):
	if pre==True:
		text = preprocess(text)
	keywords = pd.DataFrame(rake_object.run(text))
	if post==True:
		keywords = postprocess(keywords)
	if new==True:
		keywords = newprocess(keywords)
	return keywords

# keywords = keywordsExa(text)
# keywords.to_csv("data/Pre_Post_New_maxphrseLen=3.csv")

if __name__ == "__main__":
	fileList = merge.read(dirpath)
	for filename in fileList:
		file = io.open(os.path.join(filename,"allWords.txt"), 'r',encoding="iso-8859-1")
		text = file.read()
		keywords = keywordsExa(text,pre="False")
		keywords.to_csv(os.path.join(filename,"keywords_nopre.csv"))

