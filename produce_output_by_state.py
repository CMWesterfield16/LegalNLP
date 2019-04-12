import os

input_dir = "./output_by_state/"
outputfile = "summary_results_state.txt"
parameters = ["Avg Word Len", "Latin Terms","Second Person","Decisive Terms","Linguistic Diversity", "Avg Sentence Len", "Beg w/ Conjunction Sentences", "Avg Polarity", "Avg Subjectivity"]

def main():
    with open(outputfile, "w+") as outf:
        outf.write("State\t" + "\t".join(parameters) + "\n")
        for statetxt in os.listdir(input_dir):
            state = os.path.splitext("path_to_file")[0]
            outf.write(state)
            with open(input_dir + statetxt,'r') as infile:
                next(infile)
                numlines = 0
                totalsum = [0]*len(parameters)
                for line in infile:
                    numlines+=1
                    for i in range(0,len(parameters)):
                        totalsum[i] += int(line.split[3+i])
                totalsum = totalsum / numlines
                outf.write("\t" + str(totalsum))
            outf.write("\n")

main()
