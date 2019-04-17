#include <stdio.h> 
#include "../tscp/defs.h"
#include "../tscp/data.h"
#include "../tscp/protos.h"
#include "../inc/chess.h"


/* prototypes */
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
	test_moves();

	destroy_game(game);

	return 0;
}


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

