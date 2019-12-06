SCRIPTPATH=$(dirname $(readlink -f "$0"))

if [ "$1" = "-i" ]; then
	./dep/installer_temp.sh
fi

python3 $SCRIPTPATH/src/__init__.py
