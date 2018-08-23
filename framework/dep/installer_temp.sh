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
				download_and_extract_it https://ftp.gnu.org/gnu/gcc/gcc-8.2.0/gcc-8.2.0.tar.gz
				download_and_extract_it ftp://ftp.gnu.org/gnu/m4/m4-1.4.10.tar.gz
				exec_autoconf_cmds "m4-1.4.10" "." "--prefix=/usr/local/m4"
				install_gcc
				;;
			"simulavr")
				echo "Installation procedure of SIMULAVR"
				download_and_extract_it http://download.savannah.nongnu.org/releases/simulavr/simulavr-1.0.0-binary-linux32.tar.gz
				add_dir_to_bashrc 'usr' 'bin'
				;;
			"sparc-gaisler-elf-gcc")
				echo "Installation procedure for BCC"
				download_and_extract_it https://www.gaisler.com/anonftp/bcc2/bin/bcc-2.0.1-gcc-linux64.tar.bz2
				add_dir_to_bashrc 'bcc-*' 'bin' 
				;;
			"tsim-leon3")
				echo "Installation procedure for TSIM"
				download_and_extract_it https://www.gaisler.com/anonftp/tsim/tsim-eval-2.0.61.tar.gz
				add_dir_to_bashrc 'tsim-eval' 'tsim/linux-x64' 
				;;
		esac
	else
		echo "$1 already installed" 
	fi
}

function download_and_extract_it()
{
	filename=$(basename $1)
	wget $1 
	truncated_filename=$(file $filename | cut -d ' ' -f 2)

	case $truncated_filename in 
		"bzip2" )
			tar xvjf $filename > /dev/null
			;;
		"gzip" )
			tar xzvf $filename > /dev/null
			;;
	esac	
}

# $1 options 
function install_gcc()
{
	echo "#############################################"
	cd gcc-8.2.0
	./contrib/download_prerequisites
	exec_autoconf_cmds "gmp" $(pwd)"/gmp"
	exec_autoconf_cmds "mpfr" $(pwd)"/mpfr"
	exec_autoconf_cmds "mpc" $(pwd)"/mpc"
	mkdir obj 
	exec_autoconf_cmds "obj" $(pwd) $OPTS_AVRGCC
}

function exec_autoconf_cmds()
{
	echo $PWD
	cd $1
	$2/configure $3
	make > /dev/null
	sudo make install
	cd ..
}

# $1 dir-pattern $2 dir_name
function add_dir_to_bashrc()
{
	dir_name=$(find `pwd` -type d -iname "$1")
	export_cmd='export PATH=$PATH:'
	global_variable=$export_cmd$dir_name/$2

	# add dir to the PATH environment variable
	echo $global_variable >> $HOME/.bashrc 
}

cd dep
check_installation "avr-gcc"
# check_installation "simulavr"