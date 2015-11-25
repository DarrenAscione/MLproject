# model parameters
transmissions = {}
emissions = {}

# list of all tags
allTags = []

# list of sequences
sequences = []

class ViterbiSequence:
	def __init__(self, lastTag):
		self.sequence = [lastTag]
		self.probability = 1.0
	def probTransmission(self, nextTag, nextEmission):
		lastTag = self.sequence[-1]
		return self.probability * transmissions[lastTag][nextTag] * emissions[nextTag][nextEmission]
	def transit(self, nextTag, nextEmission):
		nextStep = copy.deepcopy(self)
		nextStep.probability *= nextStep.probTransmission(nextTag, nextEmission)
		nextStep.sequence.append(nextTag)
		return nextStep

for sequence in sequences:
	dpTable = [ViterbiSequence(START)]
	for i in len(sequence):
		newDpTable= []
		for tag in allTags:
			positionMax = -1
			maxChoice = None
			for dpEntry in dpTable:
				piValue = dpEntry.probTransmission(tag, sequence[i +1])
				if piValue > positionMax:
					positionMax = piValue
					maxChoice = dpEntry
			newDpRow.append(maxChoice.transit(tag,sequence[i +1]))
		dpTable = newDpTable
	print dpTable[0].sequence