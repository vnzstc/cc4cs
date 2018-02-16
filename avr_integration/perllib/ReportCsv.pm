#!/usr/bin/perl

# This package/class provides the functionalities to print reults
# produced by mipsc process.
package ReportCsv;

################################################################################
##### Constructor Methods                                                  #####
################################################################################

sub new {

	my $class = shift;
	my $self = {
		_hidden_fields => shift,
	};

	bless $self, $class;
	return $self;
}

################################################################################
##### Setter Methods                                                       #####
################################################################################

# Setter function for _hidden_fields attribute
sub setHiddenFields {
	my ( 	$self,
				$cInstrExec,
				$assInstrExec,
				$execTime8051,
				$clkCycleAss,
				$clkCycle8051,
				$timePerInstr8051,
				$clockCyclePerInstrClk,
				$clockCyclePerInstrTpi
	) = @_;

	$self->{_hidden_fields}{cInstrExec}
		= $cInstrExec            if defined($cInstrExec);
	$self->{_hidden_fields}{assInstrExec}
		= $assInstrExec          if defined($assInstrExec);
	$self->{_hidden_fields}{execTime8051}
		= $execTime8051          if defined($execTime8051);
	$self->{_hidden_fields}{clockCycleAss}
		= $clkCycleAss           if defined($clkCycleAss);
	$self->{_hidden_fields}{clockCycle8051}
		= $clkCycle8051          if defined($clkCycle8051);
	$self->{_hidden_fields}{timePerInstr8051}
		= $timePerInstr8051      if defined($timePerInstr8051);
	$self->{_hidden_fields}{clockCyclePerInstrClk}
		= $clockCyclePerInstrClk if defined($clockCyclePerInstrClk);
	$self->{_hidden_fields}{clockCyclePerInstrTpi}
		= $clockCyclePerInstrTpi if defined($clockCyclePerInstrTpi);
}

################################################################################
##### Functional Methods                                                   #####
################################################################################

# This function prints the header of result table
# INPUT  :
#		NONE
# OUTPUT :
#		NONE
sub printReportTableHeader {

	  my ( $self,$file ) = @_;

		print $file "Incite; ";
		if ( $self->{_hidden_fields}{cInstrExec}            eq False ) {
			print $file "Executed C Instr; ";	                    }
		if ( $self->{_hidden_fields}{assInstrExec}          eq False ) {
			print $file "Executed Ass Instr; ";	                  }
		if ( $self->{_hidden_fields}{execTime8051}          eq False ) {
			print $file "Execution Time; ";	                      }
		if ( $self->{_hidden_fields}{clockCycleAss}         eq False ) {
			print $file "Clock Cycle Expected Ass; ";	            }
		if ( $self->{_hidden_fields}{clockCycle8051}        eq False ) {
			print $file "Clock Cycle Effective; ";	          }
		if ( $self->{_hidden_fields}{timePerInstr8051}      eq False ) {
			print $file "Average Time per Instruction; ";	        }
		if ( $self->{_hidden_fields}{clockCyclePerInstrClk} eq False ) {
			print $file "Average Clock Cycle per Instruction; ";	}
		if ( $self->{_hidden_fields}{clockCyclePerInstrTpi} eq False ) {
			print $file "Average Clock Cycle per Instruction; ";	}
		print "\n";

		$self->printReportTableBreakLine($file);
}

