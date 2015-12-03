def checkTransition(fileName):
	inFile = open(fileName, "r")
	fileLines = inFile.readlines()
	inFile.close()
	checkList = {}
	for line in fileLines:
		lineArray = line.strip().split(" ")
		if not lineArray[0] in checkList:
			checkList[lineArray[0]] = 0.0
		checkList[lineArray[0]] += float(lineArray[2])
	print checkList

checkTransition("emission_training.txt")
