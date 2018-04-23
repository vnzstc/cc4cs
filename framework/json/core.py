import os, subprocess, json, csv
from shutil import rmtree
from inputgenerator import searchRegex

# Gets the needed directories 
scriptPath = os.path.dirname(os.path.realpath(__file__))
frameworkPath = os.path.dirname(scriptPath)
prjPath = os.getcwd()

microList = []


def removeDir(dirName):
	"""
		Removes the directory specified in dirName
	"""
	if os.path.isdir(dirName):
		rmtree(dirName)

def createDir(dirName):
	os.makedirs(dirName)

# ----------------------------------------------------
def returnListFiles(topDir):
	return [f for f in os.listdir(topDir) if os.path.isfile(os.path.join(topDir, f))]

def returnListDir(topDir):
	return [f for f in os.listdir(topDir) if os.path.isdir(os.path.join(topDir, f))]
# ---------------------------------------------------

def getExtensionFilename(fileName):
	"""
		Given the file name, returns a list containing the file name without the extension and this one
	"""
	return os.path.splitext(fileName)

def mvFiles(destination, listFileName):
	if os.path.isdir(destination):	
		for fileName in listFileName:
			os.rename(fileName, destination + fileName)

def writeTuple(label, value, writerId):
	writerId.writerow([label, value])

def mvAllFiles(destination):
	"""
		Moves all files except those with extension .c and .csv in the indicated directory "destination"
	"""
	print("moveAllFiles " + destination)
	if os.path.isdir(destination):	
		for fileName in returnListFiles(prjPath):
			if getExtensionFilename(fileName)[1] != ".c" and getExtensionFilename(fileName)[1] != '.csv':
				os.rename(fileName, destination + fileName)

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
		global frameworkData
		frameworkData = json.load(jsonFile)

		for line in frameworkData:
			microList.append(line)

		printMicroprocessors()
		microId = input('\nInsert the identifier of a microprocessor: ')
		if int(microId) >= len(frameworkData):
			raise ValueError("The id doesn't exist")

		chosenMicro = microList[int(microId)]
		print(frameworkData[chosenMicro])

		return chosenMicro
	
def parseGcovOutput(txtFilePath):
	result = 0
	with open(txtFilePath + ".c.gcov", "r") as file:
		for line in file:
			number = line.split(':')[0]
			number = number.strip()
			if number.isdigit():
				result += int(number)

	return result

def parseSimulationOutput(simFileName):
	"""
		Generic parsing for a simulation output file 
		TODO: Not Generic, it works only with the micros already tested
	"""
	with open(simFileName) as execFile:
		content = execFile.read()
		cycleStr = searchRegex(r'([cC]ycles.*?:\s*)(\d+)', content)
		
		return cycleStr.group(2)

def createFileWriter(fileDescriptor):
	return csv.writer(fileDescriptor, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)

"""
	Command Execution Phase 
"""

def splitBySpace(customString):
	return customString.split(" ")

def expandCommand(reducedCommand, directory = None):
	expandendCommand = reducedCommand

	if '[programName]' in reducedCommand:
		expandendCommand = expandendCommand.replace('[programName]', 'prova')

	if '[prjPath]' in reducedCommand:
		expandendCommand = expandendCommand.replace('[prjPath]', prjPath + '/')

	if '[scriptPath]' in reducedCommand:
		expandendCommand = expandendCommand.replace('[scriptPath]', scriptPath)

	if '[directoryName]' in reducedCommand:
		expandendCommand = expandendCommand.replace('[directoryName]', directory)

	return expandendCommand

def getOutputFilename(commandString):
	print("getOut:", commandString)
	outputFilename = searchRegex(r'\{(.*?)\}', commandString)

	if outputFilename != None:
		return outputFilename.group(1)
	return None

def executeCommandSet(inputFilename, resultFile, microName):
	with open(resultFile, 'w') as outputFile:
		fileWriter = createFileWriter(outputFile)
		commandSet = frameworkData[microName]
		commandList = splitBySpace(commandSet["dependencies"])

		for directory in returnListDir('includes'):
			for command in commandList:
				commandStr = commandSet[command]

				expandedStr = expandCommand(commandStr, directory)
				flags = splitBySpace(expandedStr)

				outputFilename = getOutputFilename(expandedStr)

				print(flags)
				if outputFilename != None:

					flags.remove('{' + outputFilename + '}')

					print(flags)
					with open(outputFilename, 'w') as execFile:
						subprocess.call(flags, stdout=execFile)
				else:
					subprocess.call(flags)

			if microName == 'profiling':
				outputPath = 'profiling/' + directory + '/'
				createDir(outputPath)
				value = parseGcovOutput(inputFilename)
			else:
				outputPath = 'simulation/' + directory + '/'
				createDir(outputPath)
				#---- CRITICAL: TO BE CHECKED 
				value = parseSimulationOutput(outputFilename)
			
			# ----------------------------------------------
			writeTuple(directory, value, fileWriter)
			mvAllFiles(outputPath)
			# ----------------------------------------------
"""
CC4CS Calculation and Plotting
"""

def calculateMetric(cyclesFilename, statementsFilename):

	with open(cyclesFilename) as cyclesFile, open(statementsFilename) as statementsFile, open("cc4csValues.csv", "w") as outputFile:
		cyclesContent = csv.reader(cyclesFile)
		statementsContent = csv.reader(statementsFile)
		fileWriter = createFileWriter(outputFile)

		for (c1, c2) in zip(cyclesContent, statementsContent):
			cc4csValue = (int(c1[1]) / int(c2[1]))
			writeTuple(c1[0], "%.3f" %  cc4csValue, fileWriter)