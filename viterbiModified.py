import copy, math, string
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

def viterbiTagger(outputs, inFilename, outFilename, rank, tags=True):
	inFile = open(inFilename, "r")
	inFileLines = inFile.readlines()
	inFile.close()
	outFile = open(outFilename, "w")
	inFilePointer = 0
	for output in outputs:
		for tag in output.nodeList[rank].sequence[1:-1]:
			line = inFileLines[inFilePointer].strip()
			if tags:
				line = line.split(" ")[0]
			outFile.write("{0} {1}\n".format(line, tag))
			inFilePointer += 1
		outFile.write("\n")
		inFilePointer += 1
	outFile.close()

START = "__START"
END = "__END"
transmissionFileName = "POS/transition.txt"
emissionsFileName = "POS/emission_testing.txt"
sequenceFileName = "POS/dev.in"
outputFileFormat = "POS/Part 4/p4_viterbi_{0}.txt"

if __name__ == "__main__":
	class ViterbiSequence:
		def __init__(self, lastTag):
			self.sequence = [lastTag]
			self.logProbability = 0.0
		def probTransmission(self, nextTag, nextEmission):
			lastTag = self.sequence[-1]
			try:
				if self.logProbability == None:
					return None
				if nextEmission == None:
					return self.logProbability + logTransmissions[lastTag][nextTag]	
				return self.logProbability + logTransmissions[lastTag][nextTag] + logEmissions[nextTag][nextEmission]
			except KeyError:
				return None
		def transit(self, nextTag, nextEmission):
			nextStep = copy.deepcopy(self)
			nextStep.logProbability = nextStep.probTransmission(nextTag, nextEmission)
			nextStep.sequence.append(nextTag)
			return nextStep

	# list of top 10 sequences ending in a particular node
	class ViterbiNodeList:
		def __init__(self):
			self.queuePointer = 0
			self.nodeList = []
		def __str__(self):
			return str([str(i) for i in self.nodeList])
		def push(self, sequence):
			if not self.shouldPush(sequence.logProbability):
				print sequence.logProbability
				raise ValueError("attempted to push invalid value")
				return False
			if len(self.nodeList) >= 10:
				self.nodeList = self.nodeList[:-1]
			self.nodeList.append(sequence)
			self.nodeList.sort(key = lambda x: x.logProbability, reverse=True)
			return True
		def shouldPush(self, sequenceProbability):
			if len(self.nodeList) < 10:
				return True
			elif sequenceProbability > self.nodeList[-1].logProbability:
				return True
			elif sequenceProbability <= self.nodeList[-1].logProbability:
				return False
		def peek(self):
			if self.queuePointer >= len(self.nodeList):
				return None
			return self.nodeList[self.queuePointer]
		def pop(self):
			retVal = self.peek()
			if retVal != None:
				self.queuePointer += 1
			return retVal
		def reset(self):
			self.queuePointer = 0
	

	# model parameters
	transmissions = parseFile(transmissionFileName)
	emissions = parseFile(emissionsFileName)

	# list of all tags
	allTags = emissions.keys()
	# list of sequences
	# each sequence is a Python list containing the words in the sequence
	sequences = parseSequences(sequenceFileName)

	logTransmissions = {}
	for key1 in transmissions:
		logTransmissions[key1] = {}
		for key2 in transmissions[key1]:
			logTransmissions[key1][key2] = math.log(transmissions[key1][key2])

	logEmissions = {}
	for key1 in emissions:
		logEmissions[key1] = {}
		for key2 in emissions[key1]:
			logEmissions[key1][key2] = math.log(emissions[key1][key2])

	# output sequences corresponding to input sequences
	outputs = []

	for sequence in sequences:
		firstDpEntry = ViterbiNodeList()
		firstDpEntry.push(ViterbiSequence(START))
		dpTable = [firstDpEntry]
		for i in range(-1, len(sequence) -1):
			# every entry in the table is a ViterbiNodeList containing the top 10 sequences ending in a certain tag
			newDpTable= []
			for tag in allTags:
				# initialise a new ViterbiNodeList for each tag
				newDpEntry = ViterbiNodeList()
				# for every node list in the table
				for dpEntry in dpTable:
					popped = dpEntry.pop()
					while popped != None:
						if newDpEntry.shouldPush(popped.probTransmission(tag, sequence[i + 1])):
							newDpEntry.push(popped.transit(tag, sequence[i + 1]))
							popped = dpEntry.pop()
						else:
							# print "broke"
							break
					dpEntry.reset()
				newDpTable.append(newDpEntry)
			dpTable = newDpTable
		lastNodeList = ViterbiNodeList()
		for dpEntry in dpTable:
			popped = dpEntry.pop()
			while popped != None:
				if lastNodeList.shouldPush(popped.probTransmission(END, None)):
					lastNodeList.push(popped.transit(END, None))
					# pop off the top entry from the original DP table
					popped = dpEntry.pop()
				else:
					break
			dpEntry.reset()
		outputs.append(lastNodeList)
		if len(lastNodeList.nodeList) != 10:
			print len(lastNodeList.nodeList)

	for i in range(10):
		viterbiTagger(outputs, sequenceFileName, outputFileFormat.format(i), i, False)	