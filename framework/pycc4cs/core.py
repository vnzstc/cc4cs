import subprocess
"""
	This function is needed to compile a couple (algorithm + the trace)
"""
def compileWithGCC(filePath, tracePath, execName):
	traceFlag = "-I" + tracePath
	cmd = ["gcc", filePath, "-fprofile-arcs", "-ftest-coverage", "-Iincludes", traceFlag, "-o", execName]
	subprocess.call(cmd)
"""
"""
def executeProgram(flagList):
	subprocess.call(flagList)
"""
"""
def parseGcovOutput(txtFilePath):
	result = 0
	with open(txtFilePath, "r") as file:
		for line in file:
			number = file.readline().split(':')[0]
			number = number.strip()
			if number.isdigit():
				result += int(number)

	return result