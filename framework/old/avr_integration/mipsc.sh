#!/bin/bash

PRJPATH=$(pwd)
MAKEFILEPATH=~/workspaces/mipsc/mipsc/makefile
INPUTGENPATH=~/workspaces/mipsc/mipsc/input_gen.sh
H8051PATH=~/workspaces/mipsc/mipsc/templates/8051.h
PERLPATH=~/workspaces/mipsc/mipsc
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
echo "** Preparing directory environment"
echo "*********"
echo ""
make checkdir --makefile=$MAKEFILEPATH

echo ""
echo "*********"
echo "** Building with GCC compiler"
echo "*********"
echo ""
make build_gcc --makefile=$MAKEFILEPATH
echo ""
echo "*********"
echo "** Building with SDCC compiler"
echo "*********"
echo ""
make build_sdcc --makefile=$MAKEFILEPATH
echo ""
echo "*********"
echo "** Building with SPARC compiler"
echo "*********"
echo ""
make build_sparc --makefile=$MAKEFILEPATH

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
echo "** Running ISASIM for SDCC program simulation"
echo "*********"
echo ""
make stats_isasim --makefile=$MAKEFILEPATH
make install_isasim  --makefile=$MAKEFILEPATH

echo ""
echo "*********"
echo "** Running TSIM for SPARC program simulation"
echo "*********"
echo ""
make stats_tsim --makefile=$MAKEFILEPATH
make install_tsim  --makefile=$MAKEFILEPATH

echo "*********"
echo "** Running perl script for I8051 data syntesys calculation"
echo "*********"
echo ""

#$PERLPATH/mipsc_i8051.pl > $PRJPATH/${PRGNAME}_I8051Report.txt
$PERLPATH/mipsc_i8051.pl
cat $PRJPATH/${PRGNAME}_I8051Report.txt

echo "*********"
echo "** Running perl script for SPARC data syntesys calculation"
echo "*********"
echo ""

#$PERLPATH/mipsc_sparc.pl > $PRJPATH/${PRGNAME}_sparcReport.txt
$PERLPATH/mipsc_sparc.pl
cat $PRJPATH/${PRGNAME}_sparcReport.txt
