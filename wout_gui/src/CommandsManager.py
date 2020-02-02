from re import search
from subprocess import call
from os.path import isdir, join
from os import chdir, makedirs, listdir
from csv import DictWriter
from shutil import rmtree

class CommandsMananger:
	def __init__(self, functionPath, scriptPath, functionName, workingDir):
		self.functionName = functionName
		self.functionPath = functionPath
		self.scriptPath = scriptPath
		self.workingDir = workingDir

	def expandCommand(self, compactCmd, directory, prjPath):
		# The expandCommand function replaces the placeholders contained in .json file with their actual values
		if '[functionPath]' in compactCmd:
			compactCmd = compactCmd.replace('[functionPath]', self.functionPath)

		if '[functionName]' in compactCmd:
			compactCmd = compactCmd.replace('[functionName]', self.functionName)

		if '[prjPath]' in compactCmd:
			compactCmd = compactCmd.replace('[prjPath]', prjPath + '/')

		if '[scriptPath]' in compactCmd:
			compactCmd = compactCmd.replace('[scriptPath]', self.scriptPath)

		if '[directoryName]' in compactCmd:
			compactCmd = compactCmd.replace('[directoryName]', directory)

		return compactCmd

	def executeCommand(self, cmd):
		outputFile = search(r'[^:\/;]\{(.*?)\}', cmd)
		flags = cmd.split(" ")

		if outputFile:
			outputFile = outputFile.group(1)
			flags.remove('{' + outputFile + '}')
	
			with open(outputFile, 'w') as obj:
				call(flags, stdout = obj)
		else:
			call(flags)

	def executeCommandSet(self, cmdSet, inputsPath, parsingFunction = None, debugFlag = False):
		# Changes working directory 
		chdir(self.workingDir)
		
		# Gets the list of commands
		jsonEntry = cmdSet["dependencies"].split(" ")			
		dirs = [f for f in listdir(inputsPath) if isdir(join(inputsPath, f))]

		# Creates the directory containing the files produced during the execution
		filesDir = "files"
		makedirs(filesDir)

		for dirName in dirs:
			filesPath = self.workingDir + '/' + filesDir + '/' + dirName
			# Creates the subdirectory containing the files produced for each input
			makedirs(filesPath)
			chdir(filesPath)

			for entry in jsonEntry:
				cmd = cmdSet[entry]
				# Changes the values of the eventual placeholders in real ones
				completedCmd = self.expandCommand(cmd, dirName, self.workingDir)
				self.executeCommand(completedCmd)

			# Calls the function to parse the output	
			if parsingFunction: parsingFunction(filesPath + '/' + self.functionName, values = [dirName])

			# Restores the previous working directory
			chdir(self.workingDir)

			if debugFlag: rmtree(filesDir)