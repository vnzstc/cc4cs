
if [ "$1" = "-i" ]; then
	./dep/installer.sh
fi

python3 ./src/__init__.py
