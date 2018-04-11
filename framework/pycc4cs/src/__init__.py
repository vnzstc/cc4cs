# Built-in modules
import csv, sys

# Custom modules
import preprocessor 
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
	core.compileProgram(fileName, headerDir, 'gcc -fprofile-arcs -ftest-coverage')
	core.executeProgram("./" + fileName)
	core.executeProgram("gcov " + fileName)

	return core.parseGcovOutput(fileName + ".c.gcov")

def simulationPhase(headerDir):
	core.compileProgram(fileName, headerDir, microSpec['compiler'])
	core.executeProgram(microSpec['iss'] + " " + fileName)
	return core.parseSimulationOutput()

microSpec = core.chooseMicro()
print(microSpec)

core.deletePreviousComputation()

# --------------------------------------
core.createDir('profiling')
core.createDir('simulation')
core.createDir('results')
# --------------------------------------

# Searches for all the '.c' files in the current directory
for flnm in core.returnListDir('.'):
	extension =  core.getExtensionFilename(flnm)
	fileName = extension[0]

	if extension[1] == '.c':
		# Preprocessing Part
		preprocessor.replaceStr(flnm, r'typedef\s[a-z0-9_\s]+TARGET_TYPE', "typedef int TARGET_TYPE;\n")
		
		# InputGenerator Part
		inputgenerator.discoverParameters(fileName)
		inputgenerator.listCreator("float")
		inputgenerator.generateHeaders("float")		
		
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
				core.mvFiles(simulationDir, [fileName, "executionOutput.txt"])
				# --------------------------------------

		# Calculate metric 
		core.cc4csCalculator()
		# --------------------------------------
		core.mvFiles('results/', ["cc4csValues.csv", "clockCycles.csv", "cStatements.csv"])
		# --------------------------------------


