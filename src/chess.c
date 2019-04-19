// TODO: Profile code and measure the performance.
/* This file implements the chess functionality for two agents to play against
 * each other. Tom Kerrigan's simple chess program is used to implement the
 * functionality. Names in this files are sometimes prefixed c to avoid name
 * clashes with the names in the tscp source files. 
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../inc/chess.h"


#define MAX_MOVES 550
#define MAX_MOVES_TURN 320

#define CBOOL			int
#define CTRUE			1
#define CFALSE			0

#define CGEN_STACK		1120
#define CMAX_PLY		32
#define CHIST_STACK		400

#define CLIGHT			0
#define CDARK			1

#define CPAWN			0
#define CKNIGHT			1
#define CBISHOP			2
#define CROOK			3
#define CQUEEN			4
#define CKING			5

#define CEMPTY			6

/* useful squares */
#define CA1				56
#define CB1				57
#define CC1				58
#define CD1				59
#define CE1				60
#define CF1				61
#define CG1				62
#define CH1				63
#define CA8				0
#define CB8				1
#define CC8				2
#define CD8				3
#define CE8				4
#define CF8				5
#define CG8				6
#define CH8				7

#define CROW(x)			(x >> 3)
#define CCOL(x)			(x & 7)

/* Constants */
/* Now we have the mailbox array, so called because it looks like a
   mailbox, at least according to Bob Hyatt. This is useful when we
   need to figure out what pieces can go where. Let's say we have a
   rook on square a4 (32) and we want to know if it can move one
   square to the left. We subtract 1, and we get 31 (h5). The rook
   obviously can't move to h5, but we don't know that without doing
   a lot of annoying work. Sooooo, what we do is figure out a4's
   mailbox number, which is 61. Then we subtract 1 from 61 (60) and
   see what mailbox[60] is. In this case, it's -1, so it's out of
   bounds and we can forget it. You can see how mailbox[] is used
   in attack() in board.c. */

int CMAILBOX[120] = {
	 -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
	 -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
	 -1,  0,  1,  2,  3,  4,  5,  6,  7, -1,
	 -1,  8,  9, 10, 11, 12, 13, 14, 15, -1,
	 -1, 16, 17, 18, 19, 20, 21, 22, 23, -1,
	 -1, 24, 25, 26, 27, 28, 29, 30, 31, -1,
	 -1, 32, 33, 34, 35, 36, 37, 38, 39, -1,
	 -1, 40, 41, 42, 43, 44, 45, 46, 47, -1,
	 -1, 48, 49, 50, 51, 52, 53, 54, 55, -1,
	 -1, 56, 57, 58, 59, 60, 61, 62, 63, -1,
	 -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
	 -1, -1, -1, -1, -1, -1, -1, -1, -1, -1
};

int CMAILBOX64[64] = {
	21, 22, 23, 24, 25, 26, 27, 28,
	31, 32, 33, 34, 35, 36, 37, 38,
	41, 42, 43, 44, 45, 46, 47, 48,
	51, 52, 53, 54, 55, 56, 57, 58,
	61, 62, 63, 64, 65, 66, 67, 68,
	71, 72, 73, 74, 75, 76, 77, 78,
	81, 82, 83, 84, 85, 86, 87, 88,
	91, 92, 93, 94, 95, 96, 97, 98
};

/* slide, offsets, and offset are basically the vectors that
   pieces can move in. If slide for the piece is FALSE, it can
   only move one square in any one direction. offsets is the
   number of directions it can move in, and offset is an array
   of the actual directions. */

CBOOL CSLIDE[6] = {
	CFALSE, CFALSE, CTRUE, CTRUE, CTRUE, CFALSE
};

int COFFSETS[6] = {
	0, 8, 4, 4, 8, 8
};

int COFFSET[6][8] = {
	{ 0, 0, 0, 0, 0, 0, 0, 0 },
	{ -21, -19, -12, -8, 8, 12, 19, 21 },
	{ -11, -9, 9, 11, 0, 0, 0, 0 },
	{ -10, -1, 1, 10, 0, 0, 0, 0 },
	{ -11, -10, -9, -1, 1, 9, 10, 11 },
	{ -11, -10, -9, -1, 1, 9, 10, 11 }
};

char CPIECE_CHAR[6] = {
	'P', 'N', 'B', 'R', 'Q', 'K'
};

/* initial board state */

