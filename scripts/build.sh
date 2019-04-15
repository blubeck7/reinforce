#!/usr/bin/env bash

# usage build.sh <top level directory>
TOPDIR="$1"
BINDIR="$TOPDIR/bin"
SRCDIR="$TOPDIR/src"
TSCPDIR="$TOPDIR/tscp"
cc -Wall -std=c99 -c -o $TSCPDIR/board.o $TSCPDIR/board.c
cc -Wall -std=c99 -c -o $TSCPDIR/book.o $TSCPDIR/book.c
cc -Wall -std=c99 -c -o $TSCPDIR/data.o $TSCPDIR/data.c
cc -Wall -std=c99 -c -o $TSCPDIR/eval.o $TSCPDIR/eval.c
cc -Wall -std=c99 -c -o $TSCPDIR/main.o $TSCPDIR/main.c
cc -Wall -std=c99 -c -o $TSCPDIR/search.o $TSCPDIR/search.c
#gcc -Wall -std=c99 -c ~/reinforce/src/book.c
#gcc -Wall -std=c99 -c ~/reinforce/src/book.c
#gcc -Wall -std=c99 -o bin/chess src/chess.c
cc -Wall -std=c99 -o $BINDIR/chess \
	$SRCDIR/chess.c \
	$TSCPDIR/board.o \
	$TSCPDIR/book.o \
	$TSCPDIR/data.o \
	$TSCPDIR/eval.o \
	$TSCPDIR/main.o \
	$TSCPDIR/search.o

