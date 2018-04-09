import re

def replaceStr(filename, regexStr, replacementStr):
	"""
	If a line, in the file called 'filename', matches the regex specified with 'regexStr' is replaced 
	with the string indicated in replacementStr
	"""
	with open(filename, "r") as file:
		lines = file.readlines()

	for i,line in enumerate(lines):
		# Better to rise an exception if this is never accessed
		if re.match(regexStr, line):
			lines[i] = replacementStr

	with open(filename, "w") as file: 
		file.writelines(lines)  


def getListfromRegex(regexStr, lineStr):
	return re.findall(regexStr, lineStr)