int CINIT_COLOR[64] = {
	1, 1, 1, 1, 1, 1, 1, 1,
	1, 1, 1, 1, 1, 1, 1, 1,
	6, 6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6, 6,
	0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0
};

int CINIT_PIECE[64] = {
	3, 1, 2, 4, 5, 2, 1, 3,
	0, 0, 0, 0, 0, 0, 0, 0,
	6, 6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6, 6,
	0, 0, 0, 0, 0, 0, 0, 0,
	3, 1, 2, 4, 5, 2, 1, 3
};


/* This is the basic description of a move. promote is what
   piece to promote the pawn to, if the move is a pawn
   promotion. bits is a bitfield that describes the move,
   with the following bits:

   1	capture
   2	castle
   4	en passant capture
   8	pushing a pawn 2 squares
   16	pawn move
   32	promote

   It's union'ed with an integer so two moves can easily
   be compared with each other. */

typedef struct {
	char from;
	char to;
	char promote;
	char bits;
} cmove_bytes;


typedef union {
	cmove_bytes b;
	int u;
} cmove;


/* an element of the move stack. it's just a move with a
   score, so it can be sorted by the search functions. */
typedef struct {
	cmove m;
	int score;
} cgen_t;

/* an element of the history stack, with the information
   necessary to take a move back. */
typedef struct {
	cmove m;
	int capture;
	int castle;
	int ep;
	int fifty;
	int hash;
} chist_t;


struct move_t {
	cmove tscp_move;
	char move_str[6];
};


struct board_t {
	int color[64];
	int piece[64];
	int side;
	int xside;
	int castle;
	int ep;
	int fifty;
	int hash;
};


struct chess_t {
	/* hash numbers for creating board hashes */
	int hash_piece[2][6][64];	
	int hash_side;
	int hash_ep[64];

	/* board state */
	int color[64];
	int piece[64];
	int side;  /* the side to move */
	int xside;
	int castle;  /* the bitfield of the castle permissions */
	int ep;  /* the en passant square. if white moves e2e4, then ep is e3 */
	int fifty;  /* the number of moves since a capture or pawn move */
	int hash;  /* a (more or less) unique number corresponding to the board */
	int ply;  /* the number of half-moves since the root of the search tree */
	int hply;  /* the number of ply since the beginning of the game */

	/* move variables */
	cgen_t gen_dat[CGEN_STACK]; /* space for moves generated by move functions */
	int first_move[CMAX_PLY]; /* first_move[n] to first_move[n+1], excluding */

	/* tscp history */
	int history[64][64];

	Player *white;
	Player *black;
	char white_move[MAX_MOVES][6]; 
	Board white_board[MAX_MOVES];
	char black_move[MAX_MOVES][6];
	Board black_board[MAX_MOVES];

	int num_moves;
	Move move_list[MAX_MOVES_TURN];
	int turn; 
	int result;
};


struct player_t { 
	char *name;  
	int color;
	Move_func *get_move;
};


/* Private prototypes */
/* hash prototypes */
static int cinit_hash(Chess *game);
static int chash_rand();
static int cset_hash(Chess *game);
/* board prototypes */
static int cinit_board(Chess *game);
/* chess prototypes */
static int cgen(Chess *game);
static int cgen_push(Chess *game, int from, int to, int bits);
static int cgen_promote(Chess *game, int from, int to, int bits);
static CBOOL cmakemove(Chess *game, move_bytes m);
static CBOOL cattack(Chess *game, int sq, int s)
static BOOL cin_check(Chess *game, int s)
static char *cmove_str(cmove_bytes m);


/* Hash functions */
/* cinit_hash
 *
 * This function sets a random 32-bit integer for color, piece and square
 * combination, a random number for white and a random number for each en
 * passant square. These random numbers are used to create a hash number for a
 * board position.
 */
static int cinit_hash(Chess *game)
{
	int i, j, k;

	srand(0);
	for (i = 0; i < 2; ++i)
		for (j = 0; j < 6; ++j)
			for (k = 0; k < 64; ++k)
				game->hash_piece[i][j][k] = chash_rand();
	game->hash_side = chash_rand();
	for (i = 0; i < 64; ++i)
		game->hash_ep[i] = chash_rand();

	return 0;
}

/* chash_rand
 * 
 * This function XORs shifted random numbers together to ensure good coverage
 * of all 32 bits.
 */

static int chash_rand()
{
	int i;
	int r = 0;

	for (i = 0; i < 32; ++i)
		r ^= rand() << i;

	return r;
}


