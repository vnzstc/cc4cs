#!/usr/bin/perl

use FindBin qw($Bin);
use lib "$Bin/perllib";

use ParserI8051;
use ReportTxt;
use ReportCsv;

################################################################################
##### Main                                                                 #####
################################################################################

@incites = ();

# parser object instantiation
$parser = new ParserI8051();

#This variable contains the number of instruction of a program execution.
$totnexec = 0;
#This static variable describes the frequency of i8051 microprocessor.
$freq8051 = 12000000;
# This static variable describes the average number of clock cycle
# i8051 took to process one of its assembly instruction
$avgCCHperAssemblyIntruction = 18;

# Set $prjPath variable:
# This variable is filled with the bash "pwd" command execution output.
$prjPath = `pwd`;
# Remove trailing spaces and breaklines from $prjPath.
chomp $prjPath;

# Set $prgname variable:
# $prgname is filled with the name of the only prog.c file name obtained by
# the bash "echo *.c | cut -f 1 -d '.'" command execution output.
$prgname = ` echo *.c | cut -f 1 -d '.' `;
# Remove trailing spaces and breaklines from $prgname.
chomp $prgname;

# Set @incites variable:
# A incite is a set of input values, which are evaluated within .c program
# execution.
# Each @incites component is filled with the distinct name of the directory
# which contains the incite's headers file with relative input values.
# See getIncites() method for more info.
@incites = @{getIncites()};

# This static variable contains the path to the mipsc project changelog file.
$changelogFilePath =  "/home/sim8051/workspaces/mipsc/mipsc/changelog";
# Obtain the version of the framework which is performing mipsc measures
# computation
$version = $parser->getMipscVersion($changelogFilePath);

foreach my $incite (@incites) {

  # Init Parsing Variables.
	$cInstrExec     = 0;
	$gcovFilePath   = "$prjPath/gcov/$incite/${prgname}.c.gcov";
	$isasimFilePath = "$prjPath/isasim/$incite/${prgname}_IsasimReport.txt";

  # Parsing gcov output file for total number of instruction executed.
	$cInstrExec = $parser->parseGCovFile($gcovFilePath);
  # Parsing isasim output file for Intel 8051 performance info.
	($assemblyInstructions, $localExeTime, $localInstrPerSec,
		$clkCycles8051,$exeTime8051,$avg8051) =
		   $parser->parseIsasimFile($isasimFilePath);

	# compute the estimeted number of clock cycles, by multiplying the
	# assembly instruction executed with the average number of clock cycle
	# per assembly instruction
    $clkCyclesAss = $assemblyInstructions * $avgCCHperAssemblyIntruction;
	# number of microseconds occurred to run the program
	$exeTime8051us = $exeTime8051 * 1000000 ;
	# 8051 frequency in Mhz
	$freq8051MHz = $freq8051 / 1000000 ;
	# average time took by 8051 microprocessor to execute 1 generic C intruction
	$timePerInstr8051 = $exeTime8051us / $cInstrExec ;
	# average number of clock cycles took by 8051 microprocessor
	# to execute 1 C intruction, this alue is computed using $timePerInstr8051
	$clockCyclePerInstrTpi = $timePerInstr8051 * $freq8051MHz ;
	# average number of clock cycles took by 8051 microprocessor
	# to execute 1 C intruction, this alue is computed using $clkCycles8051
	$clockCyclePerInstrClk = $clkCycles8051 / $cInstrExec ;

	# fill the incite array with computed values
	$statistics{$incite} = {
		cInstrExec              => $cInstrExec,
		assInstrExec            => $assemblyInstructions,
		execTime8051            => $exeTime8051,
		clockCycleAss           => $clkCyclesAss,
		clockCycle8051          => $clkCycles8051,
		timePerInstr8051        => $timePerInstr8051,
		clockCyclePerInstrClk   => $clockCyclePerInstrClk,
		clockCyclePerInstrTpi   => $clockCyclePerInstrTpi
	}; #$statiticsEntry
}

$mean = computeMean();
$variance = computeVariance();
$deviation = computeStandardDeviation();

$minimum = computeMin();
$maximum = computeMax();

printTxtReport();
printCsvReport();

################################################################################
##### Routines                                                             #####
################################################################################

