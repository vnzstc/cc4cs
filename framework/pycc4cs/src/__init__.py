# Built-in modules
import csv, sys

# Custom modules
import inputgenerator
import core

"""
CC4CS Evaluation Framework

usage:
	__init__.py --debug 

options:
	--debug		enables debug options 
"""

debugOpt = False
if "--debug" in sys.argv: debugOpt = True

types = ["int", "long", "float"]
print("\n\n ██████╗ ██████╗██╗  ██╗ ██████╗███████╗\n"+
	  "██╔════╝██╔════╝██║  ██║██╔════╝██╔════╝\n"+
	  "██║     ██║     ███████║██║     ███████╗\n"+
	  "██║     ██║     ╚════██║██║     ╚════██║\n"+
	  "╚██████╗╚██████╗     ██║╚██████╗███████║\n"+
	  " ╚═════╝ ╚═════╝     ╚═╝ ╚═════╝╚══════╝\n")

# The script must be launched in the working directory 
"""
	cwd = os.getcwd()
	print(cwd)
"""
def profilingPhase(headerDir):
	proFlags = ""

	# This branch is needed to add custum flags to the profiling phase
	if "profilingFlags" in microSpec:
		proFlags = microSpec["profilingFlags"]

	core.compileProgram(fileName, headerDir, 'gcc -fprofile-arcs -ftest-coverage ' + proFlags)
	core.executeProgram("./" + fileName)
	core.executeProgram("gcov " + fileName)

	return core.parseGcovOutput(fileName + ".c.gcov")

def simulationPhase(headerDir):
	core.compileProgram(fileName, headerDir, microSpec['compiler'])
	
	# Checks if the are dependencies before the sw simulation
	dependencies = microSpec["dependencies"].split(" ")

	for command in dependencies:
		#customFilename = core.getCustomFilename(microSpec[command])
		core.executeProgram(microSpec[command] + " " + fileName)

	# return core.parseSimulationOutput()
	return 0
	
microSpec = core.chooseMicro()
print(microSpec)

core.deletePreviousComputation()

# --------------------------------------
core.createDir('profiling')
core.createDir('simulation')
core.createDir('results')
# --------------------------------------

# Searches for all the '.c' files in the current directory
for flnm in core.returnListFiles('.'):
	extension =  core.getExtensionFilename(flnm)
	fileName = extension[0]

	if extension[1] == '.c':
		# Preprocessing Part
		inputgenerator.replaceStr(flnm, r'typedef\s[a-z0-9_\s]+TARGET_TYPE', "typedef int TARGET_TYPE;\n")
		
		# InputGenerator Part
		inputgenerator.discoverParameters(fileName)
		inputgenerator.listCreator("int")
		inputgenerator.generateHeaders("int")

		# ---------------------------------------------------------------
		# This part is needed to execute commands on additional files 
		if "additionalFiles" in microSpec:
			addFiles = microSpec["additionalFiles"].split(" ")

			for files in addFiles:
				core.executeProgram(microSpec[files])	
		# ---------------------------------------------------------------	
		
		
		# Profiling Phase
		with open('cStatements.csv', 'w') as statementFile:
			fileWriter = core.createFileWriter(statementFile)

			for directory in core.returnListDir('includes'):
				numberCstat = profilingPhase("includes/" + directory + '/')
				core.writeTuple(directory, numberCstat, fileWriter)
				
				# -----------------------------------------
				profilingDir = 'profiling/' + directory + '/'
				core.createDir(profilingDir)
				core.mvFiles(profilingDir, [fileName + ".gcno", fileName + ".gcda", fileName + ".c.gcov"])
				# --------------------------------------
				
		# Simulation Phase
		with open('clockCycles.csv', 'w') as ccFile:
			fileWriter = core.createFileWriter(ccFile)

			for directory in core.returnListDir('includes'):
				clockCycles = simulationPhase("includes/" + directory + '/')
				core.writeTuple(directory, clockCycles, fileWriter)

				# -----------------------------------------
				simulationDir = 'simulation/' + directory + '/'
				core.createDir(simulationDir)
				core.mvAllFiles(simulationDir)
				# --------------------------------------

		# Calculate metric 
		core.cc4csCalculator()
		# --------------------------------------
		core.mvFiles('results/', ["cc4csValues.csv", "clockCycles.csv", "cStatements.csv"])
		# --------------------------------------


