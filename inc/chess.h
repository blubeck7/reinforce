#ifndef CHESS_H
#define CHESS_H


typedef struct agent_t Agent; //TODO: struct members
typedef struct board_t Board; //TODO: struct members
typedef struct chess_t Chess;
typedef struct episode_t Episode; //TODO: struct members
typedef struct move_t Move; //TODO: struct members
extern Episode episode; //TODO: Keep public or not


/* Chess class methods */
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


/* History class methods */

#endif