/* cset_hash
 *
 * This function uses the Zobrist method of generating a unique number (hash)
 * for the current chess position. Of course, there are many more chess
 * positions than there are 32 bit numbers, so the numbers generated are
 * not really unique, but they're unique enough for our purposes (to detect
 * repetitions of the position). 
 * The way it works is to XOR random numbers that correspond to features of
 * the position, e.g., if there's a black knight on B8, hash is XORed with
 * hash_piece[BLACK][CKNIGHT][B8]. All of the pieces are XORed together,
 * hash_side is XORed if it's black's move, and the en passant square is
 * XORed if there is one. (A chess technicality is that one position can't
 * be a repetition of another if the en passant state is different.)
 *
 * Note that this function generates the hash for the current board position.
 */

static int cset_hash(Chess *game)
{
	int i, hash;

	hash = 0;
	for (i = 0; i < 64; ++i)
		if (game->color[i] != CEMPTY)
			hash ^= game->hash_piece[game->color[i]][game->piece[i]][i];
	if (game->side == CDARK)
		hash ^= game->hash_side;
	if (game->ep != -1)
		hash ^= game->hash_ep[game->ep];

	game->hash = hash;

	return 0;
}


/* Board functions */
/* init_board
 *
 * This function sets the board to the initial game state.
 */

static int cinit_board(Chess *game)
{
	int i;

	for (i = 0; i < 64; ++i) {
		game->color[i] = CINIT_COLOR[i];
		game->piece[i] = CINIT_PIECE[i];
	}
	game->side = CLIGHT;
	game->xside = CDARK;
	game->castle = 15;
	game->ep = -1;
	game->fifty = 0;
	game->ply = 0;
	game->hply = 0;
	cset_hash(game);  /* init_hash() must be called before this function */
	game->first_move[0] = 0;

	return 0;
}


/* Chess functions */
Chess *create_game(void)
{
	Chess *game;
	int i, j;

	game = (Chess *) malloc(sizeof(Chess));
	cinit_hash(game);
	cinit_board(game);
	
	game->white = game->black = NULL;
	game->turn = 1;
	game->result = 0;
	for (i = 0; i < MAX_MOVES; i++)
		for (j = 0; j < 5; j++) {
			game->white_move[i][j] = '\0';
			game->black_move[i][j] = '\0';
		}

	return game;
}

void destroy_game(Chess *game)
{
	free(game);
}

void set_player(Chess *game, Player *player, int color)
{
	if (color == CLIGHT)
		game->white = player;
	if (color == CDARK)
		game->black = player;
}

void display_board(Chess *game)
{
	int i;
	
	printf("\n8 ");
	for (i = 0; i < 64; ++i) {
		switch (game->color[i]) {
			case CEMPTY:
				printf(" .");
				break;
			case CLIGHT:
				printf(" %c", CPIECE_CHAR[game->piece[i]]);
				break;
			case CDARK:
				printf(" %c", CPIECE_CHAR[game->piece[i]] + ('a' - 'A'));
				break;
		}
		if ((i + 1) % 8 == 0 && i != 63)
			printf("\n%d ", 7 - CROW(i));
	}
	printf("\n\n   a b c d e f g h\n\n");
}

void display_info(Chess *game)
{
	printf("Turn: %d\n", game->turn);
	if (game->side == CLIGHT) {
		printf("White's turn to move.\n");
		printf("The previous move was %s.\n", game->black_move[game->turn]);
	} else {
		printf("Black's turn to move\n.");
		printf("The previous move was %s.\n", game->white_move[game->turn]);
	}
}

void display_move(Move *move)
{
	printf("%s\n", move->move_str);
}

void run_game(Chess *game)
{
	return;
}

Move *list_moves(Chess *game, int *num_moves)
{
	int i, first_move, last_move;

	/* gen is a tscp function. It generates pseudo-legal moves and saves them
	 * to the global array gen_dat and modifies first_move[ply+1] to count the
	 * number of moves and track the moves indices in gen_dat.
	 */

	cgen(game); 
	first_move = game->first_move[game->ply];
	last_move = game->first_move[game->ply + 1]; //exclusive i.e. < in loops
	for (i = first_move; i < last_move; i++) {
		game->move_list[i - first_move].tscp_move = game->gen_dat[i].m;
		strcpy(game->move_list[i - first_move].move_str,
			   cmove_str(game->gen_dat[i].m.b));
	}

	game->num_moves = last_move - first_move;
	if (game->num_moves <= 0) {
		*num_moves = 0;
		return NULL;
	}

	*num_moves = game->num_moves;
	return game->move_list;
}


