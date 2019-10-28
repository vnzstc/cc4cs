# Built-in modules
import csv, sys, os

# Custom modules
import inputgenerator
import core

#  ["int8_t", "int16_t", "int32_t", "long"]
# Global Variables 
indexTypes = ["int8_t", "int16_t", "int32_t", "long"]
targeTypes = ["int8_t", "int16_t", "int32_t", "float"]

# targeTypes = ["uint8_t", "uint16_t", "uint32_t", "float"]
# indexTypes = ["uint8_t", "uint16_t", "uint32_t", "long"]


# Results file headers 
headers = ['id', 'cInstr', 'assemblyInstr', 'clockCycles','executionTime', 'CC4CS']

statementsFilename = 'cStatements.csv'
cyclesFilename = 'clockCycles.csv'

cFilesList = core.returnFiles('.', extension = '.c')
prjPath = os.getcwd()

print("\n\n ██████╗ ██████╗██╗  ██╗ ██████╗███████╗\n"+
	  "██╔════╝██╔════╝██║  ██║██╔════╝██╔════╝\n"+
	  "██║     ██║     ███████║██║     ███████╗\n"+
	  "██║     ██║     ╚════██║██║     ╚════██║\n"+
	  "╚██████╗╚██████╗     ██║╚██████╗███████║\n"+
	  " ╚═════╝ ╚═════╝     ╚═╝ ╚═════╝╚══════╝\n")


def deletePreviousComputations():
	core.removeDir('includes')
	core.removeDir('profiling')	
	core.removeDir('simulation')

def createDirs():
	core.createDir('profiling')
	core.createDir('simulation')
	core.createDir('results')

if not cFilesList:
	raise ValueError("At least one .c file must be in this directory")

deletePreviousComputations()
core.removeDir('results')
createDirs()

# Searches for all the '.c' files in the current directory
for flnm in cFilesList:

	#######
	# Removes the extension from the filename
	filename = core.splitFilename(flnm)

	# Sets the global variable in the core file 
	core.setCurrentFile(filename[0])
	#######
	
	chosenMicro = core.chooseMicro()

	# Simulation Branch
	for currentType, currentIndex in zip(targeTypes, indexTypes):
		print("\nProcessing type: " + currentType + "\n")
		deletePreviousComputations()

		# Loads parameters from the file named parameters.json
		parametersFile = core.loadJSONFile(prjPath + '/parameters')

		# Preprocessing Part
		inputgenerator.replaceStr(flnm, r'typedef\s[a-z0-9_\s]+TARGET_TYPE', "typedef " + currentType + " TARGET_TYPE;\n")
		inputgenerator.replaceStr(flnm, r'typedef\s[a-z0-9_\s]+TARGET_INDEX', "typedef " + currentIndex + " TARGET_INDEX;\n" )

		# InputGenerator Part ------------------------
		inputgenerator.discoverParameters(filename[0], currentType, currentIndex)
		inputgenerator.getParametersFromFile(parametersFile, currentType)
		inputgenerator.listCreator()
		inputgenerator.generateHeaders()
		# --------------------------------------------

		# Executes profiling commands
		core.executeCommandSet(statementsFilename, 'profiling', ['id', 'cInstr'])		

		# Executes cycles commands 
		core.executeCommandSet(cyclesFilename, chosenMicro, ['id', 'clockCycles', 'assemblyInstr'])
		# Calculate Statistics 
		core.calculateMetricWithHeader(cyclesFilename, statementsFilename)
		# Create a file containg the inputs
		core.createInputResume()
		core.removeDir('includes')
		core.createDir("results/" + currentType)
		core.moveFile("results/" + currentType + "/", ".csv")
		print("Done!")