# For each incite (set of inputs for a single run), this function
# prints the relative table row.
# INPUT  :
#		$cInstrExec            => number of 8051 instruction executed,
#		$execTime8051          => time spent for 8051 execution,
#		$clockCycle8051        => number of 8051 clock cycle required,
#		$timePerInstr8051      => average time spent on a single instruction,
#		$clockCyclePerInstrTpi => average clock cycle required for
#                             a single instruction, based on avgTpi,
#		$clockCyclePerInstrClk => average number of clock cycle required for
#                             single instruction, based on clkCycles8051.
# OUTPUT :
#		NONE
sub printReportTableEntry {

	my ( 	$self,
	      $file,
				$incite,
				$cInstrExec,
				$assInstrExec,
				$execTime8051,
				$clockCycleAss,
				$clockCycle8051,
				$timePerInstr8051,
				$clockCyclePerInstrClk,
				$clockCyclePerInstrTpi
	) = @_;

	print $file " $incite;";
	if ( $self->{_hidden_fields}{cInstrExec}            eq False ) {
		print $file " $cInstrExec;";	          }
	if ( $self->{_hidden_fields}{assInstrExec}          eq False ) {
		print $file " $assInstrExec;";          }
	if ( $self->{_hidden_fields}{execTime8051}          eq False ) {
		print $file " $execTime8051;";          }
	if ( $self->{_hidden_fields}{clockCycleAss}         eq False ) {
		print $file " $clockCycleAss;";         }
	if ( $self->{_hidden_fields}{clockCycle8051}        eq False ) {
		print $file " $clockCycle8051;";        }
	if ( $self->{_hidden_fields}{timePerInstr8051}      eq False ) {
		print $file " $timePerInstr8051;";      }
	if ( $self->{_hidden_fields}{clockCyclePerInstrClk} eq False ) {
		print $file " $clockCyclePerInstrClk;"; }
	if ( $self->{_hidden_fields}{clockCyclePerInstrTpi} eq False ) {
		print $file " $clockCyclePerInstrTpi;"; }
	print $file "\n";

}

# This function prints the footer of result table
# INPUT  :
#		NONE
# OUTPUT :
#		NONE
sub printReportTableFooter {
	my ( $self, $file ) = @_;
	$self->printReportTableBreakLine($file);
	$self->printReportTableBreakLine($file);
}

# This function prints the dotted breakline in result table
# INPUT  :
#		NONE
# OUTPUT :
#		NONE
sub printReportTableBreakLine {
	my ( $self, $file ) = @_;

	print $file ";";
	if ( $self->{_hidden_fields}{cInstrExec}            eq False ) {
		print $file ";"; }
	if ( $self->{_hidden_fields}{assInstrExec}          eq False ) {
		print $file ";"; }
	if ( $self->{_hidden_fields}{execTime8051}          eq False ) {
		print $file ";"; }
	if ( $self->{_hidden_fields}{clockCycleAss}         eq False ) {
		print $file ";"; }
	if ( $self->{_hidden_fields}{clockCycle8051}        eq False ) {
		print $file ";"; }
	if ( $self->{_hidden_fields}{timePerInstr8051}      eq False ) {
		print $file ";"; }
	if ( $self->{_hidden_fields}{clockCyclePerInstrClk} eq False ) {
		print $file ";"; }
	if ( $self->{_hidden_fields}{clockCyclePerInstrTpi} eq False ) {
		print $file ";"; }
	print $file " \n";
}

sub printReportSummary{

	my ( $self,
	     $file,
  	   $minimum,
  	   $maximum,
  	   $mean,
  	   $variance,
  	   $deviation,
  	   $version
	) = @_;

	print $file "The CCPI min; ";
	print $file "$minimum; ";
	print $file "\n";
	print $file "The CCPI max; ";
	print $file "$maximum; ";
	print $file "\n";
	print $file "The CCPI mean; ";
	print $file "$mean; ";
	print $file "\n";
	print $file "The CCPI variance; ";
	print $file "$variance; ";
	print $file "\n";
	print $file "The CCPI standard deviation; ";
	print $file "$deviation; ";
	print $file "\n";
	print $file "Version of mipsc program; ";
	print $file "$version; ";
	print $file "\n";

}

# This function normalize a string.
# It format the string in order to size it of provided $length.
# INPUT  :
#		$string => string to format
#   $length => number of character the string must size
# OUTPUT :
#		$string => format string
sub sizeString {

  my ( $self ) = @_;

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

1;
