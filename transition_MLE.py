transitionCounts = {}

START = "__START"
END = "__END"

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

inFile = open("POS/train", "r")
lines = inFile.readlines()
lines = map(lambda x: x.strip(), lines)
inFile.close()
outFile = open("POS/transmission.txt", "w")
outFileReadable = open("POS/transmissionReadable.txt", "w")

prevState = START
for line in lines:
	currState = extractState(line)
	pushTransition(prevState, currState)
	if currState == END:
		prevState = START
	else:
		prevState = currState

for y in transitionCounts:
	outFileReadable.write(y + "\n--------------\n")
	for x in transitionCounts[y]:
		if x is "all":
			continue
		prob = float(transitionCounts[y][x]) / transitionCounts[y]["all"]
		outFileReadable.write(x + ((10 - len(x))* " ") + str(prob) + "\n")
		outFile.write("{0} {1} {2}\n".format(y, x, prob))
	outFileReadable.write("\n")
outFile.close()
outFileReadable.close()