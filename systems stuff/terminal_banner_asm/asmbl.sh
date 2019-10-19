#!/usr/bin/bash

if [ $# -lt 1 ]
	then echo -e "Mention the .asm file to be assembled and run!"
else
	make -f ~/code/asm/makefile FILE=$1
fi

	
