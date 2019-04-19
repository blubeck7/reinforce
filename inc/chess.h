/*
 * This header file contains the structure definitions, typedefs and functions
 * that are used to implement a chess program. It is the sole header file that
 * needs to be included for other functions to utilize the chess functionality.
 * Tom Kerrigan's simple chess program (www.tckerrigan.com) is used to help
 * implement the chess program. 
 */


#ifndef CHESS_H
#define CHESS_H


typedef struct move_t Move;
typedef struct board_t Board;
typedef struct chess_t Chess;
typedef struct history_t History;
typedef struct player_t Player;
typedef Move *Move_func(Chess *game);


/* Chess functions */
Chess *create_game(void); //
void destroy_game(Chess *game); //
void set_player(Chess *game, Player *player, int color); //
void display_board(Chess *game); //
void display_info(Chess *game); //
void display_history(Chess *game);
void run_game(Chess *game);
void reset_game(Chess *game);
int is_over(Chess *game);
History *get_history(Chess *game);

/* Move functions */
Move *list_moves(Chess *game, int *num_moves); // These are pseudo-legal moves
Move *list_movesl(Chess *game, int *num_moves); // These are legal moves
int make_move(Chess *game, Move *move);
int undo_move(Chess *game);
void display_move(Move *move); //


/* Player functions */
Player *create_player(char *name, int color, Move_func *move_func);
int *destroy_player(Player *player);
int display_player(Player *player);

#endif
