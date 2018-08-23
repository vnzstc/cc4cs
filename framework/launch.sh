SCRIPTPATH=$(dirname `which $0`)

if [ "$1" = "-i" ]; then
	./dep/installer_temp.sh
fi

python3 $SCRIPTPATH/src/__init__.py
