import os, subprocess, json, csv, fnmatch
from shutil import rmtree
from inputgenerator import searchRegex

# Gets the needed directories 
scriptPath = os.path.dirname(os.path.realpath(__file__))
frameworkPath = os.path.dirname(scriptPath)
prjPath = os.getcwd()

microList = []

def setCurrentFile(filename):
	"""Sets the global variable that indicates the current program that is under analysis
	
	Args:
		filename (string): the filename of the c program 
	"""
	global currentFilename
	currentFilename = filename

def removeDir(dirName):
	"""Removes the specified directory
	
	Args:
		dirName (string): the name of the directory to delete
	"""
	if os.path.isdir(dirName):
		rmtree(dirName)

def createDir(dirName):
	"""Creates the specified directory in the working directory
	
	Args:
		dirName (string): the name of the directory to create
	"""
	os.makedirs(dirName)

def findFileByExtension(directory, extension):
	"""
	Find the files with the specified extension.

	Args:
		directory: indicates the directory in which the file has to be searched
		extension: indicates the extension of the file

	Returns:
		list: the list of elements with the specified extension else None 
	"""
	fileList = returnListFiles(directory)
	results = []

	for element in fileList:
		# the asterisk is needed to indicate 
		if fnmatch.fnmatch(element, '*' + extension):
			results.append(element)

	return results


# ----------------------------------------------------
def returnListFiles(topDir):
	return [f for f in os.listdir(topDir) if os.path.isfile(os.path.join(topDir, f))]

def returnListDir(topDir):
	return [f for f in os.listdir(topDir) if os.path.isdir(os.path.join(topDir, f))]
# ---------------------------------------------------

def getExtensionFilename(filename):
	"""Extracts the extension from the filename
	
	Args:
		filename (string): the name of the file to be processed
	
	Returns:
		list: a list of two elements containing the filename and his extension
	"""
	return os.path.splitext(filename)

def mvFiles(destination, listFilename):
	if os.path.isdir(destination):	
		for filename in listFilename:
			os.rename(filename, destination + filename)

def writeTuple(label, value, writerId):
	"""Writes a tuple (label, value) in a file
	
	Args:
		label (string): label to be written in the file
		value (string): value to be written in the file
	"""
	writerId.writerow([label, value])

def mvAllFiles(destination):
	"""Moves all files except those with extension .c and .csv in the indicated directory 

	Args:
		destination (string): the path of the directory in which the files have to be moved
	"""
	print("moveAllFiles " + destination)
	if os.path.isdir(destination):	
		for filename in returnListFiles(prjPath):
			if getExtensionFilename(filename)[1] != ".c" and getExtensionFilename(filename)[1] != '.csv':
				os.rename(filename, destination + filename)

def printMicroprocessors():
	"""Function that prints the list of known microprocessorss
	"""
	print("List of available microprocessors:\n")
	for i, ele in enumerate(microList):
		print('(' + str(i) + ') ' + ele)

