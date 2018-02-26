import os
import preprocessor 
import inputgenerator


types = ["int", "long", "float"]
print("\n\n ██████╗ ██████╗██╗  ██╗ ██████╗███████╗\n"+
	  "██╔════╝██╔════╝██║  ██║██╔════╝██╔════╝\n"+
	  "██║     ██║     ███████║██║     ███████╗\n"+
	  "██║     ██║     ╚════██║██║     ╚════██║\n"+
	  "╚██████╗╚██████╗     ██║╚██████╗███████║\n"+
	  " ╚═════╝ ╚═════╝     ╚═╝ ╚═════╝╚══════╝\n")


# The script must be launched in the working directory 
for flnm in os.listdir('.'):
	extension =  os.path.splitext(flnm)
	if extension[1] == '.c':
		# Preprocessing Part
		preprocessor.replaceStr(flnm, r'typedef\s[a-z0-9_\s]+TARGET_TYPE', "typedef int TARGET_TYPE;\n")
		# InputGenerator Part
		inputgenerator.discoverParameters(extension[0])
		inputgenerator.listCreator("float")
		inputgenerator.generateHeaders("float")