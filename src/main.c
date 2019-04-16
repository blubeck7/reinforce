#include <stdio.h> 
#include "../inc/chess.h"


int main(int argc, char *argv[])
{
	Chess *game;
	Player *white, *black;
	int n;

	game = create_game();
	white = create_player("User", WHITE, NULL);
	black = create_player("TSCP", BLACK, NULL); 
	display_player(white);
	display_player(black);

	list_moves(game, NULL, &n);

	destroy_game(game);

	return 0;
}



