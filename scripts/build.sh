#!/usr/bin/env bash

TOPDIR="$1"
BINDIR="$TOPDIR/bin"
SRCDIR="$TOPDIR/src"
#gcc -Wall -std=c99 -c ~/reinforce/src/board.c
#gcc -Wall -std=c99 -c ~/reinforce/src/book.c
#gcc -Wall -std=c99 -c ~/reinforce/src/book.c
#gcc -Wall -std=c99 -o bin/chess src/chess.c
gcc -Wall -std=c99 -o $BINDIR/chess $SRCDIR/chess.c

