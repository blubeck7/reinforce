#include <stdio.h> 
#include <string.h> 
#include "../tscp/defs.h"
#include "../tscp/data.h"
#include "../tscp/protos.h"
#include "../inc/chess.h"


/* prototypes */
int test_hash(void);
int test_moves(void);


int main(int argc, char *argv[])
{
	Chess *game;
	//Player *white, *black;
	//int n;

	game = create_game();
	//display_info(game);
	//display_board(game);
	//white = create_player("User", cWHITE, NULL);
	//black = create_player("TSCP", cBLACK, NULL); 
	//display_player(white);
	//display_player(black);

	//list_moves(game, NULL, &n);
	if (argc > 1 && strcmp(argv[1], "-test") == 0) {
		printf("Running tests...\n");	
		test_hash();
		//test_moves();
	}

	destroy_game(game);

	return 0;
}


int test_hash(void)
{
	Chess *game;
	game = create_game();
	init_hash();

	printf("TSCP hash_piece: %d\n", hash_piece[0][0][0]);
	printf("Chess hash_piece: %d\n", game->hash_piece[0][0][0]);

	return 0;

int test_moves(void)
{
	int i;
	move move;

	init_hash();
	init_board();
	gen();
	printf("Ply is %d\n", ply);
	printf("En passant is %d\n", ep);
	printf("First move is %d to %d\n", first_move[ply], first_move[ply + 1]);

	for (i = first_move[ply]; i < first_move[ply + 1]; i++) {
		move = gen_dat[i].m;
		printf("%s\n", move_str(move.b));
	}

	return 0;
}

