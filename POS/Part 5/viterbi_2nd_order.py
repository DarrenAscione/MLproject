import copy, math, string, re, os
def parseFile(fileName):
	valueDict = {}
	inFile = open(fileName, "r")
	fileLines = inFile.readlines()
	inFile.close()
	for line in fileLines:
		splitList = line.split(" ")
		if not splitList[0] in valueDict:
			valueDict[splitList[0]] = {}
		valueDict[splitList[0]][splitList[1]] = float(splitList[2])
	return valueDict

def parseTransmissions(fileName, regular_ignore= 0.00001):
	valueDict = {}
	inFile = open(fileName, "r")
	fileLines = inFile.readlines()
	inFile.close()
	for line in fileLines:
		splitList = line.split(" ")
		if float(splitList[3]) == regular_ignore:
			continue
		if not splitList[0] in valueDict:
			valueDict[splitList[0]] = {}
		if not splitList[1] in valueDict[splitList[0]]:
			valueDict[splitList[0]][splitList[1]] = {}
		valueDict[splitList[0]][splitList[1]][splitList[2]] = float(splitList[3])
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
		for tag in output.sequence[1:-1]:
			line = inFileLines[inFilePointer].strip()
			if tags:
				line = line.split(" ")[0]
			outFile.write("{0} {1}\n".format(line, tag))
			inFilePointer += 1
		outFile.write("\n")
		inFilePointer += 1
	outFile.close()

def parse_feature_probs(feature_prob):
	fp_dict = {}
	fp_file = open(feature_prob, "r")
	fp_lines = fp_file.readlines()
	fp_file.close()
	for line in fp_lines:
		regex, tag, prob = line.strip().split(" ")
		if not regex in fp_dict:
			fp_dict[regex] = {}
		try:	
			fp_dict[regex][tag] = math.log(float(prob))
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
		try:
			if self.logProbability == None:
				return None
			if nextEmission == None:
				return self.logProbability + logTransmissions[secondLastTag][lastTag][nextTag]	
			else:
				for regex in regexFeatures:
					if compiled[regex].match(nextEmission):
						if regexFeatures[regex][nextTag] is None:
							return None
						probabilityChain += regexFeatures[regex][nextTag]
				return self.logProbability + logTransmissions[secondLastTag][lastTag][nextTag] + logEmissions[nextTag][nextEmission] + probabilityChain
		except KeyError:
			try:
				return self.logProbability + math.log(REGULARISED_PROB) + logEmissions[nextTag][nextEmission] + probabilityChain
			except KeyError:
				return None
			return None
	def transit(self, nextTag, nextEmission):
		nextStep = copy.deepcopy(self)
		nextStep.logProbability = nextStep.probTransmission(nextTag, nextEmission)
		nextStep.sequence.append(nextTag)
		return nextStep

if __name__ == "__main__":
	FEATURE_PROB_IN = "regularised_feature_probs.txt"
	START = "START"
	REGULARISED_PROB = 0.00001
	# model parameters
	transmissions = parseTransmissions("transition_2nd_order.txt", REGULARISED_PROB)
	emissions = parseFile("part5_emission_testing.txt")
	regexFeatures = parse_feature_probs(FEATURE_PROB_IN)
	compiled = {}
	for regex in regexFeatures:
		compiled[regex] = re.compile(regex)

	# list of all tags
	allTags = emissions.keys()

	# list of sequences
	# each sequence is a Python list containing the words in the sequence
	sequences = parseSequences("../dev.in")
	logTransmissions = {}
	for key1 in transmissions:
		logTransmissions[key1] = {}
		for key2 in transmissions[key1]:
			logTransmissions[key1][key2] = {}
			for key3 in transmissions[key1][key2]:
				logTransmissions[key1][key2][key3] = math.log(transmissions[key1][key2][key3])
	logEmissions = {}
	for key1 in emissions:
		logEmissions[key1] = {}
		for key2 in emissions[key1]:
			logEmissions[key1][key2] = math.log(emissions[key1][key2])

	# output sequences corresponding to input sequences
	outputs = []

	progress = 0
	for sequence in sequences:
		dpTable = {
			"__START":{
				"__START": ViterbiSequence("__START", "__START")
			}
		}
		for i in range(-1, len(sequence) -1):
			newDpTable= {}
			for key1 in dpTable:
				for key2 in dpTable[key1]:
					print i, key1, key2
					if not key2 in newDpTable:
						newDpTable[key2] = {}
					allNone = True
					for tag in transmissions[key2]:
						positionMax = None
						maxChoice = None
						piValue = dpTable[key1][key2].probTransmission(tag, sequence[i +1])
						if piValue >= positionMax:
							positionMax = piValue
							maxChoice = dpTable[key1][key2]
							if piValue != None:
								allNone = False
						newDpTable[key2][tag] = maxChoice.transit(tag,sequence[i +1])
					if allNone:
						for tag in allTags:
							positionMax = None
							maxChoice = None
							piValue = dpTable[key1][key2].probTransmission(tag, sequence[i +1])
							if piValue >= positionMax:
								positionMax = piValue
								maxChoice = dpTable[key1][key2]
								if piValue != None:
									allNone = False
							newDpTable[key2][tag] = maxChoice.transit(tag,sequence[i +1])
				dpTable = newDpTable
		endingMax = None
		endMaxChoice = None
		for key1 in dpTable:
			for key2 in dpTable[key1]:
				piValue = dpTable[key1][key2].probTransmission("__END", None)
				if piValue >= endingMax:
					endingMax = piValue
					endMaxChoice = dpTable[key1][key2]
		endingState = endMaxChoice.transit("__END", None)
		outputs.append(endingState)
		progress += 1
		print progress 
		viterbiTagger(outputs, "../dev.in", "p5_viterbi_2nd_order.txt")
	os.system("diff -u " + "p5_viterbi_test.txt " + "../dev.out" + ">difference_2nd_order.txt")
	print accuracy("p5_viterbi_2nd_order", "../dev.out")