/* cgen
 *
 * This function generates pseudo-legal moves for the current position. A
 * pseduo-legal move is a move that respects a pieces move pattern but could
 * result in check. This function scans the board to find friendly pieces and
 * then determines what squares they attack. When it finds a piece/square
 * combination, it calls gen_push to put the move on the move stack. It also
 * scans for castling moves and en passsant moves, in addition to regular
 * moves. */

static int cgen(Chess *game)
{
	int i, j, n, ep;

	/* so far, we have no moves for the current ply */
	game->first_move[game->ply + 1] = game->first_move[game->ply];

	for (i = 0; i < 64; ++i)
		if (game->color[i] == game->side) {
			if (game->piece[i] == CPAWN) {
				if (game->side == CLIGHT) {
					if (CCOL(i) != 0 && game->color[i - 9] == CDARK)
						cgen_push(game, i, i - 9, 17);
					if (CCOL(i) != 7 && game->color[i - 7] == CDARK)
						cgen_push(game, i, i - 7, 17);
					if (game->color[i - 8] == CEMPTY) {
						cgen_push(game, i, i - 8, 16);
						if (i >= 48 && game->color[i - 16] == CEMPTY)
							cgen_push(game, i, i - 16, 24);
					}
				}
				else {
					if (CCOL(i) != 0 && game->color[i + 7] == CLIGHT)
						cgen_push(game, i, i + 7, 17);
					if (CCOL(i) != 7 && game->color[i + 9] == CLIGHT)
						cgen_push(game, i, i + 9, 17);
					if (game->color[i + 8] == CEMPTY) {
						cgen_push(game, i, i + 8, 16);
						if (i <= 15 && game->color[i + 16] == CEMPTY)
							cgen_push(game, i, i + 16, 24);
					}
				}
			}
			else
				for (j = 0; j < COFFSETS[game->piece[i]]; ++j)
					for (n = i;;) {
						n = CMAILBOX[CMAILBOX64[n] + 
							COFFSET[game->piece[i]][j]];
						if (n == -1)
							break;
						if (game->color[n] != CEMPTY) {
							if (game->color[n] == game->xside)
								cgen_push(game, i, n, 1);
							break;
						}
						cgen_push(game, i, n, 0);
						if (!CSLIDE[game->piece[i]])
							break;
					}
		}

	/* generate castle moves */
	if (game->side == CLIGHT) {
		if (game->castle & 1)
			cgen_push(game, CE1, CG1, 2);
		if (game->castle & 2)
			cgen_push(game, CE1, CC1, 2);
	}
	else {
		if (game->castle & 4)
			cgen_push(game, CE8, CG8, 2);
		if (game->castle & 8)
			cgen_push(game, CE8, CC8, 2);
	}
	
	/* generate en passant moves */
	ep = game->ep;
	if (ep != -1) {
		if (game->side == CLIGHT) {
			if (CCOL(ep) != 0 && game->color[ep + 7] == CLIGHT &&
				game->piece[ep + 7] == CPAWN)
				cgen_push(game, ep + 7, ep, 21);
			if (CCOL(ep) != 7 && game->color[ep + 9] == CLIGHT &&
				game->piece[ep + 9] == CPAWN)
				cgen_push(game, ep + 9, ep, 21);
		}
		else {
			if (CCOL(ep) != 0 && game->color[ep - 9] == CDARK &&
				game->piece[ep - 9] == CPAWN)
				cgen_push(game, ep - 9, ep, 21);
			if (CCOL(ep) != 7 && game->color[ep - 7] == CDARK &&
				game->piece[ep - 7] == CPAWN)
				cgen_push(game, ep - 7, ep, 21);
		}
	}

	return 0;
}


/* cgen_push()
 *
 * This function puts a move on the move stack, unless it's a pawn promotion
 * that needs to be handled by gen_promote(). It also assigns a score to the
 * move for alpha-beta move ordering. If the move is a capture, it uses MVV/LVA
 * (Most Valuable Victim/Least Valuable Attacker). Otherwise, it uses the
 * move's history heuristic value. Note that 1,000,000 is added to a capture
 * move's score, so it always gets ordered above a "normal" move.
 */

