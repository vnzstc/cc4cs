# Built-in modules
import os
from shutil import rmtree
import csv

# Custom modules
import preprocessor 
import inputgenerator
import core


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

# Checking for previous computations 
def deletePreviousComputation():
	if os.path.isdir('includes'):
		rmtree('includes')

	if os.path.isdir('profiling'):
		rmtree('profiling')

	if os.path.isdir('results'):
		rmtree('results')

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

deletePreviousComputation()

# Searches for all the '.c' files in the current directory
for flnm in os.listdir('.'):
	extension =  os.path.splitext(flnm)
	fileName = extension[0]

	if extension[1] == '.c':
		# Preprocessing Part
		preprocessor.replaceStr(flnm, r'typedef\s[a-z0-9_\s]+TARGET_TYPE', "typedef int TARGET_TYPE;\n")
		
		# InputGenerator Part
		inputgenerator.discoverParameters(fileName)
		inputgenerator.listCreator("float")
		inputgenerator.generateHeaders("float")		
		
		# Profiling Phase
		# Creation of CSV File 
		with open('cStatements.csv', 'w') as statementFile:
			fileWriter = core.createFileWriter(statementFile)

			# -------------------------
			os.makedirs('profiling')
			# -------------------------

			for directory in os.listdir('includes'):

				# Function that is not useful
				numberCstat = profilingPhase("includes/" + directory + '/')

				core.writeTuple(directory, numberCstat, fileWriter)
				# -----------------------------------------
				profilingDir = 'profiling/' + directory + '/'
				os.makedirs(profilingDir)
				
				gcnoName = fileName + ".gcno"
				gcdaName = fileName + ".gcda"
				gcovName = fileName + ".c.gcov"

				# Moves the created files in the .c.gcov 
				os.rename(gcnoName, profilingDir + gcnoName)
				os.rename(fileName, profilingDir + fileName)
				os.rename(gcdaName, profilingDir + gcdaName)
				os.rename(gcovName, profilingDir + gcovName)
				# --------------------------------------

		# Simulation Phase
		with open('clockCycles.csv', 'w') as ccFile:
			fileWriter = core.createFileWriter(ccFile)

			for directory in os.listdir('includes'):
				clockCycles = simulationPhase("includes/" + directory + '/')
				core.writeTuple(directory, clockCycles, fileWriter)

		# Calculate metric 
		core.cc4csCalculator()
