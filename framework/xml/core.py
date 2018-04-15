import xml.etree.ElementTree as et
import os, csv
import subprocess
from shutil import rmtree

microList = []
scriptPath = os.path.dirname(os.path.realpath(__file__))
prjPath = os.getcwd()

tree = et.parse(scriptPath + '/conf.xml')
root = tree.getroot()

"""
	Operations at System-Level
"""
def checkKeyExistence(keyName, dictName):
	if keyName in dictName:
		return dictName[keyName]
	return None

def printMicros():
	"""
		Function that prints the list of known microprocessors
	"""
	print("List of available microprocessors:\n")
	for i, ele in enumerate(microList):
		print('(' + str(i) + ') ' + ele)

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

def createDir(dirName):
	os.makedirs(dirName)

def mvAllFiles(destination):
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

def executeCommands(phaseName):

	phaseEle = tree.find(phaseName)
	depEle = tree.find(phaseName + '/dependencies')

	for cmd in depEle.text.split(" "):
		flagList = []
		cmdEle = phaseEle.find(cmd)

		inputFile = checkKeyExistence('inputFile', cmdEle.attrib)
		outputFile = checkKeyExistence('outputFile', cmdEle.attrib)

		if cmdEle.text != None:
			flagList = cmdEle.text.split(" ")

		print(cmdEle, inputFile, outputFile, flagList)

		if inputFile != None:
			flagList.insert(1, inputFile)

		if outputFile != None:
			flagList.insert(len(flagList), outputFile)

			with open(outputFile, 'w') as execFile:
				subprocess.call(flagList, stdout=execFile)
		else:
			subprocess.call(flagList)

def parseGcovOutput(txtFilePath):
	result = 0
	with open(txtFilePath + ".c.gcov", "r") as file:
		for line in file:
			number = file.readline().split(':')[0]
			number = number.strip()
			if number.isdigit():
				result += int(number)

	return result
""" 
	Operation on the conf XML File
"""
def chooseMicro():
	"""
		Reads the available microprocessors from a json file and allows the user to choose one
		Return: the xml object containing all the operation about the chosen micro
	"""

	for ele in tree.findall('micro'):
		microList.append(ele.get('name'))

	printMicros()
	microId = input('\nInsert the identifier of a microprocessor: ')
	if int(microId) >= len(microList):
		raise ValueError("The id doesn't exist")

	chosenMicro = microList[int(microId)]
	
	return root.find('.//micro[@name="%s"]' % chosenMicro)

""" 
	Operation on CSV Files
"""
def writeTuple(label, value, writerId):
	writerId.writerow([label, value])

def createFileWriter(fileDescriptor):
	return csv.writer(fileDescriptor, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)



def executePhase(inputFileName, outputFileName, phaseName):
	with open(outputFileName, 'w') as outputFile:
		fileWriter = createFileWriter(outputFile)
		
		if phaseName == 'profiling':
		
			for directory in returnListDir('includes'):
				outputPath = "profiling/" + directory + '/'
				createDir(outputPath)
				executeCommands('profiling')
				numberCstat = parseGcovOutput(inputFileName)
				writeTuple(directory, numberCstat, fileWriter)
				mvAllFiles(outputPath)