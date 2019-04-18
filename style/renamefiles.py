import os

datadir="./../_data/states/"

def main():
	for folder in os.listdir(datadir):
		# print(folder[len(datadir+folder) - len(ending):])
		ending = "-20181204-text"
		if (len(folder) > len(ending)) and (folder[len(folder) - len(ending):] == ending):
			os.rename(datadir+folder, datadir+folder[:len(folder) - len(ending)])

main()