#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../tscp/defs.h"
#include "../tscp/data.h"
#include "../tscp/protos.h"
#include "../inc/chess.h"


struct move_t {
	move tscp_move; //see defs.h in tscp/
	char move_str[6];
};


struct board_t {
	int color[64];
	int piece[64];
	int castle;
	int ep;
};


struct chess_t {
	enum colors whose_move;
	Player *white;
	Player *black;
	char white_move[MAX_MOVES][6]; //a move is human-readable e2e4, etc.
	Board white_board[MAX_MOVES];
	char black_move[MAX_MOVES][6];
	Board black_board[MAX_MOVES];
	Move move[MAX_MOVES_TURN];
	int turn; 
	int result;
};


struct player_t { 
	char *name;  
	enum colors color;
	Move_func *get_move;
};


/* Chess functions */
Chess *create_game(void)
{
	Chess *game;
	int i, j;

	game = (Chess *) malloc(sizeof(Chess));
	game->whose_move = WHITE;
	game->white = game->black = NULL;
	game->turn = 1;
	game->result = 0;
	for (i = 0; i < MAX_MOVES; i++)
		for (j = 0; j < 5; j++) {
			game->white_move[i][j] = '\0';
			game->black_move[i][j] = '\0';
		}

	init_hash(); //tscp - initializes the random numbers used by set_hash.
	init_board(); //tscp - initializes the global variables for the board.
	open_book(); // tscp - a text file of opening moves.

	return game;
}


int *destroy_game(Chess *game)
{
	free(game);

	return 0;
}


int display_board(Chess *game)
{
	/* TODO: Note that tscp uses global variables. To make the code
	 * object-orienteed, one could place all of the global variables inside the
	 * chess_t structure and then replace the names of the global variables
	 * with the names of the structure elements.
	 */ 

	print_board();

	return 0;
}


int display_info(Chess *game)
{
	printf("Turn: %d\n", game->turn);
	if (game->whose_move == WHITE) {
		printf("White's turn to move.\n");
		printf("The previous move was %s.\n", game->black_move[game->turn]);
	} else {
		printf("Black's turn to move\n.");
		printf("The previous move was %s.\n", game->white_move[game->turn]);
	}

	return 0;
}


int display_moves(Chess *game)
{
	int i;

	for (i = 1; i < game->turn; i++)
		printf("%d. %s %s\n", i, game->white_move[i], game->black_move[i]);

	return 0;
}


Move *list_moves(Chess *game, Board *board, int *n)
{
	int n_moves;

	/* gen is a tscp function. It generates pseudo-legal moves and saves them
	 * to the global array gen_dat and modifies first_move[ply+1] to count the
	 * number of moves and track the moves indices in gen_dat.
	 */
	gen(); 
	n_moves = first_move[ply + 1] - first_move[ply];
	printf("n moves %d.\n", n_moves);
	//g = &gen_dat[first_move[ply + 1]++];
	// copy from tscp global variable ... to struct chess_t array of moves.
	return NULL;
}


int run_game(Chess *game)
{
	return 0;
}



/* Player functions */
Player *create_player(char *name, enum colors color, Move_func *get_move)

{
	Player *player;

	player = (Player *) malloc(sizeof(Player));
	player->name = name;
	player->color = color;
	player->get_move = get_move;

	return player;
}


int *destroy_player(Player *player)
{
	free(player);

	return 0;
}


int display_player(Player *player)
{
	if (player->color == WHITE)
		printf("%s is white.\n", player->name);
	else
		printf("%s is black.\n", player->name);

	return 0;
}

/*
int user_move(Chess *game, char *move)
{

	moves = list_moves(Chess *game,   
*/
/*
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
