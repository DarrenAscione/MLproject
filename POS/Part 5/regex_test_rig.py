import featureFinder, re

for regex in featureFinder.REGEXES:
	if re.compile(regex).match("noting"):
		print regex