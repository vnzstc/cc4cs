OPTS_AVRGCC="
	--target=avr
	--enable-languages=c,c++
	--disable-nls
	--disable-libssp
	--with-dwarf2
"

function check_installation()
{
	if ! loc="$(type -p "$1")" || [[ -z $loc ]]; then 
		case $1 in
			"gcc")
				echo "Installation procedure of gcc"
				download_and_extract_it https://ftp.gnu.org/gnu/gcc/gcc-8.2.0/gcc-8.2.0.tar.gz
				;;
			"avr-gcc")
				echo "Installation procedure of avr-gcc"
				check_installation "gcc"
				install_avrgcc
				;;
			"simulavr")
				echo "Installation procedure of SIMULAVR"
				download_and_extract_it http://download.savannah.nongnu.org/releases/simulavr/simulavr-1.0.0-binary-linux32.tar.gz
				simulavr_installation
				;;
			"sparc-gcc")
				echo "Installation procedure for BCC"
				download_and_extract_it https://www.gaisler.com/anonftp/bcc2/bin/bcc-2.0.1-gcc-linux64.tar.bz2
				install_bcc 
				;;
			"tsim-leon3")
				;;
		esac
	else
		echo "$1 already installed" 
	fi
}

function download_and_extract_it()
{
	filename=$(basename $1)
	
	echo $filename

	wget $1
	truncated_filename=$(file $filename | cut -d ' ' -f 2 )
	
	case $truncated_filename in 
		"bzip2" )
			tar xvjf $filename > /dev/null
			;;
		"gzip" )
			tar xzvf $filename > /dev/null
			;;
	esac	
}

function install_simulavr()
{
	# add "simulavr" to the PATH environment variable
	echo 'export PATH=$PATH:$PWD/simulavr/bin' >> $HOME/.bashrc 
}

function install_bcc()
{
	bcc_dir_name=$(find `pwd` -type d -iname 'bcc-*')
	export_cmd_string='export PATH=$PATH:'
	global_variable_string=$export_cmd_string$bcc_dir_name/bin

	# add "bcc" to the PATH environment variable
	echo $global_variable_string >> $HOME/.bashrc 
}

function install_avrgcc()
{
	cd gcc-*
	./contrib/download_prerequisites
	mkdir obj-avr 
	cd obj-avr
	../configure $OPTS_AVRGCC
	# make 
	# make install
} 