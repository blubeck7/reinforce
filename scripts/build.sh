#!/usr/bin/env bash

# usage build.sh <top level directory>
TOP="$1"
BIN="$TOP/bin"
SRC="$TOP/src"
TSCP="$TOP/tscp"
cc -Wall -std=c99 -c -o $TSCP/board.o $TSCP/board.c
cc -Wall -std=c99 -c -o $TSCP/book.o $TSCP/book.c
cc -Wall -std=c99 -c -o $TSCP/data.o $TSCP/data.c
cc -Wall -std=c99 -c -o $TSCP/eval.o $TSCP/eval.c
cc -Wall -std=c99 -c -o $TSCP/main.o $TSCP/main.c
cc -Wall -std=c99 -c -o $TSCP/search.o $TSCP/search.c
cc -Wall -std=c99 -c -o $SRC/chess.o $SRC/chess.c
#gcc -Wall -std=c99 -c ~/reinforce/src/book.c
#gcc -Wall -std=c99 -c ~/reinforce/src/book.c
#gcc -Wall -std=c99 -o bin/chess src/chess.c
cc -Wall -std=c99 -o $BIN/chess \
	$SRC/main.c \
	$SRC/chess.o \
	$TSCP/board.o \
	$TSCP/book.o \
	$TSCP/data.o \
	$TSCP/eval.o \
	$TSCP/main.o \
	$TSCP/search.o

rm $TSCP/*.o

