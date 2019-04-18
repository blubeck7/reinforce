#include <stdio.h> 
#include <string.h> 
#include "../tscp/defs.h"
#include "../tscp/data.h"
#include "../tscp/protos.h"
#include "../src/chess.c"


/* prototypes */
int test_init_hash(void);
int test_init_board(void);
int test_moves(void);


int main(int argc, char *argv[])
{
	printf("Running tests...\n");	
	test_init_hash();
	test_init_board();
	test_moves();

	return 0;
}


int test_init_hash(void)
{
	int i, j, k, cnt = 0;
	Chess *game;

	game = create_game();
	init_hash();

	for (i = 0; i < 2; i++)
		for (j = 0; j < 6; j++)
			for (k = 0; k < 64; k++)
				cnt += (game->hash_piece[i][j][k] - hash_piece[i][j][k]);
	cnt += (game->hash_side - hash_side);
	for (i = 0; i < 64; ++i)
		cnt += (game->hash_ep[i] - hash_ep[i]);

	if (cnt == 0)
		printf("init hash succeeded!\n");
	else
		printf("init hash failed!\n");

	destroy_game(game);

	return 0;
}


int test_init_board(void)
{
	int i, cnt = 0;
	Chess *game;

	game = create_game();
	init_hash();
	init_board();

	for (i = 0; i < 64; i++) {
		cnt += (game->color[i] - color[i]);
		cnt += (game->piece[i] - piece[i]);
	}
	cnt += (game->side - side);
	cnt += (game->xside - xside);
	cnt += (game->castle - castle);
	cnt += (game->ep - ep);
	cnt += (game->fifty - fifty);
	cnt += (game->ply - ply);
	cnt += (game->hply - hply);
	cnt += (game->hash - hash);
	cnt += (game->first_move[0] - first_move[0]);

	if (cnt == 0)
		printf("init board succeeded!\n");
	else
		printf("init board failed!\n");

	destroy_game(game);

	return 0;
}


int test_moves(void)
{
	Chess *game;
	Move *moves;
	int i, n;

	game = create_game();
	init_hash();
	init_board();

	moves = list_moves(game, &n);
	moves = list_moves(game, &n);
	moves = list_moves(game, &n);
	printf("There are %d pseudo-legal moves.\n", n);
	for (i = 0; i < n; i++)
		display_move(moves + i);
	//display_moves(game);
	destroy_game(game);

	/*
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
	*/

	return 0;
}

