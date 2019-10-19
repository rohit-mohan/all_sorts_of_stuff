#!/usr/bin/bash

make -s -f makeserv clean
make -s -f makecli clean
make -s -f makeserv
make -s -f makecli
