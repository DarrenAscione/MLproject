def accuracy(original_file, predicted_file):
	count = 0
	originals = tag_extractor(original_file)
	predicted = tag_extractor(predicted_file)
	for tag in xrange(len(originals)):
		if originals[tag] == predicted[tag]:
			count += 1
	return (count *1.0)/ len(predicted)