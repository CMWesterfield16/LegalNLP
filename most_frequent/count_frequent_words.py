import os, sys

# Text analysis
from nltk.tokenize import word_tokenize
from nltk import sent_tokenize, ngrams, FreqDist
from textblob import TextBlob
import re

# Data analysis
from statistics import mean
import numpy as np
import pandas as pd
from os import path
from PIL import Image

# Data visualization
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

datafolder = "./../_data/usc/"
codeyearsint = [1925, 1934, 1940, 1946, 1953, 1958, 1964, 1970, 1976, 1982, 1988, 1994, 2000, 2006, 2012]
#codeyears = [str(x) for x in codeyearsint]
codeyears = ["2012"]

def main():
	for year in codeyears:
		all_counts = dict()
		total_text = []
		for codefolder in ["usc2012055"]:
			for file in os.listdir(datafolder+codefolder+"/ocr/"):
				with open(datafolder+codefolder+"/ocr/"+file, "rb") as f:
					print(file)
					fullcontent = f.read().decode('utf-8', 'ignore')
					content = re.split(r'\W+', x.lower() for x in fullcontent)
					total_text+=content
		for size in 2, 3, 4:
			all_counts[size] = FreqDist(ngrams(total_text, size)).most_common()
		print(all_counts[3].most_common(5))

main()