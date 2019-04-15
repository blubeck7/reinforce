#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../inc/chess.h"


struct chess_t {
	enum colors whose_move;
	Player *white;
	Player *black;
};


struct player_t { 
	char *name;  
	enum colors color;
	int (*get_move) (Chess *game, Move *move);
};



int main(int argc, char *argv[])
{
	return 0;
}


/* Chess functions */
Chess *create(void)
{
	Chess *game;

	game = (Chess *) malloc(sizeof(Chess));
	init_hash(); //tscp - initializes the random numbers used by set_hash.
	init_board(); //tscp - initializes the global variables for the board.
	open_book(); // tscp - a text file of opening moves.

	return game;
}


int run(Chess *game)
{

	return 0;
}



/* Player functions */
Player *create_player(char *name, enum colors color,
					  int (*get_move) (Chess *game, Move *move))
{
	Player *player;

	player = (Player *) malloc(sizeof(Player));
	player->name = name;
	player->color = color;
	player->get_move = get_move;

	return player;
}


int *destroy_player(Player *player);
int display_player(Player *player);



/*
int init_game(void)
{
*/
	/* First initialize the data used by tcsp in order to play a game.
	 * Then initialize the data needed for doing reinforcement learning
	 * on top of playing a game. */
/*
	init_tscp();
	init_reinforce();

	return 0;
}


int reset_game(void)
{
*/
	/* First initialize the data used by tcsp in order to play a game.
	 * Then initialize the data needed for doing reinforcement learning
	 * on top of playing a game. */
/*
	reset_tscp();
	reset_reinforce();

	return 0;
}

static int init_tscp(void)
{
*/
	/* Initializes the hash values for the pieces, side and en passant */
	//init_hash(); 
	//init_board();
	//open_book();
	/* Generates pseudo-legal moves for the current position. */
	//gen();

	//computer_side = EMPTY;
	/* the engine will search for max_time milliseconds or until it finishes
   	searching max_depth ply. */
	//max_time = 1 << 25;
	//max_depth = 4;

	//return 0;
//}

/*
static int reset_tscp(void)
{
	computer_side = EMPTY;
	init_board();
	gen();

	return 0;
}
*/
