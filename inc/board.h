#ifndef BOARD_H
#define BOARD_H


#include "../inc/move.h"


typedef struct board Board;


Board *create_board(void);
int destroy_board(Board *board);
int set_fen(Board *board, char *fen);
char *get_fen(Board *board);
int push_move(Board *board, Move *move);
int pop_move(Board *board, Move *move);

#endif
