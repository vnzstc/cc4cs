#!/usr/bin/perl

##################################################
####
#### Routines
####
##################################################

@incites = ();

#$prjPath = ".";
$totnexec = 0;
$freq8051 = 12000000;

$prjPath = `pwd`;
chomp $prjPath;
@incites = @{getIncites()};
$prgname = ` echo *.c | cut -f 1 -d '.' `;
chomp $prgname;

foreach my $incite (@incites) {

	$gcovFilePath = "$prjPath/gcov/$incite/${prgname}.c.gcov";
	$isasimFilePath =  "$prjPath/isasim/$incite/${prgname}_IsasimReport.txt";

	$totnexec = 0;
	$totnexec = parseGCovFile($gcovFilePath);
	$exeTime8051 = parseIsasimFile($isasimFilePath);

	$exeTime8051us = $exeTime8051 * 1000000 ;
	$freq8051MHz = $freq8051 / 1000000 ;
	$avgTPI = $exeTime8051us / $totnexec ; # avgTPI =~ avgTimePerInstruction
	$avgCCPI = $avgTPI * $freq8051MHz ; # avgCCPI =~ avgClkCyclePerInstruction

	$statistics{$incite} = {totnexec=>$totnexec, exeTime8051=>$exeTime8051, avgTPI=>$avgTPI, avgCCPI=>$avgCCPI}; #$statiticsEntry
}

$mean = computeMean();
$variance = computeVariance();
$deviation = computeStandardDeviation();

$minimum = computeMin();
$maximum = computeMax();

#printReport(\%statitics);
printReportTableHeader();
printReportTable(\%statitics);

print "\n";
print "*************************************";
print "\n\n";
print "The CCPI min is: $minimum";
print "\n";
print "The CCPI max is: $maximum";
print "\n";
print "The CCPI mean is: $mean";
print "\n";
print "The CCPI variance is: $variance";
print "\n";
print "The CCPI standard deviation is: $deviation";
print "\n\n";
print "*************************************";
print "\n";
print "\n";

close (FILE);

##################################################
####
#### Routines
####
##################################################

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
		$aux = $statistics{$incite}{avgCCPI};
		if ($max < $aux) {
			$max = $aux
		}
	}
	return $max;
}

sub computeMin {
	$min = 0;
	foreach my $incite (@incites) {
		$aux = $statistics{$incite}{avgCCPI};
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
		$sum = $sum + $statistics{$incite}{avgCCPI};
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
		$inciteDistance = $statistics{$incite}{avgCCPI} - $mean;
		$inciteDistance2 = $inciteDistance * $inciteDistance;
		$sum = $sum + $inciteDistance2;
		$count = $count + 1;
	}

	$variance = $sum / ($count - 1);
	return $variance;
}

sub computeStandardDeviation {
	$deviation = 0;

	$deviation = sqrt($variance);
	return $deviation;
}

sub parseGCovFile {

	my ($file) = @_ ;
	open (STATS_GCOV, $file);

	while (<STATS_GCOV>) {
		chomp;
		($nexec, $linenumber, $lineinstruction) = split(":");

		if ($nexec != "-") {
			$totnexec = $nexec + $totnexec;
		}
	}

	return $totnexec;
}

sub parseIsasimFile {

	my ($file) = @_ ;
	open (STATS_ISASIM, $file);

	while (<STATS_ISASIM>) {
		chomp;
		($info, $value) = split(":");

		$info =~ s/^\s*(.*?)\s*$/$1/;
		$value =~ s/^\s*(.*?)\s*$/$1/;

		if ( $info eq "Clock Cycles Required for 8051" ) {
			$clkCycles8051 = $value;
		} elsif ( $info eq "Execution Time for 8051(12 MHz)(seconds)") {
			$exeTime8051 = $value;
		} elsif ($info eq "Average Instructions/second for 8051") {
			$avg8051 = $value;
		} else {}

	}

	return $exeTime8051;
}

sub printReport{

	foreach my $incite (@incites) {

		print "Values for incite $incite:";
		print "\n";
			print "\tTotal number of Executed Instruction : $statistics{$incite}{totnexec}";
		print "\n";
			print "\tExecution Time for 8051 : $statistics{$incite}{exeTime8051} sec";
		print "\n";
			print "\tAverage Time Per Instruction : $statistics{$incite}{avgTPI} usec";
		print "\n";
			print "\tAverage number of Clock Cycle Per Instruction : $statistics{$incite}{avgCCPI}";
		print "\n";
		print "\n";
	}

}

sub printReportTableHeader{

		print "*************|*************|***********|******************|********************** \n";
		print "*   Incite   | Executed    | Execution | Average Time per | Average Clock Cycle * \n";
		print "*            | Instruction | Time      | Instruction      | per Instruction     * \n";
		print "*************|*************|***********|******************|********************** \n";

}

sub printReportTable{

  $inciteStr = ""; # 10 char
	$totnexecStr = ""; # 11 char
	$exeTime8051Str = ""; # 9 char
	$avgTPIStr = ""; # 16 char
	$avgCCPIStr = ""; # 19 char

	foreach my $incite (@incites) {

    $inciteStr = normString($incite, 10);
		$totnexecStr = normString($statistics{$incite}{totnexec}, 11);
		$exeTime8051Str = normString($statistics{$incite}{exeTime8051}, 9);
		$avgTPIStr = normString($statistics{$incite}{avgTPI}, 16);
		$avgCCPIStr = normString($statistics{$incite}{avgCCPI}, 19);

		print "*************|*************|***********|******************|********************** \n";
		print "* $inciteStr | $totnexecStr | $exeTime8051Str ";
		print "| $avgTPIStr | $avgCCPIStr * \n";

	}

}

sub normString {

	$string = $_[0] ;
	$length = $_[1] ;

	$str_len = length($string);

	if ($str_len < $length) {
		for (my $i=0; $i < ($length-$str_len); $i++)
		{
      $string = "$string ";
		}
	}

	return $string;
}

exit;
