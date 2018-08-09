import xml.etree.ElementTree as et
import os, csv, re
import subprocess
from inputgenerator import getListfromRegex, searchRegex
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

def removeDir(dirName):
	"""
		Removes the directory specified in dirName
	"""
	if os.path.isdir(dirName):
		rmtree(dirName)

def createDir(dirName):
	os.makedirs(dirName)


def mvFile(filename, destination):
	if os.path.isdir(destination):	
		os.rename(filename, destination + filename)

def mvAllFiles(destination):
	"""
		Moves all files except those with extension .c and .csv in the indicated directory "destination"
	"""
	print("moveAllFiles " + destination)
	if os.path.isdir(destination):	
		for fileName in returnListFiles(prjPath):
			if getExtensionFilename(fileName)[1] != ".c" and getExtensionFilename(fileName)[1] != ".csv":
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
		flagList = dictName[keyName].split(" ")
		print(flagList)
		return flagList

	return []

def executeFileSet(microName):
	fileSetObj = tree.find('fileSet')
	microFiles = fileSetObj.findall('.//file[@name="%s"]' % microName)

	for file in microFiles:
		executeCmd(file.text.split(" "), file)


def executeCmd(flagList, elementObj):
	inputFile = checkKeyExistence('inputFile', elementObj.attrib)
	outputFile = checkKeyExistence('outputFile', elementObj.attrib)
	
	if len(inputFile) > 0:
		flagList[1:1] = inputFile

	if len(outputFile) >= 2:
		flagList[len(flagList):len(flagList)] = outputFile

	if len(outputFile) > 0:
		print(flagList)
		with open(outputFile[-1], 'w') as execFile:
			subprocess.call(flagList, stdout=execFile)
		return outputFile[-1]

	print(flagList)
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
		cycleStr = searchRegex(r'([cC]ycles.*?:\s*)(\d+)', content)
		return cycleStr.group(2)
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
						flagList.extend(["-Iincludes/" + directory])
					
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