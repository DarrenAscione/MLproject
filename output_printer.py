def output_to_file(emission, file_write, mode="normal"):
	if mode == "readable":
		with open(file_write, "a") as file:
			for key in emission.keys():
				file.write("\n ------------------------------------- \n")
				file.write("Emission State: %s\n"%(key))
				for words in emission[key].keys():
					file.write("%s: %f\n"%(words, emission[key][words]))
				file.write("\n ------------------------------------- \n")
	elif mode == "state":
		with open(file_write, "a") as file:
			for key in emission.keys():
				file.write("%s %f\n"%(key, emission[key]))
	else:
		with open(file_write, "a") as file:
			for key in emission.keys():
				for words in emission[key].keys():
					if emission[key][words] != 0:
						file.write("%s %s %f\n"%(key,words, emission[key][words]))

def tagger(predicts, file_write):
	with open(file_write, "a") as file:
			for keys in predicts.keys():
				file.write("%s %s\n"%(keys,predicts[keys]))
