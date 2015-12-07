transitionCounts = {}

START = "__START"
END = "__END"
ALL_POS_COUNT = 43
REGULARISED_PROB = 0.00001

def pushTransition(prevprevState, prevState, currState):
	global transitionCounts
	if not prevState in transitionCounts:
		transitionCounts[prevState] = {}
	if not prevprevState in transitionCounts[prevState]:
		transitionCounts[prevState][prevprevState] = {}
		transitionCounts[prevState][prevprevState]["all"] = 0
	if not currState in transitionCounts[prevState][prevprevState]:
		transitionCounts[prevState][prevprevState][currState] = 0
	transitionCounts[prevState][prevprevState][currState] += 1
	transitionCounts[prevState][prevprevState]["all"] += 1

def extractState(line):
	global END
	line = line.strip()
	if len(line) == 0:
		return END
	return line.split(" ")[1]

all_pos_file = open("../allPOS", "r")
all_pos = [line.strip() for line in all_pos_file.readlines()]
all_pos.append(START)
all_pos.append(END)
all_pos_file.close()
inFile = open("../train", "r")
lines = inFile.readlines()
lines = map(lambda x: x.strip(), lines)
inFile.close()
outFile = open("transition_2nd_order.txt", "w")

prevState = START
prevprevState = START
for line in lines:
	currState = extractState(line)
	pushTransition(prevprevState, prevState, currState)
	if currState == END:
		prevprevState = START
		prevState = START
	else:
		prevprevState = prevState
		prevState = currState

for z in all_pos:
	for y in all_pos:
		if not z in transitionCounts:
			continue
		if y in transitionCounts[z]:
			missing_tag_count = ALL_POS_COUNT - len(transitionCounts[z][y].keys())
			fitting_factor = 1 - missing_tag_count * REGULARISED_PROB
			for x in all_pos:
				if x in transitionCounts[z][y]:
					prob = fitting_factor * float(transitionCounts[z][y][x]) / transitionCounts[z][y]["all"] 
				else:
					prob = REGULARISED_PROB
				outFile.write("{0} {1} {2} {3}\n".format(z, y, x, prob))
			try:
				outFile.write("{0} {1} {2} {3}\n".format(z, y, END, float(transitionCounts[z][y][END]) / transitionCounts[z][y]["all"] ))
			except KeyError:
				outFile.write("{0} {1} {2} {3}\n".format(z, y, x, REGULARISED_PROB))
		else:
			for x in all_pos:
				outFile.write("{0} {1} {2} {3}\n".format(z, y, x, REGULARISED_PROB))
outFile.close()