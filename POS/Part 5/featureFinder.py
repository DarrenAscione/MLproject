import re
"""
Searches regexes and calculates the probability that a word matches the tag given that
the word matches the regex.
Words starting with @: @\S+
Words starting with #: #.+
Words starting with http://: http://.+
Alphanumerics.Alphanumerics: [a-zA-Z0-9]+\.[a-zA-Z0-9]+
Multiple punctuation marks: [.!?;,'"]+
Capitalised words: [A-Z][a-z]+
Words ending in 'ing': [a-zA-Z]+ing
Words ending in 'ion':[a-zA-Z]+ion
Words ending in 'ed':[a-zA-Z]+ed
Words ending in 'ly':[a-zA-Z]+ly
Words ending in 'ity':[a-zA-Z]+ity
Number followed by 'am' or 'pm': [0-9]+[pa]m
Number: [0-9]+
"""
train_file = "../train"
out_file = "feature_probs.txt"
REGEXES = [
		r'^@\S+$',
		r'^#.+$',
		r'^http://.+$',
		r'^[a-zA-Z0-9]+\.[a-zA-Z0-9]+$',
		r'^[.!?;,\'"]+$',
		r'^[A-Z][a-z]+$',
		r'^[a-zA-Z]+ing$',
		r'^[a-zA-Z]+ion$',
		r'^[a-zA-Z]+ed$',
		r'^[a-zA-Z]+ly$',
		r'^[a-zA-Z]+ity$',
		r'^[0-9]+[pa]m$',
		r'^[0-9]+$',
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

prob_dict = {}
for regex in count_dict:
	prob_dict[regex] = {}
	for tag in count_dict[regex]:
		if tag is ALL:
			continue
		prob_dict[regex][tag] = count_dict[regex][tag] / count_dict[regex][ALL]
with open(out_file, "w") as out_fileF:
	for regex in prob_dict:
		out_fileF.write(regex + "\n")
		for tag in prob_dict[regex]:
			out_fileF.write("{0} {1}\n".format(tag, prob_dict[regex][tag]))	
		out_fileF.write("-------------\n")