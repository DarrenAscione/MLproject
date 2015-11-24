inFile = open("train", "r")
outFile = open("allPOS", "w")

tags = {}
for line in inFile:
	line = line.strip()
	if len(line) <= 0:
		continue
	else:
		tag = line.split(" ")[1]
		if not (tag in tags):
			tags[tag] = tag

for tag in tags:
	outFile.write(tag + "\n")

inFile.close()
outFile.close()