#!/bin/bash

cat << EOF > pyscript.py 
#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,mmap,re
from itertools import product
from collections import OrderedDict
from random import randint
from random import uniform


ranges = {}
values = OrderedDict()

def ask_ranges_inputs(var_list):
	""" 
		For each discovered parameter, ask_ranges_steps function, asks the user to enter ranges 
		and, in case, number of inputs for non-array variables.
		the function ensures that the user has inserted right parameters using regular expressions
	"""

	for ele in var_list:

		if ele.find('[') != -1:

			input_str = raw_input('Enter range for '  + '"' + ele + '"' + ': ')
			pattern = re.match('\[(\d,\d)\]', input_str)

		else:
			
			input_str = raw_input('Enter range and number of tests for ' + '"' + ele + '"' + ' separated by a semicolon: ')
			pattern = re.match('\[(\d,\d)\];[1-9][0-9]*', input_str)

		#check_input(input_str, pattern, ele)
		ranges[ele] = input_str

def clean_prototype(arg_string):
	""" 
		This functions takes in input the prototype as a string a returns the specified parameters as a list 
	"""
	arg_string = arg_string.replace(", ",",")
	arg_string = arg_string.replace("prototype(","")
	arg_string = arg_string.replace(");\n","")
	variables = arg_string.split(',')

	return variables

def clean_range(str_range):
	""" 
		The purpouse of this function is to retrieve numbers from the range's string
	""" 
	str_range = str_range.replace('[', '')
	str_range = str_range.replace(']','')
	range_list = str_range.split(',')

	return range_list

def discover_parameters():
	""" 
		This function opens the indicate .c program as a memory-mapped file and searches 
		for a prototype called "prototype" where are defined the parameters that the function takes in input 
	"""
	file_function = open(sys.argv[1])
	mm = mmap.mmap(file_function.fileno(), 0, access=mmap.ACCESS_READ)

	index = mm.find('prototype')

	if index != -1:
		mm.seek(index)
		var_list = clean_prototype(mm.readline())
		ask_ranges_inputs(var_list)

	else:
		raise ValueError("prototype not found")

def calculate_values(range, inputs):
	""" 
		Takes in input the range and the step and returns a list with values defined as follows:
		Range = [Min, Max]
		K = Max - Min
		{Min,
		 Min + K * (Step * i)
		 	:
		 	:
		 Max 
		}

		With i incremented until it reaches the Max values
 	"""

	values = clean_range(range)

	# values[0] = min and values[1] = max
	k = int(values[1]) - int(values[0])

	# calculate the step from the number of inputs that the user have indicated previously
	step = 1/(float(inputs)-1)

	list_of_values = [int(values[0])]
	current_value = float(values[0])

	multiplier = 1;

	while current_value < float(values[1]):

		current_value = int(values[0]) + (k * (float(step) * multiplier))
		list_of_values.append(current_value)
		multiplier += 1

	return list_of_values


def calculate_random_values(user_range, inputs):
	"""
		This function generates random values for variables, within the range indicated in user_range
		Return values: list that contains values to combine
	"""
	values = clean_range(user_range)

	list_of_values = [int(values[0])]

	for i in range(int(inputs)-1):
		current_value = randint(int(values[0]), int(values[1]))
		list_of_values.append(current_value)

	return list_of_values


def list_generation():
	"""
		For each non-array variable in "ranges" dictionary, generates a list that contains the values to 
		write in each output file.
	"""
	for key in ranges.keys():

		if key.find('[') == -1:
			app_list = ranges[key].split(';')

			# Adds the calculated list in "values" OrderedDictionary as --> Variable Name : List 
			# values[key] = calculate_values(app_list[0],app_list[1])
			values[key] = calculate_random_values(app_list[0], app_list[1])
			# Removes the variable from the ranges dictionary
			ranges.pop(key)


def find_var(ele):

	"""
		This functions check if a variables is a size of an array
		If yes returns a tuple (variable_index, variable_values). If not returns -1
	"""

	for i, var in enumerate(values):
		if var.find(ele) != -1:
			return (i, var)

	return -1

def write_monodimensional(range, array_size, output_file):
	""" 
		Writes a monodimensional array in the output file 
	"""
	range_values = clean_range(range)



	i = 0
	while i < int(round(array_size)-1):

		# This "if" statement checks is the range is composed by integers or float numbers
		
		if i == 0:
			var = 0
		else:	
			var = randint(int(range_values[0]), int(range_values[1]))

		# var = uniform(float(range_values[0]), float(range_values[1]))

		output_file.write(str(var) + ', ')
		i += 1
	
	# var = uniform(float(range_values[0]), float(range_values[1]))
	var = randint(int(range_values[0]), int(range_values[1]))
	output_file.write(str(var) + '};\n')