sub printCsvReport {
	# csv report object instantiation
	$csvReport = new ReportCsv();

	$csvfilename = "${prgname}_I8051Report.csv";
	open ($csvfile, '>', $csvfilename) or die "Open file failed";

	# setting the visible and the non visible columns
	$csvReport->setHiddenFields(
		False, # $cInstrExec
		False, # $assInstrExec
		False, # $execTime8051
		False, # $clkCyclesAss
		False, # $clkCycle8051
		True,  # $timePerInstr8051
		False, # $clockCyclePerInstrClk
		True   # $clockCyclePerInstrTpi
	);

	#printing results csv
	$csvReport->printReportTableHeader($csvfile);
	foreach my $incite (@incites) {
		$csvReport->printReportTableEntry(
		  $csvfile,
			$incite,
			$statistics{$incite}{cInstrExec},              #$cInstrExec,
			$statistics{$incite}{assInstrExec},            #$assInstrExec,
			$statistics{$incite}{execTime8051},            #$execTime8051,
			$statistics{$incite}{clockCycleAss},           #$clkCycle8051,
			$statistics{$incite}{clockCycle8051},          #$clkCycle8051,
			$statistics{$incite}{timePerInstr8051},        #$timePerInstr8051,
			$statistics{$incite}{clockCyclePerInstrClk},   #$clockCyclePerInstrClk
			$statistics{$incite}{clockCyclePerInstrTpi}    #$clockCyclePerInstrTpi
		);

	}
	$csvReport->printReportTableFooter($csvfile);
	$csvReport->printReportSummary(
	   $csvfile,
	   $minimum,
		 $maximum,
		 $mean,
		 $variance,
		 $deviation,
		 $version
	);

	close $csvfile;
}

sub printTxtReport {
	# textual report object instantiation
	$txtReport = new ReportTxt();

	$txtfilename = "${prgname}_I8051Report.txt";
	open ($txtfile, '>', $txtfilename) or die "Open file failed";

	# setting the visible and the non visible columns
	$txtReport->setHiddenFields(
		False, # $cInstrExec
		False, # $assInstrExec
		False, # $execTime8051
		False, # $clkCyclesAss
		False, # $clkCycle8051
		True,  # $timePerInstr8051
		False, # $clockCyclePerInstrClk
		True   # $clockCyclePerInstrTpi
	);

	#printing results table
	$txtReport->printReportTableHeader($txtfile);
	foreach my $incite (@incites) {
		$txtReport->printReportTableEntry(
			$txtfile,
			$incite,
			$statistics{$incite}{cInstrExec},              #$cInstrExec,
			$statistics{$incite}{assInstrExec},            #$assInstrExec,
			$statistics{$incite}{execTime8051},            #$execTime8051,
			$statistics{$incite}{clockCycleAss},           #$clkCycle8051,
			$statistics{$incite}{clockCycle8051},          #$clkCycle8051,
			$statistics{$incite}{timePerInstr8051},        #$timePerInstr8051,
			$statistics{$incite}{clockCyclePerInstrClk},   #$clockCyclePerInstrClk
			$statistics{$incite}{clockCyclePerInstrTpi}    #$clockCyclePerInstrTpi
		);

	}
	$txtReport->printReportTableFooter($txtfile);
	$txtReport->printReportSummary(
	   $txtfile,
	   $minimum,
		 $maximum,
		 $mean,
		 $variance,
		 $deviation,
		 $version
	);

	close $txtfile;
}

sub getIncites {
   my @incitesUnsort;

	 opendir( my $DIR, "./includes/" );
	 while ( my $entry = readdir $DIR ) {
	     next unless -d "./includes/"  . '/' . $entry;
	     next if $entry eq '.' or $entry eq '..';
	     push (@incitesUnsort, $entry);
	 }
	 closedir $DIR;

	 my @incites = sort { lc($a) cmp lc($b) } @incitesUnsort;

	 return \@incites;

}

sub computeMax {
	$max = 0;
	foreach my $incite (@incites) {
		$aux = $statistics{$incite}{clockCyclePerInstrClk};
		if ($max < $aux) {
			$max = $aux
		}
	}
	return $max;
}

sub computeMin {
	$min = 0;
	foreach my $incite (@incites) {
		$aux = $statistics{$incite}{clockCyclePerInstrClk};
		if (( $min > $aux ) or ( $min == 0 )) {
			$min = $aux;
		}
	}
	return $min;
}

sub computeMean {
	$mean = 0;
	$sum = 0;
	$count = 0;

	foreach my $incite (@incites) {
		$sum = $sum + $statistics{$incite}{clockCyclePerInstrClk};
		$count = $count + 1;
	}

	$mean = $sum / $count;
	return $mean;
}

sub computeVariance {
	$variance = 0;
	$sum = 0;
	$inciteDistance = 0;
	$inciteDistance2 = 0;
	$count = 0;

	foreach my $incite (@incites) {
		$inciteDistance = $statistics{$incite}{clockCyclePerInstrClk} - $mean;
		$inciteDistance2 = $inciteDistance * $inciteDistance;
		$sum = $sum + $inciteDistance2;
		$count = $count + 1;
	}

	$variance = $sum / ($count);
	return $variance;
}

sub computeStandardDeviation {
	$deviation = 0;

	$deviation = sqrt($variance);
	return $deviation;
}

exit;
