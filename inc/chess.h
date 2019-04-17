/*
 * This header file contains the structure definitions, typedefs and functions
 * that are used to implement a chess program. It is the sole header file that
 * needs to be included for other functions to utilize the chess functionality.
 * Tom Kerrigan's simple chess program (www.tckerrigan.com) is used to help
 * implement the chess program. 
 */


#ifndef CHESS_H
#define CHESS_H


#define MAX_MOVES 550
#define MAX_MOVES_TURN 320


typedef struct piece_t Piece;
typedef struct move_t Move;
typedef struct board_t Board;
typedef struct chess_t Chess;
typedef struct player_t Player;
typedef int Move_func(Chess *game, char *move);


/* Chess functions */
//int reset_game(void);
Chess *create_game(void);
int *destroy_game(Chess *game);
int display_board(Chess *game);
int display_info(Chess *game);
int display_moves(Chess *game);
Move *list_moves(Chess *game, Board *board, int *n);
int run_game(Chess *game);
/*
int reset(Chess *game);
*/


/* Player functions */
Player *create_player(char *name, int color,
					  int (*get_move) (Chess *game, char *move));
int *destroy_player(Player *player);
int display_player(Player *player);
int user_move(Chess *game, char *move);


#endif
