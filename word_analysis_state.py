import os, sys
import re
from statistics import mean
from nltk.tokenize import word_tokenize
from nltk import sent_tokenize
from textblob import TextBlob
import progress_bar

import lzma, json

# inputdir = "./_data/"
outputfile = "summary_results_state.txt"


def word_analysis(content, outputfile, latinTerms, decisiveTerms):
	conjunctions = set(["and", "but", "so", "or", "nor", "yet"])

	# word features
	totalwordcount = 0
	latintermscount = 0
	secondpersoncount = 0
	decisivecount = 0
	wordlengths = []
	uniquewords = set([])

	# sentence features
	totalsentencecount = 0
	startconjunctioncount = 0
	sentencelengths = []
	sentencepolarity = []
	sentencesubjectivity = []

	# print(jsonfile['name'])
	# content = jsonfile['casebody']['data']['opinions']['text']
	tokens = word_tokenize(content)
	for i in range(0, len(tokens)):
		token = tokens[i]
		if (token.isalpha()):
			token = token.lower()
			totalwordcount+=1
			wordlengths.append(len(token))
			if (token == "you"):
				secondpersoncount+=1
			elif (token in latinTerms) or ((i + 1 < len(tokens)) and ((token + " " + tokens[i+1]) in latinTerms)) or ((i + 2 < len(tokens)) and ((token + " " + tokens[i+1] + " " + tokens[i+2]) in latinTerms)):
				latintermscount+=1
			elif (token in decisiveTerms) or ((i + 1 < len(tokens)) and ((token + " " + tokens[i+1]) in decisiveTerms) and ((token + " " + tokens[i+1]) != "probable cause" )) or ((i + 2 < len(tokens)) and ((token + " " + tokens[i+1] + " " + tokens[i+2]) in decisiveTerms)):
				decisivecount+=1

			if token not in uniquewords:
				uniquewords.add(token)

	sents = sent_tokenize(content)
	for sent in sents:
		tokens = word_tokenize(sent)
		if (len(tokens) > 1):
			sentencelengths.append(len(tokens))
			totalsentencecount+=1
			if tokens[0].lower() in conjunctions:
				startconjunctioncount+=1

			sentiment = TextBlob(sent).sentiment
			sentencesubjectivity.append(sentiment.subjectivity)
			sentencepolarity.append(sentiment.polarity)

	wordlenavg = sum(wordlengths)
	sentencelenavg = sum(sentencelengths)

	worddata = [wordlenavg, latintermscount, secondpersoncount, decisivecount, len(uniquewords)]
	sentencedata = [sentencelenavg, startconjunctioncount, sum(sentencepolarity), sum(sentencesubjectivity)]
	if (totalwordcount != 0):
		worddata = [x / totalwordcount for x in worddata]
		sentencedata = [x / totalsentencecount for x in sentencedata]
	return worddata + sentencedata

def main():
	parameters = ["Avg Word Len", "Latin Terms","Second Person","Decisive Terms","Linguistic Diversity", "Avg Sentence Len", "Beg w/ Conjunction Sentences", "Avg Polarity", "Avg Subjectivity"]

	# with lzma.open("_data/states/illinois/data/data.jsonl.xz") as in_file:
	# 	for line in in_file:
	# 		jsonfile = json.loads(str(line, 'utf8'))
	# 		print(json.dumps(jsonfile, indent=4))
	# 		break

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
	# with open(outputfile, "w+") as outf:
	# 	outf.write("State\t" + "\t".join(parameters) + "\n")

	for state in os.listdir("./_data/states/"):
		specialoutputfile = "./output_by_state/" + state + ".txt"
		with open(specialoutputfile, "w+") as f:
			f.write("Case\tJudge\tType\t" + "\t".join(parameters) + "\n")

		list_of_lists = []
		with lzma.open("_data/states/"+state+"/data/data.jsonl.xz") as in_file:
			numcases = 0
			# for line in in_file:
			# 	numcases+=1
			# linenum = 0
			for line in in_file:
				# printProgressBar(linenum, numcases, prefix = state + ' Progress:', suffix = 'Complete', length = 50)
				jsonfile = json.loads(str(line, 'utf8'))
				opinions = jsonfile['casebody']['data']['opinions']
				outputlists = []
				for opinion in opinions:
					outputlist = word_analysis(opinion['text'], specialoutputfile, latinTerms, decisiveTerms)
					with open(specialoutputfile, "a") as outf:
						case_name = jsonfile['name']
						print(case_name)
						judge = str(opinion['author'])
						# print(judge)
						typ = str(opinion['type'])
						# print(typ)
						outf.write(case_name+"\t"+judge+"\t"+typ)
						for data in outputlist:
							outf.write("\t" + str(data))
						outf.write("\n")
					outputlists.append(outputlist)
				caseoutput = [sum(x) for x in zip(*outputlists)]
				list_of_lists.append(caseoutput)
				# linenum+=1
		# fulloutput = [sum(x) for x in zip(*list_of_lists)]
		# with open(outputfile, "a") as outf:
		# 	outf.write(state)
		# 	for i in range(0, len(fulloutput)):
		# 		outf.write("\t" + str(fulloutput[i] / len(list_of_lists)))
		# 	outf.write("\n")

main()
