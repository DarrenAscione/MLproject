import copy, math, string, re, os
def parseFile(fileName, weighting=1.0):
	valueDict = {}
	inFile = open(fileName, "r")
	fileLines = inFile.readlines()
	inFile.close()
	for line in fileLines:
		splitList = line.split(" ")
		if not splitList[0] in valueDict:
			valueDict[splitList[0]] = {}
		valueDict[splitList[0]][splitList[1]] = math.log(float(splitList[2])) * weighting
	return valueDict

def parsePenalties(fileName, weighting=0.05):
	valueDict = {}
	inFile = open(fileName, "r")
	fileLines = inFile.readlines()
	inFile.close()
	for line in fileLines:
		splitList = line.split(" ")
		if not splitList[0] in valueDict:
			valueDict[splitList[0]] = {}
		if not splitList[1] in valueDict[splitList[0]]:
			valueDict[splitList[0]][splitList[1]] = {}
		valueDict[splitList[0]][splitList[1]][splitList[2]] = math.log(float(splitList[3])) * weighting
	return valueDict

def parseSequences(fileName, tags=True):
	inFile = open(fileName, "r")
	fileLines = inFile.readlines()
	inFile.close()
	valueList = []
	newSequence = []
	for line in fileLines:
		if tags:
			line = line.split(" ")[0]
		line = line.strip()
		if len(line) > 0:
			newSequence.append(line)
		elif len(line) == 0:
			valueList.append(newSequence)
			newSequence = []
	return valueList

def viterbiTagger(outputs, inFilename, outFilename, tags=True):
	inFile = open(inFilename, "r")
	inFileLines = inFile.readlines()
	inFile.close()
	outFile = open(outFilename, "w")
	inFilePointer = 0
	for output in outputs:
		for tag in output.sequence[2:-1]:
			try:
				line = inFileLines[inFilePointer].strip()
			except IndexError:
				break
			if tags:
				line = line.split(" ")[0]
			outFile.write("{0} {1}\n".format(line, tag))
			inFilePointer += 1
		outFile.write("\n")
		inFilePointer += 1
	outFile.close()

def parse_feature_probs(feature_prob, weighting=0.9):
	fp_dict = {}
	fp_file = open(feature_prob, "r")
	fp_lines = fp_file.readlines()
	fp_file.close()
	for line in fp_lines:
		regex, tag, prob = line.strip().split(" ")
		if not regex in fp_dict:
			fp_dict[regex] = {}
		try:	
			fp_dict[regex][tag] = math.log(float(prob)) * weighting
		except ValueError:
			fp_dict[regex][tag] = None
	return fp_dict

def tag_extractor(filename):
	alist = []
	with open(filename, "r") as file:
		data = file.readlines()
		for line in data:
			words = line.rstrip("\n").split(" ")
			if len(words) != 1:
				alist.append(words[1])
	return alist

def accuracy(original_file, predicted_file):
	count = 0
	originals = tag_extractor(original_file)
	predicted = tag_extractor(predicted_file)
	for tag in xrange(len(originals)):
		if originals[tag] == predicted[tag]:
			count += 1
	return (count *1.0)/ len(predicted)

class ViterbiSequence:
	def __init__(self, secondLastTag, lastTag):
		self.sequence = [secondLastTag, lastTag]
		self.logProbability = 0.0
	def probTransmission(self, nextTag, nextEmission):
		lastTag = self.sequence[-1]
		secondLastTag = self.sequence[-2]
		probabilityChain = 0
		if self.logProbability == None:
			return None
		if nextEmission == None:
			return self.logProbability + logTransitions[lastTag][nextTag]	
		else:
			testEmission = nextEmission
			if lastTag == START:
				testEmission = nextEmission.lower()
			for regex in regexFeatures:
				if compiled[regex].match(testEmission):
					probabilityChain += regexFeatures[regex][nextTag]
			if not nextEmission in logEmissions[nextTag]:
				return None
			logTransitions[lastTag][nextTag]
			logPenalties[secondLastTag][lastTag][nextTag]
			return self.logProbability + logTransitions[lastTag][nextTag] + logEmissions[nextTag][nextEmission] + logPenalties[secondLastTag][lastTag][nextTag] + probabilityChain
	def transit(self, nextTag, nextEmission):
		nextStep = copy.deepcopy(self)
		nextStep.logProbability = nextStep.probTransmission(nextTag, nextEmission)
		nextStep.sequence.append(nextTag)
		return nextStep

if __name__ == "__main__":
	START = "__START"
	END = "__END"
	FEATURE_PROB_IN = "regularised_feature_probs.txt"
	TRANSITION_PENALTY = "transition_2nd_order.txt"
	EMISSIONS = "part5_emission_testing.txt"
	TRANSITIONS = "transition.txt"
	OUTPUT_FILE = "p5_viterbi_2nd_order.txt"
	TESTING_FILE = "../dev.in"
	GOLD_STANDARD = "../dev.out"
	# model parameters
	logPenalties = parsePenalties(TRANSITION_PENALTY, 0.0087) #0.0087
	regexFeatures = parse_feature_probs(FEATURE_PROB_IN, 0.9) #0.9
	logEmissions = parseFile(EMISSIONS, 0.9) #0.9
	logTransitions = parseFile(TRANSITIONS, 0.72) #0.72

	compiled = {}
	for regex in regexFeatures:
		compiled[regex] = re.compile(regex)

	# list of all tags
	allTags = logEmissions.keys()

	# list of sequences
	# each sequence is a Python list containing the words in the sequence
	sequences = parseSequences(TESTING_FILE)

	# output sequences corresponding to input sequences
	outputs = []

	for sequence in sequences:
		dpTable = [ViterbiSequence(START, START)]
		for i in range(-1, len(sequence) -1):
			newDpTable= []
			for tag in allTags:
				positionMax = None
				maxChoice = None
				for dpEntry in dpTable:
					piValue = dpEntry.probTransmission(tag, sequence[i +1])
					if piValue >= positionMax:
						positionMax = piValue
						maxChoice = dpEntry
				newDpTable.append(maxChoice.transit(tag,sequence[i +1]))
			dpTable = newDpTable
		endingMax = None
		endMaxChoice = None
		for dpEntry in dpTable:
			piValue = dpEntry.probTransmission(END, None)
			if piValue >= endingMax:
				endingMax = piValue
				endMaxChoice = dpEntry
		endingState = endMaxChoice.transit(END, None)
		outputs.append(endingState)
	viterbiTagger(outputs, TESTING_FILE, OUTPUT_FILE)
	os.system("diff -u " + OUTPUT_FILE + " " + "../dev.out" + "> difference_2nd_order.txt")
	print accuracy(OUTPUT_FILE, GOLD_STANDARD)