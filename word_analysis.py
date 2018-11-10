import os, sys
from nltk.tokenize import word_tokenize

judge = sys.argv[1]
typ = sys.argv[2]

inputdir = "./_data/"
outputfile = "summary_results.txt"

def word_analysis(judge, type, case, outputfile, latinTerms, decisiveTerms):
	totalwordcount = 0;
	latintermscount = 0
	secondpersoncount = 0
	decisivecount = 0
	wordlengths = []
	with open("./_data/txt/" + judge + "/" + typ + "/" + case, "r") as casef:
		content = casef.read()
		tokens = word_tokenize(content)
		for token in tokens:
			if (token.isalpha()):
				totalwordcount+=1
				wordlengths.append(len(token))
				if (token == "you"):
					secondpersoncount+=1
				elif (token in latinTerms):
					latintermscount+=1
				elif (any(token in term for term in decisiveTerms)):
					decisivecount+=1
	wordlenavg = mean(wordlengths)
	# currently not returning total words
	return [wordlenavg, latintermscount, secondpersoncount, decisivecount]



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


	for judge in os.dir("./_data/txt/"):
		for type in os.dir("./_data/txt/" + judge):
			specialoutputfile = "./output_by_judge/" + judge "_" + typ + ".txt"
			for case_name in os.dir("./_data/txt/" + judge + "/" + typ):
				outputlist = word_analysis(judge, typ, case, specialoutputfile, latinTerms, decisiveTerms)
				with open(specialoutputfile, "a") as outf:
					outf.write(judge + "\t" + typ)
					for data in outputlist:
						outf.write("\t" + data)
					outf.write("\n")


main()