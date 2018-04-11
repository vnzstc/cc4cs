import os, subprocess, json, csv
from shutil import rmtree
from preprocessor import getListfromRegex

# Gets the script directory 
scriptPath = os.path.dirname(os.path.realpath(__file__))
frameworkPath = os.path.dirname(scriptPath)
microList = []

"""
def getBinPath():
	return frameworkPath + "/bin" 
"""

def createDir(dirName):
	os.makedirs(dirName)

def returnListDir(topDir):
	return os.listdir(topDir)

def getExtensionFilename(fileName):
	"""
		Given the file name, returns a list containing the file name without the extension and this one
	"""
	return os.path.splitext(fileName)

def mvFiles(destination, listFileName):
	if os.path.isdir(destination):	
		for fileName in listFileName:
			os.rename(fileName, destination + fileName)

def deletePreviousComputation():
	"""
		Removes the directories created by previous computations
	"""
	if os.path.isdir('includes'):
		rmtree('includes')

	if os.path.isdir('profiling'):
		rmtree('profiling')

	if os.path.isdir('results'):
		rmtree('results')

	if os.path.isdir('simulation'):
		rmtree('simulation')

def printMicroprocessors():
	"""
		Function that prints the list of known microprocessors
	"""
	print("List of available microprocessors:\n")
	for i, ele in enumerate(microList):
		print('(' + str(i) + ') ' + ele)

def chooseMicro():
	"""
		Reads the available microprocessors from a json file and allows the user to choose one
		Return: a dictionary that contains ISS and compiler used by the chosen microprocessor
	"""
	with open(scriptPath + '/micros.json', 'r') as jsonFile:
		frameworkData = json.load(jsonFile)

		for line in frameworkData:
			microList.append(line)

		printMicroprocessors()
		
		microId = input('\nInsert the identifier of a microprocessor: ')
		if int(microId) >= len(frameworkData):
			raise ValueError("The id doesn't exist")

		chosenMicro = microList[int(microId)]

		print(frameworkData)
		# A dictionary that contains the instruction set simulator and the compiler flags specified
		# for the chosen micro
		return frameworkData[chosenMicro]

def compileProgram(filePath, tracePath, flags):
	"""
		This function is needed to compile a couple (algorithm + the trace) with a gcc based compiler
	"""
	cmd = []
	flagList = flags.split(" ")	
	cmd.extend([flagList[0], filePath + ".c"])
	cmd.extend(flagList[1:])
	cmd.extend(["-Iincludes", "-I" + tracePath, "-o", filePath])
	subprocess.call(cmd)

def executeProgram(flags):
	flagList = flags.split(" ")

	# File created to store the output of an execution 
	with open('executionOutput.txt', 'w') as execFile:
		subprocess.call(flagList, stdout=execFile)

def parseGcovOutput(txtFilePath):
	result = 0
	with open(txtFilePath, "r") as file:
		for line in file:
			number = file.readline().split(':')[0]
			number = number.strip()
			if number.isdigit():
				result += int(number)

	return result

def parseSimulationOutput():
	"""
		Generic parsing for a simulation output file 
		TODO: Not Generic, it works only with the simulavr output, for now ;)
	"""
	with open('executionOutput.txt') as execFile:
		content = execFile.read()
		cycleStr = getListfromRegex(r'[cC]ycles.*?\d+', content)[0]
		
		return getListfromRegex(r'\d+', cycleStr)[0] 

def createFileWriter(fileDescriptor):
	return csv.writer(fileDescriptor, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)

def writeTuple(label, value, writerId):
	writerId.writerow([label, value])

def createFileReader(fileDescriptor):
	return csv.reader(fileDescriptor, delimiter=',', quotechar='|')

def cc4csCalculator():
	with open("cStatements.csv", "r") as inputFile1:
		cStatementsDict = dict(createFileReader(inputFile1))

	# print(cStatementsDict)
	
	with open("clockCycles.csv", "r") as inputFile2, open("cc4csValues.csv", "w") as outputFile:
		valuesWriter = createFileWriter(outputFile)

		for element in createFileReader(inputFile2):
			directory = element[0]
			cc4csValue = "%0.3f" % (int(element[1]) / int(cStatementsDict[directory]))
			writeTuple(directory, cc4csValue, valuesWriter)