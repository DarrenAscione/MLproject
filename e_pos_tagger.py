# returns a file containing the dev.in with its predicted labels

from testing import testing_splitter

def checker(testing_tagger, word):	
	with open(testing_tagger, "r") as file:
		data = file.readlines()
		for line in data:
			words = line.rstrip("\n").split(" ")
			if word == words[0]:
				return words[1]

def tag_all(filetest, testing_tagger, file_write):
	dataset = testing_splitter(filetest, mode="ALL")
	with open(file_write, "w") as file:
		for sets in xrange(len(dataset)):
			for words in dataset[sets]:
				tag = checker(testing_tagger,words)
				file.write("%s %s\n"%(words, tag))
			file.write("\n")


filetest = "NPC/dev.in"
testing_tagger = "NPC/emission_testing_tags.txt"
tag_all(filetest, testing_tagger, "NPC/dev.Predict")

