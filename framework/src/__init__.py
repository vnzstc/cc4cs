# graphical user interface
from tkinter.filedialog import askdirectory 
from GUI import GUI

# cmd manager
from CommandsManager import CommandsMananger
from InputsGenerator import InputsGenerator
from Parser import Parser

# os operations 
from os.path import abspath, expanduser, isdir, isfile, dirname, realpath, splitext, join
from os import mkdir, makedirs, replace, listdir, chdir
from shutil import move, rmtree

# others
from re import match
from csv import reader, DictWriter
from json import load

# Global Variables 
## Microprocessors
micros = ['8051', 'Leon3', 'Atmega328p']
## Types 
indexTypes = ["int8_t", "int16_t", "int32_t", "long"]
#indexTypes = ["uint8_t", "uint16_t", "uint32_t", "unsigned long"]
targetTypes = ["int8_t", "int16_t", "int32_t", "long"]

## Result file headers 
headers = ['ID', 'CInstr', 'AssemblyInstr', 'ClockCycles','ExecutionTime', 'CC4CS']
## Dirs and file names 
outputDir = ""
### Absolute of the directory containing the source code
sourcePath = dirname(realpath(__file__))

def replaceString(filename, regexStr, replacementStr):
	"""This function replaces a line in a file that matches the specified regular expression

		Args: 
			filename (string): the name of the file to be opened
			regexStr (string): a regular expression
			replacementStr (string): the string that is inserted in the file 
"""
	with open(filename, "r") as file:
		lines = file.readlines()

	for i,line in enumerate(lines):
		# Better to rise an exception if this is never accessed
		if match(regexStr, line):
			lines[i] = replacementStr

	with open(filename, "w") as file: 
		file.writelines(lines)  

def loadJSONFile(filePath):
	with open(filePath + '.json', 'r') as jsonFile:
		fileObj = load(jsonFile)
	return fileObj

def getFiles(topDir, extension):
	"""This function returns the files with a specified extension that are contained in topDir.
	"""
	return [f for f in listdir(topDir) if isfile(join(topDir, f)) and f.endswith(extension)]

def num(s):
	try:
		return int(s)
	except ValueError:
		return float(s)

def calculateMetric(profPath, simPath):
	"""The function merges the content of the files obtained from the simulation and the profiling phases. 
	Then, it writes their content and the metric values in the "cc4csValues.csv" file

	Args:
		cyclesFilename (string): path of the file obtained from the simulation phase
		statementsFilename (string): path of the file obtained from the profiling phase
	"""
	with open(simPath) as cyclesFile, open(profPath) as statementsFile, \
		open("cc4csValues.csv", "w") as outputFile:
		
		# Reads the content of the two phases output files
		profilingContent = reader(cyclesFile)
		simulationContent = reader(statementsFile)

		# Retrieves the headers of the two phases output files
		profilingHeaders = next(profilingContent)
		simulationHeaders = next(simulationContent)

		# Headers of the output file
		headers = list(dict.fromkeys(profilingHeaders + simulationHeaders))
		headers.append('cc4cs')

		# Write Headers in the file 
		resWriter = DictWriter(outputFile, headers)
		resWriter.writeheader()

		# Iterates thorugh the content of the files 
		for c1, c2 in zip(profilingContent, simulationContent):
			op1 = num(c1[1])
			op2 = num(c2[1])
			# Calculates the values of the metric
			cc4csValue = '%.3f' % (op1 / op2)
			# Merges the data of the files
			c1.extend(x for x in c2 if x not in c1)
			c1.append(cc4csValue)
			# Writes it on a file
			resWriter.writerow(dict(zip(headers, c1)))


