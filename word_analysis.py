import os, sys
import re
from statistics import mean 
from nltk.tokenize import word_tokenize

# judge = sys.argv[1]
# typ = sys.argv[2]

inputdir = "./_data/"
outputfile = "summary_results.txt"

def word_analysis(judge, typ, case, outputfile, latinTerms, decisiveTerms):
	totalwordcount = 0;
	latintermscount = 0
	secondpersoncount = 0
	decisivecount = 0
	wordlengths = []
	with open("./_data/txt/" + judge + "/" + typ + "/" + case, "rb") as casef:
		print( "./_data/txt/" + judge + "/" + typ + "/" + case)
		content = casef.read().decode('utf-8', 'ignore')
		tokens = word_tokenize(content)
		for i in range(0, len(tokens)):
			token = tokens[i]
			if (token.isalpha()):
				totalwordcount+=1
				wordlengths.append(len(token))
				# print(token + ", " + str(len(token)))
				if (token == "you"):
					secondpersoncount+=1
				elif (token in latinTerms) or ((i + 1 < len(tokens)) and ((token + " " + tokens[i+1]) in latinTerms)) or ((i + 2 < len(tokens)) and ((token + " " + tokens[i+1] + " " + tokens[i+2]) in latinTerms)):
					latintermscount+=1
				elif (token in decisiveTerms) or ((i + 1 < len(tokens)) and ((token + " " + tokens[i+1]) in decisiveTerms)) or ((i + 2 < len(tokens)) and ((token + " " + tokens[i+1] + " " + tokens[i+2]) in decisiveTerms)):
					decisivecount+=1
	wordlenavg = mean(wordlengths)
	# currently not returning total words
	return [wordlenavg, latintermscount / totalwordcount, secondpersoncount / totalwordcount, decisivecount / totalwordcount]



def main():
	latinTerms = set([])
	with open("./_data/term_lists/latin_terms.txt", "r") as latinf:
		content = latinf.read().splitlines()
		for line in content:
			latinTerms.add(line)
	decisiveTerms = set([])
	with open("./_data/term_lists/decisive_terms.txt", "r") as decf:
		content = decf.read().splitlines()
		for line in content:
			decisiveTerms.add(line)
	with open(outputfile, "w+") as outf:
		outf.write("Judge\tType\tAvg Word Len\tLatin Terms\tSecond Person\tDecisive Terms\n")


	for judge in os.listdir("./_data/txt/"):
		specialoutputfile = "./output_by_judge/" + judge + ".txt"
		with open(specialoutputfile, "w+") as f:
			f.write("Judge\tType\tCase\tAvg Word Len\tLatin Terms\tSecond Person\tDecisive Terms\n")
		
		for typ in os.listdir("./_data/txt/" + judge):	
			list_of_lists = []
			for case in os.listdir("./_data/txt/" + judge + "/" + typ):
				outputlist = word_analysis(judge, typ, case, specialoutputfile, latinTerms, decisiveTerms)
				with open(specialoutputfile, "a") as outf:
					case_name = case.split(".")[0]
					outf.write(judge + "\t" + typ + "\t" + case_name)
					for data in outputlist:
						outf.write("\t" + str(data))
					outf.write("\n")
				list_of_lists.append(outputlist)
			fulloutput = [sum(x) for x in zip(*list_of_lists)]
			with open(outputfile, "a") as outf:
				outf.write(judge + "\t" + typ)
				for i in range(0, len(fulloutput)):
					outf.write("\t" + str(fulloutput[i] / len(list_of_lists)))
				outf.write("\n")


main()