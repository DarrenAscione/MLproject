#Structure of the count_word = {tag: {word: count, word: count}, tag:{word, count}}

from output_printer import output_to_file, tagger

def gen_bjos(state_count, filetest, emission_count):
	states = {}
	dict = {}
	predicts = {} #list of tag to unique words
	# Read state count from file
	with open(state_count, "r") as file:
		data = file.readlines()
		for line in data:
			words = line.rstrip("\n").split(" ")
			states[words[0]] = float(words[1])
	for i in states.keys(): dict[i] = {}
	for words in filetest:
		prob_list = check(emission_count, words)
		if prob_list != {}: # word exist
			for tags in states.keys():
				if tags in prob_list.keys():
					dict[tags][words] = prob_list[tags]/(states[tags] + 1)
				else:
					dict[tags][words] = 0.0
			predicted_tag = argmax(prob_list)
			predicts[words] = predicted_tag
		elif prob_list == {}: # word does not exist
			temp = 0
			argtemp = ""
			for tags in states.keys():
				dict[tags][words] = 1.0 / (states[tags] + 1)
				if dict[tags][words] >= temp:
					temp = dict[tags][words]
					argtemp = tags
			predicts[words] = argtemp
	return dict, predicts

def testing_splitter(filename, mode):
	if mode == "ALL":
		one_dataset = []
		total_dataset = []
		with open(filename) as file:
			data = file.readlines()
			for line in data:
				words = line.rstrip("\n")
				if len(words) != 0:
					one_dataset.append(words)
				else:
					total_dataset.append(one_dataset)
					one_dataset = []
		return total_dataset
	elif mode == "unique": # finds all unique word, saves time
		data_set = []
		with open(filename) as file:
			data = file.readlines()
			for line in data:
				words = line.rstrip("\n")
				if len(words) != 0:
					if words not in data_set:
						data_set.append(words)
		return data_set

def check(filename, word):
	dict = {}
	with open(filename) as file:
		data = file.readlines()
		for line in data:
			words = line.rstrip("\n").split(" ")
			if word == words[1]:
				dict[words[0]] = float(words[2])
	return dict

def argmax(alist):
	for key in alist.keys():
		if alist[key] == max(alist.values()):
			return key

testing = "NPC/dev.in"
emission_count = "NPC/emission_train_count.txt"
state_count = "NPC/emission_count.txt"
filetest = testing_splitter(testing, mode="unique")
bjos, predicts = gen_bjos(state_count, filetest, emission_count)
output_to_file(bjos, "NPC/emission_testing.txt")
tagger(predicts, "NPC/emission_testing_tags.txt")