def callback(algName, chosenMicro, listBoxFlag):
	global outputDir

	functionName = algName.get(listBoxFlag)
	absFunctionPath = abspath('benchmark/' + functionName) + '/'

	outputDir = askdirectory(initialdir = expanduser("~/Desktop"),
		title = 'Select folder to save results')
	
	if not isdir(outputDir):
		mkdir(outputDir)

	# the GUI returns the index of the microprocessor in the "micros" list
	chosenMicro = micros[chosenMicro.get()]
	# Loads a different source file according to the microprocessor that has been chosen
	funSrc = 'scnd.c' if chosenMicro == "8051" else 'frst.c'
	# Absolute path of the function source code
	absFunctionFile = absFunctionPath + funSrc

	# Loads parameters from the file named parameters.json
	paramsFile = loadJSONFile(absFunctionPath + '/parameters')
	# Contains the parameters of the chosen microprocessors according with the current type
	chosenParams = paramsFile[chosenMicro]

	# Loads the commands to execute from the file named cmds.json
	cmdsFile = loadJSONFile(sourcePath + '/cmds')
	# Commands for the profiling phase
	cmdsProfiling = cmdsFile['Profiling']
	# Commands for the simulation phase
	cmdsMicro = cmdsFile[chosenMicro]
	# Commands for the FramaC workflow
	cmdsFrama = cmdsFile['FramaC']

	# CommandManager Singleton
	## Removes the extension from the filename
	funSrcName = splitext(funSrc)[0]
	cmdMan = CommandsMananger(absFunctionFile, sourcePath, funSrcName, outputDir)
	# InputsGenerator 
	inptGen = InputsGenerator(absFunctionFile, functionName)

	# Executes the flow for each type in "parameters.json" file
	for currentType, currentIndex in zip(targetTypes, indexTypes):
		print(currentType, currentIndex)
		# The path of the folder that will contain  the inputs of the function
		inputsPath = outputDir + "/includes"
		# The path of the directory that will contain the results of the computation
		resultsPath = "results/" + currentType
		# The path of the file contaning the executed C statements 
		profilingFilename = outputDir + "/cStatements.csv"
		# The path of the file contaning the number of clock cycles needed for the execution
		simulationFilename = outputDir + "/clockCycles.csv"

		# Preprocessing Part
		replaceString(absFunctionFile, r'typedef\s[a-z0-9_\s]+TARGET_TYPE', 
			"typedef " + currentType + " TARGET_TYPE;\n")
		replaceString(absFunctionFile, r'typedef\s[a-z0-9_\s]+TARGET_INDEX',
			"typedef " + currentIndex + " TARGET_INDEX;\n" )

		# Create the directory in which the headers will be placed
		makedirs(inputsPath)
		# Changes working directory 
		chdir(inputsPath)
		inptGen.createHeaders(chosenParams, currentType, currentIndex)
		# Returns to the previous working directory
		chdir("..")
		
		# Executes profiling commands
		parser = Parser(profilingFilename, Parser.gcovParser, ['id', 'cInstr'])
		cmdMan.executeCommandSet(cmdsProfiling, inputsPath, parsingFunction = parser.run, debugFlag = True)

		# Executes simulation commands
		parser = Parser(simulationFilename, Parser.simParser, ['id', 'clockCycles', 'assemblyInstr'])
		cmdMan.executeCommandSet(cmdsMicro, inputsPath, parsingFunction = parser.run, debugFlag = True)
		
	
		# Executes FramaC commands 
		cmdMan.executeCommandSet(cmdsFrama, inputsPath)

		# Builds a parser for the Halsted output file
		parser = Parser(outputDir + "/Halsted.csv", Parser.getFramaRow)
		parser.framaParser(outputDir + "/files", 1)

		# Buils a parser for the McCabe output file
		parser.outputPath = outputDir + "/McCabe.csv"
		parser.framaParser(outputDir + "/files", 0)

		parser = Parser(outputDir + "/inputResume.csv", Parser.inputParser)
		parser.inputParser(inputsPath)

		# Function that calculates the metric
		calculateMetric(profilingFilename, simulationFilename)

		# Creates the directory in which store the results 
		if not isdir(resultsPath):
			makedirs(resultsPath)
		
		# Moves all the '.csv' and '.txt' in the results file
		dirFiles = getFiles('.', '.csv') + getFiles('.', '.txt')
		for resFile in dirFiles:
			move(resFile, resultsPath)
		
		# Deletes the directory containing the inputs for the current type 
		rmtree("includes/")
		# Deletes the files produced for the current type
		# rmtree("files/")

	print("Done!")

# Start GUI
viewInstance = GUI("CC4CS Calculator", "300x370")
# viewInstance.fixSize()
viewInstance.fillMainWindow(micros, abspath('benchmark'), callback)
viewInstance.start()
