import os, subprocess, json
from preprocessor import getListfromRegex

# Gets the script directory 
scriptPath = os.path.dirname(os.path.realpath(__file__))
microList = []

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
	This function is needed to compile a couple (algorithm + the trace)
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
		return getListfromRegex(r'\d+', content)[0]