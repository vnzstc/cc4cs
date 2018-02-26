#!/bin/bash

PRJPATH=$(pwd)
GCOVPATH=$PRJPATH/gcov 
AVRESPATH=$PRJPATH/simulavr
PRGNAME=$(echo *.c | cut -f 1 -d '.')
# NUMDIR=$(($(ls includes/| wc -l)-1))

# This function is used to parse gcov .c.gcov file and get the number of c total statements 
function total_statem
{	
	res=0
	while read p; do 
		# Gets the first column of a .c.gcov file 
    	temp=$(echo $p | awk '{ print $1 }' | grep -o -m 1 -E '[0-9]+')
    	if [ -n $temp ]; then 
    		res=$((res+temp))
    	fi
	done < $1
}

# This function is used to parse the simulavr output to get number of clock cycles requested
function get_clockcycles
{
	while read p; do 
		ccy=$(echo $p | grep -o -E '[0-9]+')
	done < $1
}
 
# This function is used to calculate the metric
function calc_metric
{
	freq=4;
	echo "Incite; Executed C Instr; Clock Cycle Effective; Execution Time; CC4CS;"
	for directory in $GCOVPATH/*; do 
		total_statem $directory/$PRGNAME.c.gcov
		get_clockcycles $AVRESPATH/$(basename $directory)/$PRGNAME\_avreport.txt 
		cc4cs=$(bc -l <<< "scale=3;$ccy/$res")
		exetime=$(bc -l <<< "scale=3;$ccy/$freq")
		echo "$(basename $directory); $res; $ccy; $exetime; $cc4cs"
	done
}

calc_metric