def chooseMicro():
	"""Reads the available microprocessors from a json file and allows the user to choose one
	
	Returns: 
		string: the name of the chosen microprocessor
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
	
def parseGcovOutput():
	"""Analyzes the output of GCov profiler 

	Args:
		txtfilePath (string): the name of the .c.gcov file.

	Returns: 
		int: the number of executed C statements
	"""
	result = 0
	with open(currentFilename + ".c.gcov", "r") as file:
		for line in file:
			number = line.split(':')[0]
			number = number.strip()
			if number.isdigit():
				result += int(number)

	return result

def parseSimulationOutput(simFilename):
	"""Generic parsing for a simulation output file 

	Args:
		simFilename (string):  the name of the file that contains simulation information

	Returns:
		string: number of clock cycles

	Todo: 
		* Not Generic, it works only with the micros already tested
	"""
	with open(simFilename) as execFile:
		content = execFile.read()
		cycleStr = searchRegex(r'([cC]ycles.*?:\s*)(\d+)', content)
		
		return cycleStr.group(2)

def createFileWriter(fileDescriptor):
	"""Prepares a file to be written that uses the comma as delimiter
	
	Args:
		fileDescription (obj): the object that represents a file

	Returns:
		obj: writer object responsible for converting the user’s data into delimited strings on the given file-like object
	"""
	return csv.writer(fileDescriptor, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)

def splitBySpace(customString):
	"""Function used to split a string that contains spaces 
	
	Args:
		customString (string): the string to be split

	Returns: 
		list: the list that contains the elements separated by a space
	"""
	return customString.split(" ")


def expandCommand(reducedCommand, directory = None):
	"""Replaces the placeholder, inserted in .json file, with the appropriate values

	Args:
		reducedCommand (string): the string with the placeholders 
		directory (string, optional):  a string that contains a directory path. Defaults to None.

	Returns:
		string: the expanded string 
	"""
	expandendCommand = reducedCommand

	# ----------------------------------------------
	if '[programName]' in reducedCommand:
		expandendCommand = expandendCommand.replace('[programName]', currentFilename)

	if '[prjPath]' in reducedCommand:
		expandendCommand = expandendCommand.replace('[prjPath]', prjPath + '/')

	if '[scriptPath]' in reducedCommand:
		expandendCommand = expandendCommand.replace('[scriptPath]', scriptPath)

	if '[directoryName]' in reducedCommand:
		expandendCommand = expandendCommand.replace('[directoryName]', directory)
	# ----------------------------------------------

	return expandendCommand

def getOutputFilename(commandString):
	"""Searches for the placeholder that indicates the output file

	Args:
		commandString (string): 

	Examples:
		Output File placeholder: {content.format}  

	Returns: 
		string: if present, the content of the output file placeholder otherwise None
	"""
	outputFilename = searchRegex(r'\{(.*?)\}', commandString)

	if outputFilename != None:
		return outputFilename.group(1)
	return None

def executeCommandSet(resultFile, microName):
	"""Executes the set of commands incated under microName label in the .json file

	Args:	
		filename (string): the filename of the c program
		resultFile (string): the file in which are stored the information about the execution 
		microName (string): the label of the .json file 

	Todo:
		* delete filename parameter
		* insert comments in the algorithm
	"""
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

					# ---------------------------------------
					flags.remove('{' + outputFilename + '}')
					# ---------------------------------------
					
					print(flags)
					with open(outputFilename, 'w') as execFile:
						subprocess.call(flags, stdout=execFile)
				else:
					subprocess.call(flags)

			if microName == 'profiling':
				outputPath = 'profiling/' + directory + '/'
				createDir(outputPath)
				value = parseGcovOutput()
			else:
				outputPath = 'simulation/' + directory + '/'
				createDir(outputPath)
				value = parseSimulationOutput(outputFilename)
			
			# ----------------------------------------------
			writeTuple(directory, value, fileWriter)
			mvAllFiles(outputPath)
			# ----------------------------------------------
"""
CC4CS Calculation and Plotting
"""

def calculateMetric(cyclesFilename, statementsFilename):
	"""Analyzes the content of the files with the clock cycles, used by the microprocessoe, and the number of C statements.

	Args:
		cyclesFilename (string): path of the file obtained from the simulation phase
		statementsFilename (string): path of the file obtained from the profiling phase
	"""
	with open(cyclesFilename) as cyclesFile, open(statementsFilename) as statementsFile, open("cc4csValues.csv", "w") as outputFile:
		cyclesContent = csv.reader(cyclesFile)
		statementsContent = csv.reader(statementsFile)
		fileWriter = createFileWriter(outputFile)

		for (c1, c2) in zip(cyclesContent, statementsContent):
			cc4csValue = (int(c1[1]) / int(c2[1]))
			writeTuple(c1[0], "%.3f" %  cc4csValue, fileWriter)