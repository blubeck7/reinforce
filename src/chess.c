#include <stdio.h>
#include <stdlib.h>
#include "../inc/chess.h"


struct agent_t {
};

struct agent_t agent;
struct agent_t comp;


struct board_t {
};


struct chess_t {
	struct tscp_t {
		int computer_side;
		char s[256];
		int m;
} game;


struct episode_t {
};


struct move_t {
};


extern Episode episode; //TODO: Keep public or not


int main(int argc, char *argv[])
{
	return 0;
}


/* Chess class methods */
int init_game(void)
{
	/* First initialize the data used by tcsp in order to play a game.
	 * Then initialize the data needed for doing reinforcement learning
	 * on top of playing a game. */
	init_tscp();
	init_reinforce();

	return 0;
}


int reset_game(void)
{
	/* First initialize the data used by tcsp in order to play a game.
	 * Then initialize the data needed for doing reinforcement learning
	 * on top of playing a game. */
	reset_tscp();
	reset_reinforce();

	return 0;
}

static int init_tscp(void)
{
	/* Initializes the hash values for the pieces, side and en passant */
	init_hash(); 
	init_board();
	open_book();
	/* Generates pseudo-legal moves for the current position. */
	gen();

	computer_side = EMPTY;
	/* the engine will search for max_time milliseconds or until it finishes
   	searching max_depth ply. */
	max_time = 1 << 25;
	max_depth = 4;

	return 0;
}


static int reset_tscp(void)
{
	computer_side = EMPTY;
	init_board();
	gen();

	return 0;
}

