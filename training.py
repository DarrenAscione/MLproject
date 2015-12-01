#Structure of the count_word = {tag: {word: count, word: count}, tag:{word, count}}
# training.py outputs 2 file: bjo file and count file

def count_word(filename):
	dict = {}
	with open(filename) as file:
		data = file.readlines()
		for line in data:
			words = line.rstrip("\n").split(" ")
			if len(words) != 1:
				# if tag not seen
				if words[1] not in dict.keys():
					dict[words[1]] = {}
				if words[0] not in dict[words[1]].keys():
					dict[words[1]][words[0]] = 0
				dict[words[1]][words[0]] += 1
	return dict

def count_all_states(word_count):
	states = {}
	for key in word_count.keys():
		states[key] = sum(word_count[key].values())
	return states

def output_to_file(emission, file_write, mode="normal"):
	if mode == "readable":
		with open(file_write, "a") as file:
			for key in emission.keys():
				file.write("\n ------------------------------------- \n")
				file.write("Emission State: %s\n"%(key))
				for words in emission[key].keys():
					file.write("%s: %f\n"%(words, emission[key][words]))
				file.write("\n ------------------------------------- \n")
	elif mode == "state":
		with open(file_write, "a") as file:
			for key in emission.keys():
				file.write("%s %f\n"%(key, emission[key]))
	else:
		with open(file_write, "a") as file:
			for key in emission.keys():
				for words in emission[key].keys():
					file.write("%s %s %f\n"%(key,words, emission[key][words]))

# Computes the bjos
def gen_bjo(word_count):
	dict = {}
	state_count = count_all_states(word_count)
	for key in word_count.keys():
		dict[key] = {}
		for words in word_count[key].keys():
			dict[key][words] = word_count[key][words]*1.0 / state_count[key]
	return dict


training = "NPC/dev.out"
word_count = count_word(training)
bjo = gen_bjo(word_count)
#Outputs readable format
output_to_file(bjo, "NPC/emission_trainingReadable.txt", mode="readable")
#Outputs normal format (Emission Probability)
output_to_file(bjo, "NPC/emission_training.txt")
#Outputs normal format (Word count for each Tag)
output_to_file(count_word(training), "NPC/emission_train_count.txt")
# output_to_file(count_all_states(word_count), "POS/state_count.txt")
output_to_file(count_all_states(word_count), "NPC/emission_count.txt", mode="state")
