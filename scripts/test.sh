#!/usr/bin/env bash

# usage build.sh <top level directory>
TOP="$1"
BIN="$TOP/bin"
TEST="$TOP/test"
TSCP="$TOP/tscp"
cc -Wall -std=c99 -c -o $TSCP/board.o $TSCP/board.c
cc -Wall -std=c99 -c -o $TSCP/book.o $TSCP/book.c
cc -Wall -std=c99 -c -o $TSCP/data.o $TSCP/data.c
cc -Wall -std=c99 -c -o $TSCP/eval.o $TSCP/eval.c
cc -Wall -std=c99 -c -o $TSCP/main.o $TSCP/main.c
cc -Wall -std=c99 -c -o $TSCP/search.o $TSCP/search.c
cc -Wall -std=c99 -c -o $TEST/test_chess.o $TEST/test_chess.c
cc -Wall -std=c99 -o $BIN/test_chess \
	$TEST/test_chess.c \
	$TSCP/board.o \
	$TSCP/book.o \
	$TSCP/data.o \
	$TSCP/eval.o \
	$TSCP/main.o \
	$TSCP/search.o

rm $TSCP/*.o
rm $TEST/*.o

