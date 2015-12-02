#Structure of the count_word = {tag: {word: count, word: count}, tag:{word, count}}

def gen_bjos(state_count, filetest, emission_count):
	states = {}
	dict = {}
	predicts = {}
	# Read state count from file
	with open(state_count, "r") as file:
		data = file.readlines()
		for line in data:
			words = line.rstrip("\n").split(" ")
			states[words[0]] = float(words[1])
	for i in states.keys(): dict[i] = {}
	# Iterate through test set
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
			for tags in states.keys():
				dict[tags][words] = 1.0 / (states[tags] + 1)
			# predicted_tag = min(states[tags] + 1)
			# predicts[words] = predicted_tag
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
	elif mode == "unique":
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

def output_to_file(emission, file_write, mode="normal"):
	if mode == "readable":
		with open(file_write, "a") as file:
			for key in emission.keys():
				file.write("\n ------------------------------------- \n")
				file.write("Emission State: %s\n"%(key))
				for words in emission[key].keys():
					file.write("%s: %f\n"%(words, emission[key][words]))
				file.write("\n ------------------------------------- \n")
	else:
		with open(file_write, "a") as file:
			for key in emission.keys():
				for words in emission[key].keys():
					file.write("%s %s %f\n"%(key,words, emission[key][words]))

def tagger(predicts, file_write):
	with open(file_write, "a") as file:
			for keys in predicts.keys():
				file.write("%s %s\n"%(keys,predicts[keys]))


testing = "POS/dev.in"
emission_count = "POS/emission_train_count.txt"
state_count = "POS/emission_count.txt"
filetest = testing_splitter(testing, mode="unique")
# bjos, predicts = gen_bjos(state_count, filetest, emission_count)
# # output_to_file(bjos, "POS/emission_testing.txt")


# tagger(predicts, "POS/emission_testing_tags.txt")

