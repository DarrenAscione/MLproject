import re
"""
Searches regexes and calculates the probability that a word matches the tag given that
the word matches the regex.
Words starting with @: @\S+
Words starting with #: #.+
Words starting with http://: http://.+
Alphanumerics.Alphanumerics: [a-zA-Z0-9]+\.[a-zA-Z0-9]+
Multiple punctuation marks that ARE NOT ...: (?!\.\.\.)[.!?;,\'"]+
Capitalised words: [A-Z][a-z]+
Words ending in 'ing': [a-zA-Z]+ing
Words ending in 'ion':[a-zA-Z]+ion
Words ending in 'ed':[a-zA-Z]+ed
Words ending in 'ly':[a-zA-Z]+ly
Words ending in 'ity':[a-zA-Z]+ity
Number followed by 'am' or 'pm': [0-9]+[pa]m
Number: [0-9]+
Words ending in 's': .+s
All alphabetical: [a-zA-Z]+
Colon followed by other characters: :.+
"""
train_file = "../train"
out_file = "feature_probs.txt"
REGEXES = [
		r'^@\S+$',
		r'^#.+$',
		r'^http://.+$',
		r'^(?!\.\.\.)[.!?;,\'"]+$',
		r'^[A-Z][a-z]+$',
		r'^[a-zA-Z]+[iI][nN][gG]$',
		r'^[a-zA-Z]+[iI][oO][nN]$',
		r'^[a-zA-Z]+[eE][dD]$',
		r'^[a-zA-Z]+[lL][yY]$',
		r'^[a-zA-Z]+[iI][tT][yY]$',
		r'^[a-zA-Z]+[eE][rR]$',
		r'^[0-9]+[pPaA][mM]$',
		r'^[0-9]+$',
		r'^[0-9]+[:][0-9]+$',
		r'^[0-9]+.*[0-9]+$',
		# r'^[0-9]+.+$',
		r'^[0-9]{4}$',
		r'^[0-9]+[sS]$',
		r'^.+(?!\')[sS]$',
		r'[Hell]$',
		r'^:.+$',
		r'^=.+$',
		r'^[lL][oO][lL]$',
		r'^.+[fF][uU][lL]$',
		r'^.*\'[sS]$',
		r'^[0-9]+[sS][tT]$',
		r'^[0-9]+[nN][dD]$',
		r'^[0-9]+[rR][dD]$',
		r'^[0-9]+[tT][hH]$',
		r'^[(one)(two)(three)(four)(five)(six)(seven)(eight)(nine)(ten)]$',
		r'^[tT][hH][eE]$',
		r'^[dD][oO]$',
		r'^[sS][oO]$',
		r'^[vV][sS]$',
		r'^[A-Z].+[sS]$',
]
ALL = "ALL"
COMPILED = [re.compile(regex) for regex in REGEXES]
in_file = open(train_file, "r")
in_lines = in_file.readlines()
in_file.close()
count_dict = {}
for regex in REGEXES:
	count_dict[regex] = {ALL: 0.0}
for line in in_lines:
	line = line.strip()
	if len(line) <= 0:
		continue
	word, tag = line.split(" ")
	for i in range(len(COMPILED)):
		if COMPILED[i].match(word):
			if not tag in count_dict[REGEXES[i]]:
				count_dict[REGEXES[i]][tag] = 0.0
			count_dict[REGEXES[i]][tag] += 1
			count_dict[REGEXES[i]][ALL] += 1

def regularise(prob_dict, regularisation_strength = 0.01):
	allPOS_file = open("../allPOS", "r")
	allPOS = []
	for line in allPOS_file:
		allPOS.append(line.strip())
	allPOS_file.close()
	for regex in prob_dict:
		num_missing = len(allPOS) - len(prob_dict[regex].keys())
		if num_missing == 0:
			regularised_prob = 0
		else:
			regularised_prob = (regularisation_strength / num_missing) ** 2
		fitting_factor = 1 - num_missing * regularised_prob
		for POS in allPOS:
			if not POS in prob_dict[regex]:
				prob_dict[regex][POS] = regularised_prob
			elif POS in prob_dict[regex]:
				prob_dict[regex][POS] *= fitting_factor
	return prob_dict

prob_dict = {}
for regex in count_dict:
	prob_dict[regex] = {}
	for tag in count_dict[regex]:
		if tag is ALL:
			continue
		prob_dict[regex][tag] = count_dict[regex][tag] / count_dict[regex][ALL]

with open(out_file, "w") as out_fileF:
	for regex in prob_dict:
		for tag in prob_dict[regex]:
			out_fileF.write("{0} {1} {2}\n".format(regex, tag, prob_dict[regex][tag]))	

with open("regularised_" + out_file, "w") as out_fileF:
	regularised_dict = regularise(prob_dict, 1e-30)
	for regex in regularised_dict:
		for tag in regularised_dict[regex]:
			out_fileF.write("{0} {1} {2}\n".format(regex, tag, prob_dict[regex][tag]))	