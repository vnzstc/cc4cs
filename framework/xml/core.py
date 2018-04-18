import xml.etree.ElementTree as et
import os, csv
import subprocess
from inputgenerator import getListfromRegex
from shutil import rmtree

microList = []
scriptPath = os.path.dirname(os.path.realpath(__file__))
prjPath = os.getcwd()

tree = et.parse(scriptPath + '/conf.xml')
root = tree.getroot()
chosenMicro = ""

"""
	Operations at System-Level
"""
def printMicros():
	"""
		Function that prints the list of known microprocessors
	"""
	print("List of available microprocessors:\n")
	for i, ele in enumerate(microList):
		print('(' + str(i) + ') ' + ele)

# ------------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------------
def createDir(dirName):
	os.makedirs(dirName)

def mvAllFiles(destination):
	"""
		Moves all files except those with extension .c and .csv in the indicated directory "destination"
	"""
	print("moveAllFiles " + destination)
	if os.path.isdir(destination):	
		for fileName in returnListFiles(prjPath):
			if getExtensionFilename(fileName)[1] != ".c" and getExtensionFilename(fileName)[1] != '.csv':
				os.rename(fileName, destination + fileName)

# ------------------------------------------------------------------------------------
def returnListDir(topDir):
	return [f for f in os.listdir(topDir) if os.path.isdir(os.path.join(topDir, f))]

def returnListFiles(topDir):
	return [f for f in os.listdir(topDir) if os.path.isfile(os.path.join(topDir, f))]
# ------------------------------------------------------------------------------------

def getExtensionFilename(fileName):
	"""
		Given the file name, returns a list containing the file name without the extension and this one
	"""
	return os.path.splitext(fileName)

def checkKeyExistence(keyName, dictName):
	if keyName in dictName:
		return dictName[keyName]
	return None

def executeFileSet(microName):
	fileSetObj = tree.find('fileSet')
	microFiles = fileSetObj.findall('.//file[@name="%s"]' % microName)

	for file in microFiles:
		executeCmd(file.text.split(" "), file)


def executeCmd(flagList, elementObj):
	inputFile = checkKeyExistence('inputFile', elementObj.attrib)
	outputFile = checkKeyExistence('outputFile', elementObj.attrib)

	if inputFile != None:
		flagList.insert(1, inputFile)

	if outputFile != None:
		with open(outputFile, 'w') as execFile:
			subprocess.call(flagList, stdout=execFile)

			return outputFile
	else:
		subprocess.call(flagList)

	return None

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
		cycleStr = getListfromRegex(r'[cC]ycles.*?\d+', content)[0]
		return getListfromRegex(r'\d+', cycleStr)[0] 
""" 
	Operation on the conf XML File
"""
def chooseMicro():
	"""
		Reads the available microprocessors from a json file and allows the user to choose one
		Return: the xml object containing all the operation about the chosen micro
	"""
	for ele in tree.findall('.//commandSet[@type="micro"]'):
		microList.append(ele.get('name'))

	printMicros()
	microId = input('\nInsert the identifier of a microprocessor: ')
	if int(microId) >= len(microList):
		raise ValueError("The id doesn't exist")

	chosenMicro = microList[int(microId)]

	return chosenMicro
""" 
	Operation on CSV Files
"""
def writeTuple(label, value, writerId):
	writerId.writerow([label, value])

def createFileWriter(fileDescriptor):
	return csv.writer(fileDescriptor, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)

def executeCommandSet(inputFileName, outputFileName, microName):
	with open(outputFileName, 'w') as outputFile:
		fileWriter = createFileWriter(outputFile)

		for directory in returnListDir('includes'):
			# Finds the chosen micro commandSet in the xml, returns a list of subtree
			currentObj = tree.findall('.//commandSet[@name="%s"]' % microName)
			# Searches for dependencies tag in the currentObj subtree
			for currentElement in currentObj:
				dependenciesObj = currentElement.find('dependencies')
				# Commands and flags are specified in the tag value, separated by a space
				for cmd in dependenciesObj.text.split(" "):
					cmdObj = currentElement.find(cmd)

					flagList = []
					# If the command flag field is not empty
					if cmdObj.text != None:
						flagList = cmdObj.text.split(" ")
					# If the tag is the compiler one, adds the "includes" flags 
					if cmdObj.tag == 'compiler': 
						flagList.extend(['-Iincludes/', "-Iincludes/" + directory, "-o", inputFileName])
					
					simOutput = executeCmd(flagList, cmdObj)

				if microName == 'profiling':
					outputPath = 'profiling/' + directory + '/'
					createDir(outputPath)
					value = parseGcovOutput(inputFileName)
				else:
					outputPath = 'simulation/' + directory + '/'
					createDir(outputPath)
					value = parseSimulationOutput(simOutput)

				# ----------------------------------------------
				writeTuple(directory, value, fileWriter)
				mvAllFiles(outputPath)
				# ----------------------------------------------
