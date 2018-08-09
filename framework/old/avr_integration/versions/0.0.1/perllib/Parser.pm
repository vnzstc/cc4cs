#!/usr/bin/perl

# This package/class provides the functionalities to parse gcov and isasim file
# produced by mipsc process.
package Parser;

################################################################################
##### Constructor Methods                                                  #####
################################################################################

sub new {

	my $class = shift;
	my $self = {
		_isasim_path    => shift,
		_gcov_path      => shift,
		_changelog_path => shift,
	};

	bless $self, $class;
	return $self;
}

################################################################################
##### Setter Methods                                                       #####
################################################################################

# Setter function for _changelog_path attribute
sub setChangelogPath() {
	my ( $self, $changelogPath ) = @_;
	$self->{_changelog_path} = $changelogPath if defined($changelogPath);
	return $self->{_changelog_path};
}

# Setter function for _isasim_path attribute
sub setIsasimPath() {
	my ( $self, $isasimPath ) = @_;
	$self->{_isasim_path} = $isasimPath if defined($isasimPath);
	return $self->{_isasim_path};
}

# Setter function for _gcov_path attribute
sub setGCovPath() {
	my ( $self, $gcovPath ) = @_;
	$self->{_gcov_path} = $gcovPath if defined($gcovPath);
	return $self->{_gcov_path};
}

################################################################################
##### Getter Methods                                                       #####
################################################################################

# Getter function for _changelog_path attribute
sub getChangelogPath {
    my( $self ) = @_;
    return $self->{_changelog_path};
}

# Getter function for _isasim_path attribute
sub getIsasimPath {
    my( $self ) = @_;
    return $self->{_isasim_path};
}

# Getter function for _gcov_path attribute
sub getGCovPath {
    my( $self ) = @_;
    return $self->{_gcov_path};
}

################################################################################
##### Functional Methods                                                   #####
################################################################################

# This function opens the file provided in input $changelogPath variable.
# It reads its info and retrieve the version of mipsc ramework into
# output $version argument.
# INPUT  :
#		$changelogPath => path of the changelog file to parse.
#                     It expects this file to be the changelog file
#											of mipsc framework.
# OUTPUT :
#		$version => version of mipsc framework.
sub getMipscVersion {
	my ( $self, $changelogPath ) = @_;
	$self->{_changelog_path} = $changelogPath if defined($changelogPath);
	open (CHANGELOG, $self->{_changelog_path});

	while (<CHANGELOG>) {
		chomp;
		($label, $versionCH) = split(":");

		if ($label eq "## Version") {
			$version = $versionCH;
		}
	}

	return $version;
}

# This function opens the file provided in input $gcovPath variable.
# It reads its info and for each c program line retrieve the number of times
# it was executed.
# This function sums the times each line was executed, and put that info into
# output $cInstrExec argument.
# INPUT  :
#		$gcovPath => path of the gcov file to parse.
#                It expects this file to be the output gcov result for
#                .c program.
# OUTPUT :
#		$cInstrExec => total number of "c instruction" executed.
#                  It supposes that each program line contains
# 							   one and only one instruction.
sub parseGCovFile {
	my ( $self, $gcovPath ) = @_;
	$self->{_gcov_path} = $gcovPath if defined($gcovPath);
	open (STATS_GCOV, $self->{_gcov_path});
	$cInstrExec = 0;
	while (<STATS_GCOV>) {
		chomp;
		($nexec, $linenumber, $lineinstruction) = split(":");
		if ($nexec != "-") {
			$cInstrExec = $nexec + $cInstrExec;
		}
	}

	return $cInstrExec;
}

# This function opens the file provided in input $isasimPath variable.
# It reads its info and return variables into a hash.
# It sums the times each line was executed, and put that info into
# output $totnexec argument.
# INPUT  :
#		$isasimPath => path of the isasim file to parse.
#                It expects this file to be the isasim output simulation for
#                .c program.
# OUTPUT :
#   $assInstrExec     => number of assembly instruction executed
#                        during simulation
#   $execTimeLocal    => time elapsed on host machine for program exeution
#   $instrPerSecLocal => average number of instruction executed whithin
#                        one second on host machine
#		$clkCycleHit8051  => number of clock cycle took by Intel 8051 microprocessor
#                        for .c program execution.
#		$execTime8051     => time in seconds took by Intel 8051 microprocessor
#                        for .c program execution.
#		$instrPerSec8051  => average number of instruction executed whithin
#                        one second by Intel 8051 microprocessor
#                        for .c program execution.
#
sub parseIsasimFile {
	my ( $self, $isasimPath ) = @_;
	$self->{_isasim_path} = $isasimPath if defined($isasimPath);
	open (STATS_ISASIM, $self->{_isasim_path});

	while (<STATS_ISASIM>) {
		chomp;
		($info, $value) = split(":");

		$info =~ s/^\s*(.*?)\s*$/$1/;
		$value =~ s/^\s*(.*?)\s*$/$1/;

		if ( $info eq "Instructions Executed" ) {
			$assInstrExec = $value;
		} elsif ( $info eq "Execution Time(seconds)" ) {
			$execTimeLocal = $value;
		} elsif ( $info eq "Average Instructions/second" ) {
			$instrPerSecLocal = $value;
		} elsif ( $info eq "Clock Cycles Required for 8051" ) {
			$clkCycleHit8051 = $value;
		} elsif ( $info eq "Execution Time for 8051(12 MHz)(seconds)") {
			$execTime8051 = $value;
		} elsif ($info eq "Average Instructions/second for 8051") {
			$instrPerSec8051 = $value;
		} else {}

	}

	return ($assInstrExec, $execTimeLocal, $instrPerSecLocal,
		$clkCycleHit8051,$execTime8051,$instrPerSec8051);

}

1;
