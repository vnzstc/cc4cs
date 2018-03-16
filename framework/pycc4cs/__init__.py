import os
import preprocessor 
import inputgenerator
import core
import csv


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
def profilingPhase(fileName, execName, headerDir):
	core.compileWithGCC(fileName, headerDir, execName)
	core.executeProgram(["./" + execName])
	core.executeProgram(["gcov", execName])

	return core.parseGcovOutput(execName + ".c.gcov")
# - Checking for previous computations 
# Searches for all the '.c' files in the current directory
for flnm in os.listdir('.'):
	extension =  os.path.splitext(flnm)
	if extension[1] == '.c':
		# Preprocessing Part
		preprocessor.replaceStr(flnm, r'typedef\s[a-z0-9_\s]+TARGET_TYPE', "typedef int TARGET_TYPE;\n")
		
		# InputGenerator Part
		inputgenerator.discoverParameters(extension[0])
		inputgenerator.listCreator("float")
		inputgenerator.generateHeaders("float")		
		
		# Profiling Phase
		# Creation of CSV File 
		with open('cStatements.csv', 'w') as csvfile:
			filewriter = csv.writer(csvfile, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)

			for directory in os.listdir('includes'):
				numberCstat = profilingPhase(flnm, extension[0], "includes/" + directory)
				filewriter.writerow([directory, numberCstat])