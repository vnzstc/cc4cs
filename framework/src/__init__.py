# Built-in modules
import csv, sys

# Custom modules
import inputgenerator
import core

# Global Variables 
types = ["int8_t", "int"]
cycleFile = "clockCycles.csv"
statementsFile = "cStatements.csv"
cFilesList = core.returnFiles('.', extension = '.c')

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

	filename =  core.splitFilename(flnm)
	core.setCurrentFile(filename[0])

	for kind in types:

		deletePreviousComputations()
		# Preprocessing Part
		inputgenerator.replaceStr(flnm, r'typedef\s[a-z0-9_\s]+TARGET_TYPE', "typedef " + kind + " TARGET_TYPE;\n")

		# InputGenerator Part
		inputgenerator.discoverParameters(filename[0])
		inputgenerator.listCreator(kind)
		inputgenerator.generateHeaders(kind)

		# Simulation Part
		chosenMicro = core.chooseMicro()

		core.executeCommandSet('cStatements.csv', 'profiling')
		core.executeCommandSet('clockCycles.csv', chosenMicro)

		# Calculate Statistics 
		core.calculateMetric(cycleFile, statementsFile)

		core.createDir("results/" + kind)
		core.mvFiles("results/" + kind + "/", ".csv")