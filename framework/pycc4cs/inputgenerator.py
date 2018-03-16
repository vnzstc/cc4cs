import sys, mmap, re
import random as rn
from itertools import product
from functools import reduce
import os

scalars = {}
arrays = {}
sizes = {}

def getListfromRegex(regexStr, lineStr):
	return re.findall(regexStr, lineStr)

def initializeSizes(variable):
	matched = getSizes(variable)
	if matched:
		arrays[variable] = ""

		for element in matched:
			sizes[element] = ""
		return True

	return False

def getSizes(variable):
	return getListfromRegex(r'\[(.*?)\]', variable)
"""
Given a list of parameters, returns the name of each element
Divides the latters looking at the type (scalar or not)
"""
def parametersFilter(lineStr):
	global scalars
	tempScalars = []
	matched = getListfromRegex(r'\w+\s\w+(?:\[\w+\]){0,2}', lineStr.decode("utf-8"))
	
	for i, variable in enumerate(matched):
		index = variable.index(' ')
		varName = variable[index+1:]

		if not initializeSizes(varName):
			tempScalars.append(varName)

	scalars = {variable : "" for variable in set(tempScalars) - set(sizes.keys())}

def insertInput(variable, regexStr):
	inputStr = input('Enter input for '  + '"' + variable + '"' + ': ')

	if not re.match(regexStr, inputStr):
		raise ValueError("Bad input for " + inputStr)
	return inputStr
""" 
For each parameter, asks to re.match('\[(\d,\d)\]', input_str)	- a range used to generate random values between min and max
	- the number of inputs to create, for scalar variable
"""
def askForInputs():
	print("- Enter a range [min,max] for array variables\n"+
		  "- Enter a range [min,max];inputs for scalar variables\n")

	for variable in scalars:
		scalars[variable] = insertInput(variable, r'\[\d+,\d+\];[1-9][0-9]*')

	for variable in sizes:
		sizes[variable] = insertInput(variable, r'\[\d+,\d+\];[1-9][0-9]*')

	for variable in arrays:
		arrays[variable] = insertInput(variable, r'\[\d+,\d+\]$')
"""
This function opens a .c program, searches for a function with the same name of the file
in which are defined the parameters that the function takes in input
"""
def discoverParameters(filename):
	file = open(filename + '.c')
	mm = mmap.mmap(file.fileno(), 0, access = mmap.ACCESS_READ)
	index = mm.find(str.encode(filename))

	if index != -1:
		mm.seek(index)
		parametersFilter(mm.readline())
		askForInputs()
	else:
		raise ValueError("function not found")
"""
	For each scalar variable in "ranges" dictionary, generates a list that contains the values to 
	write in each output file.
"""
def splitScalarInput(rangeStr):
	currentInput = rangeStr.split(';')
	vaRange = eval(currentInput[0])
	vaNum = int(currentInput[1])

	return (vaRange, vaNum)

def genRandomList(rangeMin, rangeMax, elementNum, varType):
	lst = [round(rn.uniform(rangeMin, rangeMax), 3) for _ in range(elementNum)]

	if varType != "float":
		return [int(element) for element in lst]

	return lst

def generateListForScalars(lst, varType):
	for variable in lst:
		currentTuple = splitScalarInput(lst[variable])
		lst[variable] = genRandomList(currentTuple[0][0], currentTuple[0][1], currentTuple[1], varType)

	return lst

def listCreator(varType):
	generateListForScalars(scalars, varType)
	generateListForScalars(sizes, "int8_t")
"""
	This function creates the output file.
	Returns the object that rappresents the file
"""
def createHeader():
	basic = "#ifndef VALUES\n#define VALUES\n"

	output = open('values.h', 'w+')
	output.write(basic)

	return output

def closeHeader(fileObject):
	fileObject.write("#endif")
	fileObject.close()


def removeLastOccurence(character, string):
	k = string.rfind(character)
	string = string[:k] + "" + string[k+1:]
	return string

def writeArray(headerFile, value, varType, arraySizes):
	arrayRange = eval(value)
	elementNum = reduce(lambda x, y: x*y, arraySizes)

	toWrite = "{"
	for i in range(0, arraySizes[0]):
		arrayValues = genRandomList(arrayRange[0], arrayRange[1], elementNum, varType)
		try:
			for j in range(0, arraySizes[1]):
				if j == 0:
					toWrite += "{"
				toWrite += str(arrayValues[j]) + ","
			toWrite = removeLastOccurence(',', toWrite)
			toWrite += "},"	
		
		except Exception as e:
				toWrite += str(arrayValues[i]) + ","

	toWrite = removeLastOccurence(',', toWrite)
	toWrite += "};\n"

	headerFile.write(toWrite)

"""
	This function writes variables in the output file.
"""
def writeVariables(combination, headerFile, varType):
	cont = 0
	currentSizeValues = {}

	for key, value in scalars.items():
		pos = combination[cont]
		headerFile.write("\t" + varType + " " + key + " = " + str(value[pos]) + ";\n")
		cont += 1

	for key,value in sizes.items():
		pos = combination[cont]
		headerFile.write("\tenum{ " + key + " = " + str(value[pos]) + " };\n")	
		currentSizeValues.update({key : value[pos]})
		cont += 1

	for key, value in arrays.items():
		matched = getSizes(key)
		currentSizes = [currentSizeValues[element] for element in matched]
		headerFile.write("\t" + key + " = ")
		writeArray(headerFile, value, varType, currentSizes)
""" 
	This function generates combinations of the values of previously calculated lists.
	Combines indexes and then accesses by index, the correspondent list, to get the value.
	Furthermore, for each header a directory is created 
"""
def generateHeaders(varType):
	counts = [len(singleList) for singleList in list(scalars.values()) + list(sizes.values())]
	iterate = [range(length) for length in counts]
	fileIndex = 0

	# Includes directory creation 
	os.makedirs("includes")
	# Change working directory
	os.chdir("includes")

	for combination in product(*iterate):
		# For each combination will be generated 10 random array
		for index in range(1):
			# Creates the directory in which the header will be placed 
			dirName = "values_" + str(fileIndex) + str(index)
			os.makedirs(dirName)

			headerFile = createHeader()
			writeVariables(combination, headerFile, varType)
			closeHeader(headerFile)

			# Moves the file in the above created directory  
			os.rename("values.h", dirName + "/values.h")
				
		fileIndex += 1

	# Return to the previous directory
	os.chdir('..')