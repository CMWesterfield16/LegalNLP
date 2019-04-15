import os, sys
from progressbar import ProgressBar

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
# from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

# Global Variables
datafolder = "./../_data/usc/"
outputfolder = "./output/"
codeyearsint = [1925, 1934, 1940, 1946, 1953, 1958, 1964, 1970, 1976, 1982, 1988, 1994, 2000, 2006, 2012]
codeyears = [str(x) for x in codeyearsint]
# codeyears = ["2012"]

NUM_MOST_COMMON = 50
ngram_sizes = [2, 3, 4]
all_letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
irrelevant_words = ["",'',"nt","ord","et","rep","seq","no"]+all_letters


# This generates a graph of the top 50 words of the given year and how they have changed in rank over time
# def generate_year_summary_graph(overall_year,size,top_100_words,all_counts_dict):
# 	title = "Top 100 Phrases of Size "+size+" in "+overall_year+" Frequency from "+codeyears[0]+" to "+codeyears[len(codeyearsint)-1]
# 	outputfile = outputdir+"/over_time_"+size+"gram_"+overall_year
# 	for key in top_100_words:
# 		for year in codeyears:
#			TODO

# 	top = plt.figure()
# 	ax = mpl_fig.add_subplot(111)
# 	ax.set_ylabel('Frequency')
# 	ax.set_xlabel('Phrase')
# 	ax.set_title(title)

# 	ax.bar(range(len(data)), data.values(), align='center')
# 	ax.xticks(range(len(data)), data.keys())
# 	plotly_fig = tls.mpl_to_plotly(top)
# 	py.iplot(plotly_fig, filename=outputfile)

def generate_top_graph(data,size,year,outputdir):
	title = "Top "+str(NUM_MOST_COMMON)+" Phrases of Size "+str(size)+" in "+year
	outputfile = outputdir+"/top_"+str(NUM_MOST_COMMON)+"_"+str(size)+"gram_"+year+".jpg"
	plt.xlabel('Phrase')
	plt.title(title)
	plt.bar(range(len(data)), list(data.values()), align='center')
	plt.xticks(range(len(data)), list(x[0] for x in data.keys()), rotation=90)
	plt.yticks([])
	plt.tight_layout()
	plt.savefig(outputfile)

def main():
	all_counts_dict = {}
	top_words = {}
	for year in codeyears:
		print("Working on:" + year)
		numcases=0
		for codefolder in (y for y in os.listdir(datafolder) if (y[:7] == "usc"+year)):
			numcases+=len([name for name in os.listdir(datafolder+codefolder+"/ocr/") if os.path.isfile(datafolder+codefolder+"/ocr/"+name)])

		all_counts = dict()
		total_text = []
		linenum=0
		pbar = ProgressBar()
		for codefolder in pbar(list(y for y in os.listdir(datafolder) if (y[:7] == "usc"+year))):
		# for codefolder in pbar(["usc2012055"]):
			for file in os.listdir(datafolder+codefolder+"/ocr/"):
				with open(datafolder+codefolder+"/ocr/"+file, "rb") as f:
					linenum+=1
					totalcontent = f.read().decode('utf-8', 'ignore')
					tokens = totalcontent.split()
					stripped = ""
					for token in tokens:
						stripped += ("".join(c for c in token if c.isalpha())).lower() + " "
					content = re.split(r'\W+', stripped)
					if content != []:
						total_text+=content
		print("Content files processed")
		for size in ngram_sizes:
			print("Generating FreqDist for size: "+str(size))
			all_counts[size] = FreqDist(ngrams(total_text, size)).most_common()
			print("Removing irrelevant words")
			i = 0
			length = len(all_counts[size])
			numcases = len(irrelevant_words)*length
			count=0
			pbar = ProgressBar(maxval=numcases).start()
			while ((i < length) and (i < NUM_MOST_COMMON)):
			# while (i < length):
				gram = all_counts[size][i][0]
				found = False
				for item in irrelevant_words:
					count+=1
					pbar.update(i+1)
					if item in gram:
						all_counts[size].pop(i)
						length-=1
						numcases-=1
						found=True
						break
				if (found == False):
					i+=1
			pbar.finish()
		
		print("Sorting for just "+str(NUM_MOST_COMMON)+" phrases")
		all_counts_dict[year] = all_counts
		top_words[year] = {}
		for size in ngram_sizes:
			word_tups = []
			all_words = all_counts[size][:NUM_MOST_COMMON]
			for word in all_words:
				word_tups.append((word, NUM_MOST_COMMON - all_words.index(word)))
			top_words[year][size] = dict(word_tups)

	for year in codeyears:
		print("Graphing")
		os.mkdir(outputfolder+year)
		for size in ngram_sizes:
			generate_top_graph(top_words[year][size], size, year,outputfolder+year)
			with open(outputfolder+year+"/"+year+"_"+str(size)+"grams.txt", "w+") as f:
				f.write("Rank\t"+str(size)+"gram\tNumberOfTimes\n")
				lst = all_counts_dict[year][size]
				for i in range(0,min(len(lst), NUM_MOST_COMMON)):
					tup = lst[i]
					f.write(str(i)+"\t"+str(tup[0])+"\t"+str(tup[1])+"\n")

main()