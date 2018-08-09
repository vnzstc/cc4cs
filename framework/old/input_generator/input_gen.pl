#! /usr/bin/ perl 
use warnings;
use Algorithm::Loops qw/ NestedLoops /;

my %non_array_hash;
my %array_hash;

# Open the file to parse. 
# Searches for the string "void prototype(parameters);"
# Retrieves parameters through regular expression.
# Returns a list that contains the parameters of the functions.

sub get_parameters
{
	open(DATA, "<quicksort.c");

	# For each line in the file, the presence of the keyword 
	# "prototype" is checked.

	while(<DATA>)
	{
		# This statement checks if the prototype is written in the right format
		if($_ =~ m/(void prototype\(([a-z0-9_]+\s[a-z]+(\[[0-9a-z]+\])*,*\s*)*)\);/)
		{
			$str = $_;
			# Substitution of the "void prototype" part with empty string.
			$str =~ s/void prototype\(//;
			# Substitution of the ");" part with empty string.
			$str =~ s/\)\;\n//;

			return split /,/, $str;
		}
	}

	die "Error: can't find prototype";
}


# Type checking on the user input
# Returns a list with Min, Max and Values (in the array case)

sub match_input_string
{
	# Retrieves data from stdin
	my $input = <STDIN>;

	# Retrieves compiled regex as a parameter
	my @local_par = @_;

	chomp $input;

	# Discards letters and symbols and stores numbers in a list with the following positioning:
	# P0: Min, P1: Max, P2: Values (Array Case)
	my @list = ($input =~ m/[0-9]+/g);
	
	# This "if" needs to trigger an error if the input is wrong. 
	# The left hand side of the or checks if the input is in the correct format while 
	# the right hand side if the Min value if greater than the Max

	if(($input !~ @local_par) or ($list[0] > $list[1]))
	{
		die 'Error: bad input string';
	}
		
	return @list;
}

# For each parameters asks user to insert a range [Min, Max] and, if needed, number of values.
# The script uses two hashes to store data. The data structures are filled using the name of the variable
# as the key and the user data as the values.
# Ex. { int a    => [Min, Max]; Values
#		int8_t b => [Min, Max]; Values
#	   }
# In "array_hash" are stored the informations for the array variables while in "non_array_hash" the variables of the
# other type.

sub ask_for_data
{
	foreach $ele (@_)
	{
		# Deletes white spaces
		$ele =~ s/^\s+//;

		# Check if the variable is an array 
		if(index($ele, '[') != -1)
		{
			print "Insert [Min, Max] for $ele: ";
			@{$array_hash{$ele}} = match_input_string(qr/^\[(\d+,\d+)\]$/);
		} 
		else
		{
			print "Insert [Min, Max];Values for $ele: ";
			@{$non_array_hash{$ele}} = match_input_string(qr/^\[(\d+,\d+)\];[1-9][0-9]*$/);
		}
	}
}


my $file_cont = 0;

sub create_file
{
	my %array_sizes; 

	# print "Current comb: ", @_, "\n";
	open(my $fh, ">values$file_cont.h")
		or die "Could not open file";

	print $fh "#ifndef VALUES\n#define VALUES\n";

	my $cont = 0;	
	foreach my $var (keys %non_array_hash)
	{
		# Deletes type
		$cut_type = ($var =~ s/[0-9a-zA-Z_]+ / /r);
		$cut_type =~ s/^\s+//;

		if(is_size($cut_type))
		{
			print $fh "\tenum{ $cut_type = $_[$cont] };\n";	
			$array_sizes{$cut_type} = $_[$cont];

		}else
		{
			print $fh "\t$var = $_[$cont];\n";
		}

		$cont += 1;
	}

	$file_cont += 1;
	write_random_arrays($fh, \%array_sizes);

	print $fh "#endif";
}


sub is_size
{
	my ($var) = @_;
	foreach $skey (keys %array_hash)
	{
		if($skey =~ m/$var/)
		{
			return 1;
		}
	}

	return 0;
}


sub gen_int
{	
	my $min = $_[0];
	my $max = $_[1];

	return int(rand($max)) + $min;
}

# For each non-array variable generates a list of Values random numbers between
# Min and Max. In order to generate the values, is iterated the hash that contains 
# non-array variable.

sub generate_values
{
	for my $skey (keys %non_array_hash)
	{
			# List in which are store random generated values
			my @values;

			for(my $i = 0; $i < $non_array_hash{$skey}[2]; $i++)
			{
				# Check if the current variable is an int or not. 
				if($skey =~ m/int/) 
				{
					# Generates a random int value and stores it in the @values list
					push @values, gen_int($non_array_hash{$skey}[0], $non_array_hash{$skey}[1]);
				}
				else
				{
					# Round the float random generated value
					my $cut = rand($non_array_hash{$skey}[1] + 0) + $non_array_hash{$skey}[0];
					# Stores it in the @values list
					push @values, int(($cut * 1000.0) + 0.5) / 1000.0;	
				}
			}
		@{$non_array_hash{$skey}} = @values;
	}
}


# Generates a monodimensional array and writes it on the file.
sub write_monodimensional
{
	my ($dim1, $min, $max, $filehead) = @_;
	my $gen_int = gen_int($min, $max);

	print $filehead " {";

	if($dim1 > 1)
	{
		for($i = 0; $i < $dim1 - 1; $i++)
		{
			$gen_int = gen_int($min, $max);
			print $filehead "$gen_int, ";
		}

		print $filehead "$gen_int";
	}

	print $filehead "};\n";
}

# Generates a multimensional array and writes it on the file.
sub write_multidimensional
{
	my ($dim1, $dim2, $min, $max, $filehead) = @_;
	my $gen_int;

	print $filehead " {";

	for(my $i = 0; $i < $dim1; $i++)
	{	
		print $filehead "{";

		for(my $y = 0; $y < $dim2 - 1; $y++)
		{
			$gen_int = gen_int($min, $max);
			print $filehead "$gen_int, ";
		}

		$gen_int = gen_int($min, $max);
		print $filehead "$gen_int}";

		if($i < ($dim1 - 1))
		{
			print $filehead ", ";
		}
	}

	print $filehead "};\n";
}

# This subroutine generates a random instance of each array that is in the hash.
sub write_random_arrays
{
	my ($filehead) = $_[0];

	# Hash with array var sizes
	my %array_sizes = %{$_[1]};

	foreach my $skey (keys %array_hash)
	{
		print $filehead "\t$skey =";

		if($skey =~ m/\[(.*?)\]\[(.*?)\]/)
		{
			my ($dim1, $dim2) = ($skey =~ m/\[(.*?)\]/g);

			$dim1 = $array_sizes{$dim1};
			$dim2 = $array_sizes{$dim2};

			write_multidimensional($dim1, $dim2, $array_hash{$skey}[0], $array_hash{$skey}[1], $filehead);
		}
		else
		{	
			my ($dim1) = ($skey =~ m/\[(.*?)\]/g);

			$dim1 = $array_sizes{$dim1};

			write_monodimensional($dim1, $array_hash{$skey}[0], $array_hash{$skey}[1], $filehead);
		}
	}
}

# Discovering parameters and ask for data
my @parameters = get_parameters();
ask_for_data(@parameters);

# Generation of non-array variable values 
generate_values();

# At this point, the hashes has been filled. In particular, the array_hash contains the list with values to combine. 
# Generates combinations with the lists in "array_hash"
my @hash_values = values %non_array_hash;
NestedLoops(\@hash_values, \&create_file);