from os.path import isdir, join
from os import listdir
from re import search, findall
from csv import DictWriter, reader
from os.path import isfile

class Parser:
    def __init__(self, outputPath, parsingFunction, headers = []):
        self.outputPath = outputPath
        self.parsingFunction = parsingFunction
        self.headers = headers

    def writeFile(self, row):
        # output file access mode
        flag = 'w'

        if isfile(self.outputPath): flag = 'a'
        # Creates the output file 
        with open(self.outputPath, flag) as outFile:
            wrt = DictWriter(outFile, fieldnames = self.headers)

            # If headers is a field of the object, then they are written on the output file
            if flag == 'w': wrt.writeheader()
            wrt.writerow(row)

    def run(self, parserInput, values = []):

        # Executes the parsing function 
        results = self.parsingFunction(parserInput)
        values.extend(results)

        # Writes the values
        self.writeFile({key:value for key, value in zip(self.headers, values)})

    def gcovParser(filePath):
        """This function analyzes the output of GCov profiler

        Args:
            txtfilePath (string): the name of the .c.gcov file.

        Returns:
            int: the number of executed C statements
        """
        result = 0
        with open(filePath + ".c.gcov", "r") as file:
            for line in file:
                number = line.split(':')[0]
                number = number.strip()
                if number.isdigit():
                    result += int(number)

        return [result]

    def thumbParser(filePath):
        results = []
        with open(filePath + ".txt", "r") as execFile:
            content = execFile.read()

            cycleStr = search(r'(\d+)\s+ticks', content)
            assemblyInst = search(r'(\d+)\s+instructions', content)

            print(cycleStr.group(1))
            print(assemblyInst.group(1))

            if cycleStr: results.append(cycleStr.group(1))
            if assemblyInst: results.append(assemblyInst.group(1))

        return results

    def simParser(filePath):
        """Generic parsing for the output file of an ISS

        Args:
            simFilename (string):  the name of the file that contains simulation information

        Returns:
            string: number of clock cycles

        Todo:
            * Not Generic, it works only with the micros already tested
        """
        results = []
        with open(filePath + ".txt", "r") as execFile:
            content = execFile.read()

            cycleStr = search(r'([cC]ycles.*?:\s*)(\d+)', content)
            assemblyInst = search(r'([iI]nstructions.*?:\s*)(\d+(.\d+)?)', content)

            print(cycleStr.group(2))
            print(assemblyInst.group(2))

            if cycleStr: results.append(cycleStr.group(2))
            if assemblyInst: results.append(assemblyInst.group(2))

        return results

    def getHeaders(self, args, pascalCase = False):
        """ This functions extracts the needed information from a FramaC output file
        """
        filePath, idxStart, idxEnd, regex = args
        headers = []

        with open(filePath, 'r') as fp:
            lines = fp.readlines()[idxStart:idxEnd]
            for ln in lines:
                key = search(regex, ln)

                if key:
                    # Removes the last char (e.g. :)
                    key = key.group()[:-1]
                    # Puts the string in pascal case
                    if pascalCase: key = ''.join(x for x in key.title() if not x.isspace())

                    headers.append(key)

        return headers

    def getFramaRow(args):
        filePath, idxStart, idxEnd = args
        content = []

        with open(filePath, 'r') as fp:
            lines = fp.readlines()[idxStart:idxEnd]
            for ln in lines:
                value = search(r'\d+\.?\d+', ln)
                if value: content.append(value.group())

        return content

    def getInputsRow(self, args, values = []):
        filePath, idxStart, idxEnd = args

        with open(filePath, 'r') as fp:
            lines = fp.readlines()[idxStart:idxEnd]
            # Removes the last element from the array that is a useless line
            lines = lines[:-1]
            content = []

            for ln in lines:
                value = ln.split('=')[1]
                value = value.replace('=', '').strip()
                value = value.replace(';', '')
                occurrences = value.count('}')
                if occurrences <= 1:
                    value = value.replace('}', '')
                else:
                    value = value.replace('{', '[')
                    value = value.replace('}', ']')

                content.append(value)

        self.writeFile({key:value for key, value in zip(self.headers, content)})

    def framaParser(self, inputsPath, analysisFlag):
        dirs = [f for f in listdir(inputsPath) if isdir(join(inputsPath, f))]
        # Gets the headers from the output file
        self.headers = ["inputName"]
        idxStart = 4

        # Halsted output parsing
        if analysisFlag:
            fileName = "Halsted.txt"
            idxEnd = 15
            # Parameters for the Halsted file
            filesPath = inputsPath + "/values_0/" + fileName
            params = [filesPath, idxStart, idxEnd, r'([a-zA-Z_]+\s?)*:']

        else:
            # McCabe output parameters 
            fileName = "McCabe.txt"
            idxEnd = None
            filesPath = inputsPath + "/values_0/" + fileName
            params = [filesPath, idxStart, idxEnd, r'(\w+\s)+=']

        self.headers.extend(self.getHeaders(params, pascalCase = True))

        for dirName in dirs:
            filesPath = inputsPath + '/' + dirName + '/' + fileName
            params = [filesPath, idxStart, idxEnd]
            self.run(params, values = [dirName])

    def inputParser(self, inputsPath):
        dirs = [f for f in listdir(inputsPath) if isdir(join(inputsPath, f))]
        # Gets the headers from the output file
        self.headers = ["inputName"]
        filesPath = inputsPath + "/values_0/values.h"
        params = [filesPath, 2, None, r'[a-z\[\]]+\s=']

        tempHeaders = map(str.strip, self.getHeaders(params))
        self.headers.extend(tempHeaders)

        for dirName in dirs:
            filesPath = inputsPath + '/' + dirName + '/values.h'
            params = [filesPath, 2, None]
            self.getInputsRow(params, values = [dirName])
