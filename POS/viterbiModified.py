import copy
START = "START"
# model parameters
transmissions = {
				"START": {
						"X": 0.5,
						"Z": 0.5,
					},
				"X": {
						"X": 0.33,
						"Z": 0.33,
						"END": 0.33,
					},
				"Y": {
						"X": 0.25,
						"END": 0.75,
					},
				"Z": {
						"X": 1.0 / 7,
						"Y": 4.0 / 7,
						"Z": 1.0 / 7,
						"END": 1.0 / 7,
					}
				}
emissions = {
				"X": {
						"a": 3.0/7,
						"b": 2.0/7,
						"c": 2.0/7,
					},
				"Y": {
						"a": 0.5,
						"c": 0.25,
						"d": 0.25,
					},
				"Z": {
						"a": 1.0/7,
						"b": 4.0/7,
						"c": 1.0/7,
						"d": 1.0/7,
					}
			}

# list of all tags
allTags = ["X", "Y", "Z"]

# list of sequences
# each sequence is a Python list containing the words in the sequence
sequences = [["a", "d", "a", "d", "a", "d"]]

# output sequences corresponding to input sequences
outputs = []
class ViterbiSequence:
	def __init__(self, lastTag):
		self.sequence = [lastTag]
		self.probability = 1.0
	
	def probTransmission(self, nextTag, nextEmission):
		lastTag = self.sequence[-1]
		try:
			if nextEmission == None:
				return self.probability * transmissions[lastTag][nextTag]	
			return self.probability * transmissions[lastTag][nextTag] * emissions[nextTag][nextEmission]
		except KeyError:
			return 0
	def transit(self, nextTag, nextEmission):
		nextStep = copy.deepcopy(self)
		nextStep.probability = nextStep.probTransmission(nextTag, nextEmission)
		nextStep.sequence.append(nextTag)
		return nextStep
	def __str__(self):
		return str(self.sequence)

# list of top 10 sequences ending in a particular node
class ViterbiNodeList:
	def __init__(self):
		self.queuePointer = 0
		self.nodeList = []
	def __str__(self):
		return str([str(i) for i in self.nodeList])
	def push(self, sequence):
		if not self.shouldPush(sequence):
			return
		if len(self.nodeList) >= 10:
			self.nodeList = self.nodeList[:-1]
		self.nodeList.append(sequence)
		self.nodeList.sort(key = lambda x: -(x.probability))
	def shouldPush(self, sequenceProbability):
		if len(self.nodeList) < 10:
			return True
		elif sequenceProbability == None:
			return False
		elif sequenceProbability > self.nodeList[-1]:
			return True
		elif sequenceProbability <= self.nodeList[-1]:
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

for sequence in sequences:
	firstDpEntry = ViterbiNodeList()
	firstDpEntry.push(ViterbiSequence("START"))
	dpTable = [firstDpEntry]
	for i in range(-1, len(sequence) -1):
		# every entry in the table is a ViterbiNodeList containing the top 10 sequences ending in a certain tag
		newDpTable= []
		for tag in allTags:
			# initialise a new ViterbiNodeList for each tag
			newDpEntry = ViterbiNodeList()
			# for every node list in the table
			for dpEntry in dpTable:
				while dpEntry.peek() != None:
					if newDpEntry.shouldPush(dpEntry.peek().probTransmission(tag, sequence[i + 1])):
						# pop off the top entry from the original DP table
						popped = dpEntry.pop()
						newDpEntry.push(popped.transit(tag, sequence[i + 1]))
						hasValidSequences = True
					else:
						break
				dpEntry.reset()
			newDpTable.append(newDpEntry)
		dpTable = newDpTable
	lastNodeList = ViterbiNodeList()
	for dpEntry in dpTable:
		while dpEntry.peek() != None:
			if newDpEntry.shouldPush(dpEntry.peek().probTransmission("END", None)):
				# pop off the top entry from the original DP table
				lastNodeList.push(dpEntry.pop().transit("END", None))
				hasValidSequences = True
			else:
				break
	outputs.append(lastNodeList)

print outputs[0]