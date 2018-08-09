#!/bin/bash

PRJPATH=$(pwd)
MAKEFILEPATH=~/workspaces/mipsc/mipsc/makefile
PERLPATH=~/workspaces/mipsc/mipsc
EXEPATH=$PRJPATH/exe
PRGNAME=$(echo *.c | cut -f 1 -d '.')

echo "PRJ PATH is: $PRJPATH"

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
echo "** Executing GCC builded program"
echo "*********"
echo ""


for directory in $EXEPATH/* ; do
  echo "$directory"
	${directory}/${PRGNAME}_debug > ${directory}/${PRGNAME}_debug_output.txt
	${directory}/${PRGNAME}
  echo ""
	echo "**Content of ${PRGNAME}_debug_output.txt in" $directory ":"
	cat ${directory}/${PRGNAME}_debug_output.txt
	echo ""
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

echo "*********"
echo "** Running perl script for data syntesys calculation"
echo "*********"
echo ""

$PERLPATH/mipsc.pl > $PRJPATH/${PRGNAME}Report.txt
cat $PRJPATH/${PRGNAME}Report.txt
