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
sequences = [["a", "d"], ["c", "b"]]

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

for sequence in sequences:
	dpTable = [ViterbiSequence("START")]
	for i in range(-1, len(sequence) -1):
		newDpTable= []
		for tag in allTags:
			positionMax = -1
			maxChoice = None
			for dpEntry in dpTable:
				piValue = dpEntry.probTransmission(tag, sequence[i +1])
				if piValue > positionMax:
					positionMax = piValue
					maxChoice = dpEntry
			newDpTable.append(maxChoice.transit(tag,sequence[i +1]))
		dpTable = newDpTable
		
	endingMax = -1
	endMaxChoice = None
	for dpEntry in dpTable:
		piValue = dpEntry.probTransmission("END", None)
		if piValue > endingMax:
			endingMax = piValue
			endMaxChoice = dpEntry
	outputs.append(endMaxChoice.transit("END", None))

print outputs[0].sequence, outputs[0].probability