#!/usr/bin/perl

# This package/class provides the functionalities to print reults
# produced by mipsc process.
package ReportTxt;

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

		$self->printReportTableBreakLine($file);

		print $file "*|";
		print $file " Incite     |";
		if ( $self->{_hidden_fields}{cInstrExec}            eq False ) {
			print $file " Executed    |";	        }
		if ( $self->{_hidden_fields}{assInstrExec}          eq False ) {
			print $file " Executed    |";	        }
		if ( $self->{_hidden_fields}{execTime8051}          eq False ) {
			print $file " Execution |";	          }
		if ( $self->{_hidden_fields}{clockCycleAss}         eq False ) {
			print $file " Clock Cycle  |";	      }
		if ( $self->{_hidden_fields}{clockCycle8051}        eq False ) {
			print $file " Clock Cycle  |";	      }
		if ( $self->{_hidden_fields}{timePerInstr8051}      eq False ) {
			print $file " Average Time per    |";	}
		if ( $self->{_hidden_fields}{clockCyclePerInstrClk} eq False ) {
			print $file " Average Clock Cycle |";	}
		if ( $self->{_hidden_fields}{clockCyclePerInstrTpi} eq False ) {
			print $file " Average Clock Cycle |";	}
		print $file "* \n";

		print $file "*|";
		print $file "            |";
		if ( $self->{_hidden_fields}{cInstrExec}            eq False ) {
			print $file " C Instr     |";         }
		if ( $self->{_hidden_fields}{assInstrExec}          eq False ) {
			print $file " Ass Instr   |";	        }
		if ( $self->{_hidden_fields}{execTime8051}          eq False ) {
			print $file " Time      |";           }
		if ( $self->{_hidden_fields}{clockCycleAss}         eq False ) {
			print $file " Expected Ass |";        }
		if ( $self->{_hidden_fields}{clockCycle8051}        eq False ) {
			print $file " Effect. 8051 |";        }
		if ( $self->{_hidden_fields}{timePerInstr8051}      eq False ) {
			print $file " Instruction         |"; }
		if ( $self->{_hidden_fields}{clockCyclePerInstrClk} eq False ) {
			print $file " per Instruction     |"; }
		if ( $self->{_hidden_fields}{clockCyclePerInstrTpi} eq False ) {
			print $file " per Instruction     |";	}
		print $file "* \n";

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

  $inciteStr                = sizeString($incite,                10); # 10 char
	$cInstrExecStr            = sizeString($cInstrExec,            11); # 11 char
	$assInstrExecStr          = sizeString($assInstrExec,          11); # 11 char
	$execTime8051Str          = sizeString($execTime8051,           9); #  9 char
	$clockCycle8051Str        = sizeString($clockCycle8051,        12); # 12 char
	$clockCycleAssStr         = sizeString($clockCycleAss,         12); # 12 char

	$timePerInstr8051Str      = sizeString($timePerInstr8051,      19); # 19 char
	$clockCyclePerInstrClkStr = sizeString($clockCyclePerInstrClk, 19); # 19 char
	$clockCyclePerInstrTpiStr = sizeString($clockCyclePerInstrTpi, 19); # 19 char

	$self->printReportTableBreakLine($file);

	print $file "*|";
	print $file " $inciteStr |";
	if ( $self->{_hidden_fields}{cInstrExec}            eq False ) {
		print $file " $cInstrExecStr |";	    }
	if ( $self->{_hidden_fields}{assInstrExec}          eq False ) {
		print $file " $assInstrExecStr |";	    }
	if ( $self->{_hidden_fields}{execTime8051}          eq False ) {
		print $file " $execTime8051Str |";   }
	if ( $self->{_hidden_fields}{clockCycleAss}         eq False ) {
		print $file " $clockCycleAssStr |"; }
	if ( $self->{_hidden_fields}{clockCycle8051}        eq False ) {
		print $file " $clockCycle8051Str |"; }
	if ( $self->{_hidden_fields}{timePerInstr8051}      eq False ) {
		print $file " $timePerInstr8051Str |";    }
	if ( $self->{_hidden_fields}{clockCyclePerInstrClk} eq False ) {
		print $file " $clockCyclePerInstrClkStr |";        }
	if ( $self->{_hidden_fields}{clockCyclePerInstrTpi} eq False ) {
		print $file " $clockCyclePerInstrTpiStr |";     }
	print $file "* \n";

}

# This function prints the footer of result table
# INPUT  :
#		NONE
# OUTPUT :
#		NONE
sub printReportTableFooter {
	my ( $self,$file ) = @_;
	$self->printReportTableBreakLine($file);
	$self->printReportTableBreakLine($file);
}

# This function prints the dotted breakline in result table
# INPUT  :
#		NONE
# OUTPUT :
#		NONE
sub printReportTableBreakLine {
	my ( $self,$file ) = @_;

	print $file "*|";
	print $file "************|";
	if ( $self->{_hidden_fields}{cInstrExec}            eq False ) {
		print $file "*************|";	        }
	if ( $self->{_hidden_fields}{assInstrExec}          eq False ) {
		print $file "*************|";	        }
	if ( $self->{_hidden_fields}{execTime8051}          eq False ) {
		print $file "***********|";           }
	if ( $self->{_hidden_fields}{clockCycleAss}         eq False ) {
		print $file "**************|";        }
	if ( $self->{_hidden_fields}{clockCycle8051}        eq False ) {
		print $file "**************|";        }
	if ( $self->{_hidden_fields}{timePerInstr8051}      eq False ) {
		print $file "*********************|"; }
	if ( $self->{_hidden_fields}{clockCyclePerInstrClk} eq False ) {
		print $file "*********************|"; }
	if ( $self->{_hidden_fields}{clockCyclePerInstrTpi} eq False ) {
		print $file "*********************|";  }
	print $file "* \n";
}

# This function prints the results' sumamry
# INPUT  :
#   $minimum   => minimum value for mipsc measure,
#   $maximum   => maximum value for mipsc measure,
#   $mean      => average value for mipsc measure,
#   $variance  => variance value for mipsc measure,
#   $deviation => standard deviation value for mipsc measure,
#   $version   => mipsc framework version
# OUTPUT :
#		NONE
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

	print $file "\n";
	print $file "*************************************";
	print $file "\n\n";
	print $file "The CCPI min is: $minimum";
	print $file "\n";
	print $file "The CCPI max is: $maximum";
	print $file "\n";
	print $file "The CCPI mean is: $mean";
	print $file "\n";
	print $file "The CCPI variance is: $variance";
	print $file "\n";
	print $file "The CCPI standard deviation is: $deviation";
	print $file "\n\n";
	print $file "*************************************";
	print $file "\n";
	print $file "\n";
	print $file "Version of mipsc program: $version";
	print $file "\n";
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
