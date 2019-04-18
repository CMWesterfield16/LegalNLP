import os

input_dir = "./output_by_state/"
outputfile = "summary_results_state.txt"
parameters = ["Avg Word Len", "Latin Terms","Second Person","Decisive Terms","Linguistic Diversity", "Avg Sentence Len", "Beg w/ Conjunction Sentences", "Avg Polarity", "Avg Subjectivity"]

def main():
    with open(outputfile, "w+") as outf:
        outf.write("State\t" + "\t".join(parameters) + "\n")
        for statetxt in os.listdir(input_dir):
            state = os.path.splitext(statetxt)[0]
            outf.write(state+"\t")
            with open(input_dir + statetxt,'r') as infile:
                next(infile)
                numlines = 0
                totalsum = [0]*len(parameters)
                for line in infile:
                    if (len(line.split("\t")) < (2 + len(parameters))):
                        break
                    numlines+=1
                    for i in range(0,len(parameters)):
                        # print(i)
                        totalsum[i] += float(line.split("\t")[3+i])
                totalsum = [str(x / numlines) for x in totalsum]
                outf.write("\t".join(totalsum))
            outf.write("\n")

main()
