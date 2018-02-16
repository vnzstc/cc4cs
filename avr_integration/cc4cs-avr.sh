#!/bin/bash

PRJPATH=$(pwd)
MAKEFILEPATH=~/mipsc/makefile
INPUTGENPATH=~/mipsc/input_gen.sh
ISSPATH=~/mipsc/8051.h
PERLPATH=~/mipsc
EXEPATH=$PRJPATH/exe
PRGNAME=$(echo *.c | cut -f 1 -d '.')

echo ""
echo "*********"
echo "** Deleting previous computations"
echo "*********"
echo ""
make cleandir --makefile=$MAKEFILEPATH

echo ""
echo "*********"
echo "** Input generation"
echo "*********"
echo ""
sh $INPUTGENPATH $PRJPATH/*.c
cp $ISSPATH $PRJPATH/includes

echo ""
echo "*********"
echo "** Preparing directory environment"
echo "*********"
echo ""
make checkdir_avr --makefile=$MAKEFILEPATH

echo ""
echo "*********"
echo "** Building with GCC compiler"
echo "*********"
echo ""
make build_gcc --makefile=$MAKEFILEPATH

echo ""
echo "*********"
echo "** Executing GCC builded program"
echo "*********"
echo ""


for directory in $EXEPATH/* ; do
   #echo "$directory"
	${directory}/${PRGNAME}_debug > ${directory}/${PRGNAME}_debug_output.txt
	${directory}/${PRGNAME}
   #echo ""
 	#echo "**Content of ${PRGNAME}_debug_output.txt in" $directory ":"
 	#cat ${directory}/${PRGNAME}_debug_output.txt
 	#echo ""
done

echo ""
echo "*********"
echo "** Running GCOV for GCC Builded program"
echo "*********"
echo ""
make stats_gcov --makefile=$MAKEFILEPATH
make install_gcov --makefile=$MAKEFILEPATH

echo ""
echo "*********"
echo "** Building with AVR-GCC compiler"
echo "*********"
echo ""

make build_avr --makefile=$MAKEFILEPATH

echo ""
echo "*********"
echo "** Running SIMULAVR for atmega328 simulation"
echo "*********"
echo ""

make stats_simulavr --makefile=$MAKEFILEPATH
make install_avr  --makefile=$MAKEFILEPATH


echo ""
echo "*********"
echo "** Calculate metric for atmega328"
echo "*********"
echo ""

avr_stat.sh > atmega328_report.txt
cat atmega328_report.txt