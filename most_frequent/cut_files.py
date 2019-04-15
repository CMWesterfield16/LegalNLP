import os, sys
from progressbar import ProgressBar


def main():
	for folder in os.listdir("./output/"):
		pbar = ProgressBar()
		for file in pbar(list(y for y in os.listdir("./output/"+folder) if (y[:4] == folder))):
			with open("./output/"+folder+"/"+file, "r") as f:
				content = f.read().splitlines()
				savecontent = content[:min(len(content),52)]
			with open("./output/"+folder+"/"+file, "w+") as f:
				for line in savecontent:
					f.write(line+"\n")

main()