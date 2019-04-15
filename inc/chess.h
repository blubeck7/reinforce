/*
 * This header file contains the structure definitions, typedefs and functions
 * that are used to implement a chess program. It is the sole header file that
 * needs to be included for other functions to utilize the chess functionality.
 * Tom Kerrigan's simple chess program (www.tckerrigan.com) is used to help
 * implement the chess program. 
 */


#ifndef CHESS_H
#define CHESS_H


#include "../tscp/defs.h"
#include "../tscp/data.h"
#include "../tscp/protos.h"


enum colors {WHITE, BLACK};


typedef struct chess_t Chess;
typedef struct move_t Move;
typedef struct player_t Player;


/* Chess functions */
//int init_game(void);
//int reset_game(void);
Chess *create(void);
int run(Chess *game);
/*
int destroy(Chess *game);
Agent *get_agent(Chess * game);
int set_agent(Chess * game, Agent *agent, int key);
Agent *get_comp(Chess * game);
int set_comp(Chess * game, Agent *comp, int key);
int run(Chess *game);
int reset(Chess *game);
Move *list_moves(Chess *game, int key, Board *board);
Episode *get_episode(Chess *game);
*/


/* Player functions */
Player *create_player(char *name, enum colors color,
					  int (*get_move) (Chess *game, Move *move));
int *destroy_player(Player *player);
int display_player(Player *player);


#endif
