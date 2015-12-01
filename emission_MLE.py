#Structure of the count_word = {tag: {word: count, word: count}, tag:{word, count}}

# training.py outputs 2 file: bjo file and count file
# testing.py output annotation file and bjo file
def count_word(filename):
	dict = {}
	with open(filename) as file:
		data = file.readlines()
		for line in data:
			words = line.rstrip("\n").split(" ")
			if len(words) != 1:
				if words[1] not in dict.keys():
					dict[words[1]] = {}
					dict[words[1]][words[0]] = 0
				if words[0] not in dict[words[1]].keys():
					dict[words[1]][words[0]] = 0
				dict[words[1]][words[0]] += 1
	return dict
#change later
count_states = lambda dict_word: sum(dict_word.values())

def count_all_states(word_count):
	states = {}
	for key in word_count.keys():
		states[key] = count_states(word_count[key])
	return states

# Computes the bjos
def gen_bjo(filename, mode="training"):
	word_count = count_word(filename)
	for key in word_count.keys():
		for words in word_count[key].keys():
			if mode == "training":
				tag_count = count_states(word_count[key])
			else:
				tag_count = count_states(word_count[key])+1
			word_count[key][words] = word_count[key][words]*1.0/ tag_count
	return word_count

def output_to_file(emission, file_write):
	with open("NPC/" + file_write, "a") as file:
		for key in emission.keys():
			file.write("\n ------------------------------------- \n")
			file.write("Emission State: %s\n"%(key))
			for words in emission[key].keys():
				file.write("%s: %f\n"%(words, emission[key][words]))
			file.write("\n ------------------------------------- \n")

def testing_splitter(filename):
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

# def emission_prob_Tagger(filetest, filetrain, file_write):
# 	dataset = testing_splitter(filetest)
# 	word_count = count_word(filetrain)
# 	states_count = count_states(filetrain)
# 	# Generate table of bjos from training data
# 	bjos = gen_bjo(filetrain, mode = "training")
# 	# Generate file to save generate bjos of testing data
# 	with open(file_write, "w") as file:
# 		for sets in xrange(len(dataset)):
# 			for words in dataset[sets]:
# 				temp = 0
# 				temp_arg = ""
# 				for tags in bjos.keys():
# 					# if word found in training bjo table
# 					if words in bjos[tags].keys():
# 						if bjos[tags][words] >= temp: #replace with highest prob
# 							temp = bjos[tags][words]
# 							temp_arg = tags

# 				if temp == 0:
# 					for tag in states_count.keys():
# 						if states_count[tag] == min(states_count.values()):
# 							temp_arg = tag
# 				file.write("%s %s\n"%(words,temp_arg))
# 			file.write("\n")
# 	return file_write

def emission_prob(filetest, filetrain, file_write):
	dataset = testing_splitter(filetest)
	word_count = count_word(filetrain)
	states_count = count_all_states(word_count)
	bjos = gen_bjo(filetrain, mode="testing")
	# Generate file to save generate bjos of testing data
	with open(file_write, "w") as file:
		for sets in xrange(len(dataset)):
			for words in dataset[sets]:
				temp = 0
				temp_arg = ""
				for tags in bjos.keys():
					# if word found in training bjo table
					if words in bjos[tags].keys():
						if bjos[tags][words] >= temp: #replace with highest prob
							temp = bjos[tags][words]
							temp_arg = tags
				# word does not appear
				if temp == 0:
					for tag in states_count.keys():
						if states_count[tag] == min(states_count.values()):
							temp_arg = tag
				file.write("%s %s\n"%(words,temp_arg))
			file.write("\n")
	return file_write

def accuracy(original_file, predicted_file):
	count = 0
	originals = tag_extractor(original_file)
	predicted = tag_extractor(predicted_file)
	for tag in xrange(len(originals)):
		if originals[tag] == predicted[tag]:
			count += 1
	return (count *1.0)/ len(predicted)

def tag_extractor(filename):
	tags = []
	with open(filename) as file:
		data = file.readlines()
		for line in data:
			words = line.rstrip("\n").split(" ")
			if len(words) != 1:
				tags.append(words[1])
	return tags

test_file = "POS/dev.in"
correct_file = "POS/dev.out"
train_file = "NPC/train"
save_file = "POS/copy2.txt"
predicted = emission_prob(test_file, correct_file, save_file)
# print accuracy(correct_file, predicted)

# output_to_file(gen_bjo(train_file), "emissionReadable")