def write_multidimensional(range, array_size, output_file):
	""" 
		Writes a multidimensional array in the output file 
	"""
	range_values = clean_range(range)

	i = 0
	j = 0

	while i  < int(round(array_size[0])):

		j = 0
		while j < int(round(array_size[1])-1):
			var = randint(int(range_values[0]), int(range_values[1]))
			# var = uniform(float(range_values[0]), float(range_values[1]))
			output_file.write(str(var) + ', ')
			j += 1

		var = randint(int(range_values[0]), int(range_values[1]))	
		# var = uniform(float(range_values[0]), float(range_values[1]))

		if i < int(round(array_size[0]))-1:
			output_file.write(str(var) + '},\n\t   {')
		else:
			output_file.write(str(var) + '}};\n')

		i += 1

def write_variables(combination,output_file):

	"""
		This function write variables in the output file.
		For first write arrays that are contained in the ranges dictionary and their size,
		then the remaining variables
	"""

	# List to remember variables to write
	var_to_write = []
	for key in values:
		var_to_write.append(key)

	# Give me all the words between curly brackets 
	for array_name in ranges:

		# Find all alphanumeric char in array_name, find the size for the current array
		sizes = re.findall("[a-zA-Z0-9_]+", array_name)
		# The first found is always the name so we pop it beacause we don't need it
		sizes.pop(0)
		sizes.pop(0)

		# Define array sizes values
 		for i, ele in enumerate(sizes):

 			# For first we check if a variabile is a size of current array then retrieves the value 
 			# by index suggested by the current combination

			var_specs = find_var(ele)
			value_position = combination[var_specs[0]]
			value = (values[var_specs[1]])[value_position]

			# This check serves to avoid ripetitive write in case of bidimensional square arrays
			if var_specs[1] in var_to_write:
				output_file.write("\tenum{ " + ele + " = " + str(int(round(value))) + " };\n")	
				var_to_write.remove(var_specs[1])

			sizes[i] = value

		if len(sizes) == 1:
			output_file.write("\t" + array_name + "\n\t= {")
			write_monodimensional(ranges[array_name], sizes[0], output_file)
		else:
			output_file.write("\t" + array_name + "\n\t= {{")
			write_multidimensional(ranges[array_name], sizes, output_file)

	# Writing remaining variables
	for var in var_to_write:
		position = values.keys().index(var)
		value_position = combination[position]
		value = (values[var])[value_position]

		output_file.write("\t" + var + " = " + str(int(round(value))) + ";\n")

def create_output_file(first_index, second_index):
	"""
		This function creates the output file.
		Returns the object that rappresents the file
	""" 

	basic = "#ifndef VALUES\n#define VALUES\n"

	output = open('values_' + str(first_index) + str(second_index) + '.h', 'w+')
	output.write(basic)

	return output

def count_lenghts():
	"""
		This function discover the generated list lenghts.
		The lenghts will be combined to generate the indexes
	"""
	counts = []
	for key, val in values.iteritems():
		counts.append(len(val))

	return counts

def generate_combinations():

	""" 
		This function generates combinations of the values contained in the previously calculated lists.
		In particular it generates the index of the lists in which the value is.
		In general it combines indexes and then accesses by index, the correspondent list,
		to retrieve the value.
	"""

	counts = count_lenghts()
	iterate = [range(x) for x in counts]

	index_file = 0
	for combination in product(*iterate):
		
		# For each combination generates 10 random arrays
		for i in range(10):
			output_file = create_output_file(index_file, i)
			write_variables(combination, output_file)
			output_file.write("#endif")
			output_file.close()		
				
		# break
		index_file += 1

if __name__ == '__main__':

	# Module 1: Input Management
	discover_parameters();
	# Module 2: Creation of lists
	list_generation();
	# Module 3: Generation of combinations
	generate_combinations()

EOF

chmod 755 pyscript.py

./pyscript.py ${@}


rm pyscript.py

# If "includes" already exist then delete it 
if [ -d "includes" ]; then
	rm -r ./includes/*
	rm -r ./includes
fi

# Create "includes" directory that will contain the inputs
mkdir "includes"

for f in values_*.h; 
do
	mkdir "${f%.h}"
	mv ${f} ./"${f%.h}"
	mv ./"${f%.h}"/${f} ./"${f%.h}"/"values.h"
	mv ./"${f%.h}" ./includes
done
