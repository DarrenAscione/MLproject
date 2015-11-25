def count_states(filename):
	dict = {}
	with open(filename) as file:
		data = file.readlines()
		for line in data:
			words = line.rstrip("\n").split(" ")
			if len(words) != 1:
				if words[1] not in dict.keys():
					dict[words[1]] = 0
				dict[words[1]] += 1
	return dict

def count_word(filename):
	dict = {}
	with open(filename) as file:
		data = file.readlines()
		for line in data:
			words = line.rstrip("\n").split(" ")
			if len(words) != 1:
				if words[1] not in dict.keys():
					dict[words[1]] = {}
					dict[words[1]][words[0]] = 1
				if words[0] not in dict[words[1]].keys():
					dict[words[1]][words[0]] = 1
				dict[words[1]][words[0]] += 1
	return dict

def emission_prob(filename):
	count_u = count_states(filename)
	count_e = count_word(filename)
	for key in count_e.keys():
		for words in count_e[key].keys():
			count_e[key][words] = count_e[key][words]*1.0 / count_u[key]
	return count_e


print count_states('/Users/DarrenRetinaMBP/MLproject/NPC/dev.out')