static int cgen_push(Chess *game, int from, int to, int bits)
{
	cgen_t *g;
	
	if (bits & 16) {
		if (game->side == CLIGHT) {
			if (to <= CH8) {
				cgen_promote(game, from, to, bits);
				return 0;
			}
		}
		else {
			if (to >= CA1) {
				cgen_promote(game, from, to, bits);
				return 0;
			}
		}
	}
	g = &(game->gen_dat[game->first_move[game->ply + 1]++]);
	g->m.b.from = (char)from;
	g->m.b.to = (char)to;
	g->m.b.promote = 0;
	g->m.b.bits = (char)bits;
	if (game->color[to] != CEMPTY)
		g->score = 1000000 + (game->piece[to] * 10) - game->piece[from];
	else
		g->score = game->history[from][to];

	return 0;
}


/* cgen_promote
 *
 * This function is just like gen_push(), only it puts 4 moves on the move
 * stack, one for each possible promotion piece
 */

static int cgen_promote(Chess *game, int from, int to, int bits)
{
	int i;
	cgen_t *g;
	
	for (i = CKNIGHT; i <= CQUEEN; ++i) {
		g = &(game->gen_dat[game->first_move[game->ply + 1]++]);
		g->m.b.from = (char)from;
		g->m.b.to = (char)to;
		g->m.b.promote = (char)i;
		g->m.b.bits = (char)(bits | 32);
		g->score = 1000000 + (i * 10);
	}

	return 0;
}


/* move_str returns a string with move m in coordinate notation */

static char *cmove_str(cmove_bytes m)
{
	static char str[6];

	char c;

	if (m.bits & 32) {
		switch (m.promote) {
			case CKNIGHT:
				c = 'n';
				break;
			case CBISHOP:
				c = 'b';
				break;
			case CROOK:
				c = 'r';
				break;
			default:
				c = 'q';
				break;
		}
		sprintf(str, "%c%d%c%d%c",
				CCOL(m.from) + 'a',
				8 - CROW(m.from),
				CCOL(m.to) + 'a',
				8 - CROW(m.to),
				c);
	}
	else
		sprintf(str, "%c%d%c%d",
				CCOL(m.from) + 'a',
				8 - CROW(m.from),
				CCOL(m.to) + 'a',
				8 - CROW(m.to));
	return str;
}

int make_move(Chess *game, Move *move)
{
	/* do tscp stuff */
	if (!cmakemove(game, move->tscp_move.b))
	/* do chess stuff */
	/*
	char white_move[MAX_MOVES][6]; 
	Board white_board[MAX_MOVES];
	char black_move[MAX_MOVES][6];
	Board black_board[MAX_MOVES];
	*/

	return 0;
}

/* cmakemove() makes a move. If the move is illegal, it
   undoes whatever it did and returns FALSE. Otherwise, it
   returns TRUE. */
static CBOOL cmakemove(move_bytes m)
{
	
	/* test to see if a castle move is legal and move the rook
	   (the king is moved with the usual move code later) */
	if (m.bits & 2) {
		int from, to;

		if (in_check(side))
			return FALSE;
		switch (m.to) {
			case 62:
				if (color[F1] != EMPTY || color[G1] != EMPTY ||
						attack(F1, xside) || attack(G1, xside))
					return FALSE;
				from = H1;
				to = F1;
				break;
			case 58:
				if (color[B1] != EMPTY || color[C1] != EMPTY || color[D1] != EMPTY ||
						attack(C1, xside) || attack(D1, xside))
					return FALSE;
				from = A1;
				to = D1;
				break;
			case 6:
				if (color[F8] != EMPTY || color[G8] != EMPTY ||
						attack(F8, xside) || attack(G8, xside))
					return FALSE;
				from = H8;
				to = F8;
				break;
			case 2:
				if (color[B8] != EMPTY || color[C8] != EMPTY || color[D8] != EMPTY ||
						attack(C8, xside) || attack(D8, xside))
					return FALSE;
				from = A8;
				to = D8;
				break;
			default:  /* shouldn't get here */
				from = -1;
				to = -1;
				break;
		}
		color[to] = color[from];
		piece[to] = piece[from];
		color[from] = EMPTY;
		piece[from] = EMPTY;
	}

	/* back up information so we can take the move back later. */
	hist_dat[hply].m.b = m;
	hist_dat[hply].capture = piece[(int)m.to];
	hist_dat[hply].castle = castle;
	hist_dat[hply].ep = ep;
	hist_dat[hply].fifty = fifty;
	hist_dat[hply].hash = hash;
	++ply;
	++hply;

	/* update the castle, en passant, and
	   fifty-move-draw variables */
	castle &= castle_mask[(int)m.from] & castle_mask[(int)m.to];
	if (m.bits & 8) {
		if (side == LIGHT)
			ep = m.to + 8;
		else
			ep = m.to - 8;
	}
	else
		ep = -1;
	if (m.bits & 17)
		fifty = 0;
	else
		++fifty;

	/* move the piece */
	color[(int)m.to] = side;
	if (m.bits & 32)
		piece[(int)m.to] = m.promote;
	else
		piece[(int)m.to] = piece[(int)m.from];
	color[(int)m.from] = EMPTY;
	piece[(int)m.from] = EMPTY;

	/* erase the pawn if this is an en passant move */
	if (m.bits & 4) {
		if (side == LIGHT) {
			color[m.to + 8] = EMPTY;
			piece[m.to + 8] = EMPTY;
		}
		else {
			color[m.to - 8] = EMPTY;
			piece[m.to - 8] = EMPTY;
		}
	}

	/* switch sides and test for legality (if we can capture
	   the other guy's king, it's an illegal position and
	   we need to take the move back) */
	side ^= 1;
	xside ^= 1;
	if (in_check(xside)) {
		takeback();
		return FALSE;
	}
	set_hash();
	return TRUE;
}


