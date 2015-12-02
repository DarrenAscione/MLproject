# def pos_tagger(filelist, testing_data, testing_tagger):
# 	dict = {}

from testing import testing_splitter
	

def checker(testing_tagger, word):	
	with open(testing_tagger, "r") as file:
		data = file.readlines()
		for line in data:
			words = line.rstrip("\n").split(" ")
			if word == words[0]:
				return words[1]

def tagger(filetest, testing_tagger, file_write):
	dataset = testing_splitter(filetest, mode="ALL")
	with open(file_write, "w") as file:
		for sets in xrange(len(dataset)):
			for words in dataset[sets]:
				tag = checker(testing_tagger,words)
				file.write("%s %s\n"%(words, tag))
			file.write("\n")


filetest = "POS/dev.in"
testing_tagger = "POS/emission_testing_tags.txt"
tagger(filetest, testing_tagger, "POS/dev.Predict")

