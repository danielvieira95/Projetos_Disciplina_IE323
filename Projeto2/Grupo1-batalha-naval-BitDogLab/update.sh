#!/bin/bash

if [ $# -ne 1 ]; then
	>&2 echo "Invalid number of arguments"
fi

if [ $1 == 0 ] || [ $1 == 2 ]; then
	ampy -p /dev/ttyACM0 rm main.py 2>/dev/null ; \
		ampy -p /dev/ttyACM0 put main.py && \
		echo "main.py updated successfully"
fi

if [ $1 == 1 ] || [ $1 == 2 ]; then
	ampy -p /dev/ttyACM0 rm /lib/BitDogLib 2>/dev/null ; \
		ampy -p /dev/ttyACM0 put BitDogLib /lib/BitDogLib && \
		echo "BitDogLib updated successfully"
fi
