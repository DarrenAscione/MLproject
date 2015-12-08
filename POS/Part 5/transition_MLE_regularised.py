transitionCounts = {}

START = "__START"
END = "__END"
ALL_POS_COUNT = 43
REGULARISED_PROB = 0.001 #0.001

def pushTransition(prevState, currState):
	global transitionCounts
	if not prevState in transitionCounts:
		transitionCounts[prevState] = {}
		transitionCounts[prevState]["all"] = 0
	if not currState in transitionCounts[prevState]:
		transitionCounts[prevState][currState] = 0
	transitionCounts[prevState][currState] += 1
	transitionCounts[prevState]["all"] += 1

def extractState(line):
	global END
	line = line.strip()
	if len(line) == 0:
		return END
	return line.split(" ")[1]

all_pos_file = open("../allPOS", "r")
all_pos = [line.strip() for line in all_pos_file.readlines()]
all_pos.append(END)
all_pos.append(START)
all_pos_file.close()
inFile = open("../train", "r")
lines = inFile.readlines()
lines = map(lambda x: x.strip(), lines)
inFile.close()
outFile = open("transition.txt", "w")

prevState = START
for line in lines:
	currState = extractState(line)
	pushTransition(prevState, currState)
	if currState == END:
		prevState = START
	else:
		prevState = currState

for y in transitionCounts:
	missing_tag_count = ALL_POS_COUNT - len(transitionCounts[y].keys())
	fitting_factor = 1 - missing_tag_count * REGULARISED_PROB
	for x in all_pos:
		if x in transitionCounts[y]:
			prob = fitting_factor * float(transitionCounts[y][x]) / transitionCounts[y]["all"] 
		else:
			prob = REGULARISED_PROB
		outFile.write("{0} {1} {2}\n".format(y, x, prob))
	try:
		outFile.write("{0} {1} {2}\n".format(y, END, float(transitionCounts[y][END]) / transitionCounts[y]["all"] ))
	except KeyError:
		pass
outFile.close()