/* takeback() is very similar to makemove(), only backwards :)  */

void takeback()
{
	move_bytes m;

	side ^= 1;
	xside ^= 1;
	--ply;
	--hply;
	m = hist_dat[hply].m.b;
	castle = hist_dat[hply].castle;
	ep = hist_dat[hply].ep;
	fifty = hist_dat[hply].fifty;
	hash = hist_dat[hply].hash;
	color[(int)m.from] = side;
	if (m.bits & 32)
		piece[(int)m.from] = PAWN;
	else
		piece[(int)m.from] = piece[(int)m.to];
	if (hist_dat[hply].capture == EMPTY) {
		color[(int)m.to] = EMPTY;
		piece[(int)m.to] = EMPTY;
	}
	else {
		color[(int)m.to] = xside;
		piece[(int)m.to] = hist_dat[hply].capture;
	}
	if (m.bits & 2) {
		int from, to;

		switch(m.to) {
			case 62:
				from = F1;
				to = H1;
				break;
			case 58:
				from = D1;
				to = A1;
				break;
			case 6:
				from = F8;
				to = H8;
				break;
			case 2:
				from = D8;
				to = A8;
				break;
			default:  /* shouldn't get here */
				from = -1;
				to = -1;
				break;
		}
		color[to] = side;
		piece[to] = ROOK;
		color[from] = EMPTY;
		piece[from] = EMPTY;
	}
	if (m.bits & 4) {
		if (side == LIGHT) {
			color[m.to + 8] = xside;
			piece[m.to + 8] = PAWN;
		}
		else {
			color[m.to - 8] = xside;
			piece[m.to - 8] = PAWN;
		}
	}
}


/* in_check() returns TRUE if side s is in check and FALSE
   otherwise. It just scans the board to find side s's king
   and calls attack() to see if it's being attacked. */

BOOL in_check(int s)
{
	int i;

	for (i = 0; i < 64; ++i)
		if (piece[i] == KING && color[i] == s)
			return attack(i, s ^ 1);
	return TRUE;  /* shouldn't get here */
}


/* attack() returns TRUE if square sq is being attacked by side
   s and FALSE otherwise. */

BOOL attack(int sq, int s)
{
	int i, j, n;

	for (i = 0; i < 64; ++i)
		if (color[i] == s) {
			if (piece[i] == PAWN) {
				if (s == LIGHT) {
					if (COL(i) != 0 && i - 9 == sq)
						return TRUE;
					if (COL(i) != 7 && i - 7 == sq)
						return TRUE;
				}
				else {
					if (COL(i) != 0 && i + 7 == sq)
						return TRUE;
					if (COL(i) != 7 && i + 9 == sq)
						return TRUE;
				}
			}
			else
				for (j = 0; j < offsets[piece[i]]; ++j)
					for (n = i;;) {
						n = mailbox[mailbox64[n] + offset[piece[i]][j]];
						if (n == -1)
							break;
						if (n == sq)
							return TRUE;
						if (color[n] != EMPTY)
							break;
						if (!slide[piece[i]])
							break;
					}
		}
	return FALSE;
}


/* Player functions */
Player *create_player(char *name, int color, Move_func *get_move)

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
	if (player->color == CLIGHT)
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
