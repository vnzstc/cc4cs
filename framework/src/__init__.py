# Built-in modules
import csv, sys

# Custom modules
import inputgenerator
import core

types = ["int", "long", "float"]

print("\n\n ██████╗ ██████╗██╗  ██╗ ██████╗███████╗\n"+
	  "██╔════╝██╔════╝██║  ██║██╔════╝██╔════╝\n"+
	  "██║     ██║     ███████║██║     ███████╗\n"+
	  "██║     ██║     ╚════██║██║     ╚════██║\n"+
	  "╚██████╗╚██████╗     ██║╚██████╗███████║\n"+
	  " ╚═════╝ ╚═════╝     ╚═╝ ╚═════╝╚══════╝\n")

# Global Variables 
cycleFile = "clockCycles.csv"
statementsFile = "cStatements.csv"

cFilesList = core.returnFiles('.', extension = '.c')

# Deletes previous computations
core.removeDir('includes')
core.removeDir('profiling')
core.removeDir('simulation')
core.removeDir('results')

if not cFilesList:
	raise ValueError("At least one .c file must be in this directory")

# --------------------------------------
core.createDir('profiling')
core.createDir('simulation')
core.createDir('results')
# --------------------------------------

# Searches for all the '.c' files in the current directory
for flnm in cFilesList:

	filename =  core.splitFilename(flnm)
	core.setCurrentFile(filename[0])

	# Preprocessing Part
	inputgenerator.replaceStr(flnm, r'typedef\s[a-z0-9_\s]+TARGET_TYPE', "typedef int TARGET_TYPE;\n")

	# InputGenerator Part
	inputgenerator.discoverParameters(filename[0])
	inputgenerator.listCreator("int")
	inputgenerator.generateHeaders("int")

	# Simulation Part
	chosenMicro = core.chooseMicro()

	core.executeCommandSet('cStatements.csv', 'profiling')
	core.executeCommandSet('clockCycles.csv', chosenMicro)

	# Calculate Statistics 
	core.calculateMetric(cycleFile, statementsFile)
	core.mvFiles("results/", ".csv")