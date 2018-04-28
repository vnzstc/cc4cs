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

"""
	cwd = os.getcwd()
	print(cwd)
"""

# Deletes previous computations
core.removeDir('includes')
core.removeDir('profiling')
core.removeDir('simulation')
core.removeDir('results')

# --------------------------------------
core.createDir('profiling')
core.createDir('simulation')
core.createDir('results')
# --------------------------------------
cycleFile = "clockCycles.csv"
statementsFile = "cStatements.csv"

# Searches for all the '.c' files in the current directory
for flnm in core.returnListFiles('.'):
	extension =  core.getExtensionFilename(flnm)
	filename = extension[0]
	core.setCurrentFile(filename)

	if extension[1] == '.c':
	
		# Preprocessing Part
		inputgenerator.replaceStr(flnm, r'typedef\s[a-z0-9_\s]+TARGET_TYPE', "typedef int TARGET_TYPE;\n")

		# InputGenerator Part
		inputgenerator.discoverParameters(filename)
		inputgenerator.listCreator("int")
		inputgenerator.generateHeaders("int")

		# Simulation Part
		chosenMicro = core.chooseMicro()
		# core.executeFileSet(chosenMicro)

		core.executeCommandSet('cStatements.csv', 'profiling')
		core.executeCommandSet('clockCycles.csv', chosenMicro)

		# Calculate Statistics 
		core.calculateMetric(cycleFile, statementsFile)