import os, subprocess, json, csv, fnmatch
from shutil import rmtree
from inputgenerator import searchRegex, getListfromRegex

# Gets the needed directories 
scriptPath = os.path.dirname(os.path.realpath(__file__))
frameworkPath = os.path.dirname(scriptPath)
prjPath = os.getcwd()

def setCurrentFile(filename):
	"""The function is needed to set the global variable representing the filename of the current program
	
	Args:
		filename (string): the filename of the c program 
	"""
	global currentFilename
	currentFilename = filename

def checkDir(dirPath):
	return (os.path.isdir(dirPath) and os.path.exists(dirPath))

def removeDir(dirName):
	"""removeDir uses the "isdir" function, from the library os, to check if
	the indicated directory "dirName" is a folder and if so deletes it
	
	Args:
		dirName (string): the name of the directory to delete
	"""
	if os.path.isdir(dirName):
		rmtree(dirName)

def createDir(dirName):
	"""createDir creates the specified directory in the current working directory
	
	Args:
		dirName (string): the name of the directory to create
	"""
	os.makedirs(dirName)

def findFileByExtension(directory, extension):
	"""
	This functions finds the files with the specified extension.

	Args:
		directory: indicates the directory in which the file has to be searched
		extension: indicates the extension of the file

	Returns:
		list: the list of elements with the specified extension else None 
	"""
	fileList = returnFiles(directory)
	results = []

	for element in fileList:
		# the asterisk is needed to indicate 
		if fnmatch.fnmatch(element, '*' + extension):
			results.append(element)

	return results

def returnFiles(topDir, dirFlag = False, extension = None):
	""" This function returns the files or directories contained in the indicated directory "topDir"
		
	Args:
		topDir (string): indicates the directory in which the files has to be searched
		dirFlag (boolean, optional): if specified, the function returns the list of directories in topDir
		extension (string, optional): if specified, the function returns the list of files with the indicated extension

	Returns:
		list: the list of files or directories in the directory
	"""
	fileList = []
	
	if dirFlag == True:
		return [f for f in os.listdir(topDir) if os.path.isdir(os.path.join(topDir, f))]

	if extension != None:
		return [f for f in os.listdir(topDir) if os.path.isfile(os.path.join(topDir, f)) and f.endswith(extension)]

	return [f for f in os.listdir(topDir) if os.path.isfile(os.path.join(topDir, f))]

def splitFilename(filename):
	"""This function retrieves the extension from the filename
	
	Args:
		filename (string): the name of the file to be processed
	
	Returns:
		list: a list of two elements containing the filename and his extension
	"""
	return os.path.splitext(filename)

def moveFile(destination, extension):
	""" This functions moves all the files with the given extension
	
	Args:
		destination (string): the directory in which the files will be moved
		extension (string): the extension of the files to move
	"""
	if os.path.isdir(destination):	
		for filename in returnFiles('.', extension = extension):
			if splitFilename(filename)[1] != ".c":
				os.rename(filename, destination + filename)

def writeTuple(label, value, writerObject):
	""" writeTuple writes a tuple (label, value) in a file
	
	Args:
		label (string): label to be written in the file
		value (string): value to be written in the file
	"""
	writerObject.writerow([label, value])


def moveAllFiles(destination):
	"""This functions moves all files except those with extension .c , .csv and .json in the specified directory 

	Args:
		destination (string): the path of the directory in which the files have to be moved
	"""
	if os.path.isdir(destination):	
		for filename in returnFiles(prjPath):
			extension = splitFilename(filename)[1]
			if (extension != ".c" and extension != ".json"
				and extension != ".csv"):
				os.rename(filename, destination + filename)


def printMicroprocessors():
	"""Function that prints the list of known microprocessorss
	"""
	print("\n- List of available microprocessors:\n")
	for i, ele in enumerate(microList):
		print('\t(' + str(i) + ') ' + ele)


def loadJSONFile(filePath):
	with open(filePath + '.json', 'r') as jsonFile:
		fileObject = json.load(jsonFile)
	return fileObject

def chooseMicro():
	"""This function reads the available microprocessors from a json file and allows the user to choose one
	
	Returns: 
		string: the name of the chosen microprocessor
	"""

	global microList
	global frameworkData

	microList = []
	frameworkData = loadJSONFile(scriptPath + '/' + 'micros')

	for line in frameworkData:
		if line != 'profiling':
			microList.append(line)

	printMicroprocessors()
	microId = input('\n- Insert the identifier of a microprocessor: ')
	if int(microId) >= len(frameworkData):
		raise ValueError("The id doesn't exist")

	chosenMicro = microList[int(microId)]

	return chosenMicro

def createFile(filename, extension=""):
	return open(filename + extension, "w")

def closeFile(fileObject):
	fileObject.close()
	
def parseGcovOutput():
	"""This function analyzes the output of GCov profiler 

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
	"""Generic parsing for the output file of an ISS

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
		assemblyInst = searchRegex(r'([iI]nstructions.*?:\s*)(\d+(.\d+)?)', content)
		print(cycleStr, assemblyInst.group())
		
		return cycleStr.group(2), assemblyInst.group(2)


