/* This header file contains the structure definitions, typedefs and functions
 * that are used to implement a chess program. It is the sole header file that
 * needs to be included for other functions to utilize the chess functionality.
 * Tom Kerrigan's simple chess program (www.tckerrigan.com) is used to help
 * implement the chess program. Since this chess program is intended to be used
 * with reinforcement learning algorithms, global variables and structures are
 * used instead of opaque pointers to increase speed. Opaque pointers to
 * structures create more reusable objects, but decrease speed because an
 * additional memory read is introduced to get the pointer's value.
 */


#ifndef CHESS_H
#define CHESS_H


#include "../inc/defs.h"
#include "../inc/data.h"
#include "../inc/protos.h"


typedef struct agent_t Agent; //TODO: struct members
typedef struct board_t Board; //TODO: struct members
typedef struct chess_t Chess;
typedef struct episode_t Episode; //TODO: struct members
extern Episode episode; //TODO: Keep public or not


/* Agent class methods */
/*
char *get_name(Agent *agent);
int get_key(Agent *agent):
int set_key(Agent *agent, key):
Policy *get_policy(Agent *agent):
int set_policy(Agent *agent, Policy *policy);
*/
//int list_moves(Agent *agent, Chess *game, state, move moves[]);
//int select(Agent *agent, Chess *game, state, char *move);


/* Chess class methods */
int init_game(void);
int reset_game(void);
int run_game(Agent *white, Agent *black);

/*
Chess *create(void);
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



#endif