def createFileWriter(fileDescriptor):
	"""This function is specify the characteristics of a .csv file (e.g. set its delimiter)
	
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
	"""This functions replaces the placeholder, inserted in .json file, with the appropriate values

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
	"""This functions searches for the placeholder that indicates the output file

	Args:
		commandString (string): 

	Examples:
		Output File placeholder: {content.format}  

	Returns: 
		string: if present, the content of the output file placeholder otherwise None
	"""
	outputFilename = searchRegex(r'[^:\/;]\{(.*?)\}', commandString)

	if outputFilename != None:
		return outputFilename.group(1)
	return None

def executeCommandSet(resultFile, microName, headers):
	"""This functions executes the set of commands incated under microName label in the .json file

	Args:	
		filename (string): the filename of the c program
		resultFile (string): the file in which are stored the information about the execution 
		microName (string): the label of the .json file 

	Todo:
		* insert comments in the algorithm
	"""

	with open(resultFile, 'w') as outputFile:
		fileWriter = csv.DictWriter(outputFile, fieldnames=headers)
		fileWriter.writeheader()

		commandSet = frameworkData[microName]
		commandList = splitBySpace(commandSet["dependencies"])

		for directory in returnFiles('includes', True):
			for command in commandList:
				commandStr = commandSet[command]


				expandedStr = expandCommand(commandStr, directory)
				flags = splitBySpace(expandedStr)
			
				# Executes a command that expects an output file 
				outputFilename = getOutputFilename(expandedStr)
				if outputFilename != None:
					# ---------------------------------------
					flags.remove('{' + outputFilename + '}')
					# ---------------------------------------
					with open(outputFilename, 'w') as execFile:
						subprocess.call(flags, stdout = execFile)

				else:
					print("flags", flags)
					subprocess.call(flags)

			# Move all the products of the computation in a temporary directory
			outputPath = 'debug_' + directory + '/'
			createDir(outputPath)

			row = {}
			row_values = []
			row_values.append(directory)

			if microName == 'profiling':
				# Gcov returns the number of C statements 
				cInstr = parseGcovOutput()
				row_values.append(cInstr)
			else:
				# The function parses the output of the simulation to get the number of assembly instruction 
				# and the number of cycles
				cycleStr, assemblyInst = parseSimulationOutput(outputFilename)
				row_values.append(cycleStr)
				row_values.append(assemblyInst)
			
			# Write the values
			row = {key:value for key, value in zip(headers, row_values)}
			fileWriter.writerow(row)
			# Move all files in the debug directory 
			moveAllFiles(outputPath)
			# Deletes the debug directory
			removeDir(outputPath)

"""
CC4CS Calculation
"""

def calculateMetric(cyclesFilename, statementsFilename):
	"""This function analyzes the files with the clock cycles and the number of C statements.
	Finally, calculates the metric

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


def calculateMetricWithHeader(cyclesFilename, statementsFilename):
	with open(cyclesFilename) as cyclesFile, open(statementsFilename) as statementsFile, open("cc4csValues.csv", "w") as outputFile:
		cyclesContent = csv.reader(cyclesFile)
		statementsContent = csv.reader(statementsFile)
		# get the header of the simulation output file
		secondFileHeader = next(cyclesContent)
		# get the header from the profiling phase result
		firstFileHeader = next(statementsContent)		
		# headers of the outputfile
		headers = list(dict.fromkeys(firstFileHeader + secondFileHeader))
		headers.append('cc4cs')
		# Write headers in the file 
		resultWriter = csv.DictWriter(outputFile, headers)
		resultWriter.writeheader()

		for (c1, c2) in zip(statementsContent, cyclesContent):
			cc4csValue = "{0:.3f}".format(int(c2[1]) / int(c1[1]))
			row = [str(c1[0]), str(c1[1]), str(c2[1]), str(c2[2]), str(cc4csValue)]
			resultWriter.writerow(dict(zip(headers, row)))



def getDataFromValues(filePath, getKey=False):
	with open(filePath, 'r') as inputFile:
		reader = csv.reader(inputFile, delimiter='=')
		keys, values = [], []

		for row in reader:
			# if required to skip the macros 
			if not row[0].startswith('#'):	
				if getKey:
					key = row[0]
					key = key.strip()
					key = key.replace(' ', '{')
					key = getListfromRegex(r'(?:\{)(.*)', key)
					keys.append(key[0])	
				else:
					value = row[1]
					value = [x[0] for x in getListfromRegex(r'(\d+(\.\d+)?)', value)]
					values.append(value)
		if getKey: 
			return keys 
		return values

def createInputResume():
	with open('inputResume.csv', 'w') as outputFile:
		keys = getDataFromValues('includes/values_0/values.h', getKey=True)
		fileWriter = csv.DictWriter(outputFile, fieldnames=keys)
		fileWriter.writeheader()
		for directory in returnFiles('includes', True):
			values = getDataFromValues('includes/' + directory + '/values.h')
			fileWriter.writerow(dict(zip(keys, values)))