from tabnanny import check
import numpy as np
import os

# ---------------------------------------- #
BRIAN, SASHA = 'R', 'B'
FIRST_PLAYER = BRIAN
# ---------------------------------------- #

WIDTH, HEIGHT = 7, 6  # dimentions (7x6 standard)
EMPTY = '*'
CONNECT_X = 4
MAX_DEPTH = 6
LOG_FILENAME = 'log.txt'

CONNECT_X_VALUE = 1000  # score for a win, multiplied by the layers left in the search
CONNECT_X_CLOSE_VALUE = 69  # score added for a setup for winning (aka 3 in a row)
MAX_NEG_SCORE = -9999999  # represents an illegal move that should never be chosen

board = np.full((HEIGHT,WIDTH), EMPTY)

'''
Check if a cord is on the board
@param cords: (r,c) tuple of just placed move
@return: True if valid, False if out of bounds
'''
def valid_cord(cords):
    r,c = cords
    return not (r < 0 or c < 0 or r >= HEIGHT or c >= WIDTH)

'''
Updates the board with a move, if it is valid
@param move: colm index of move
@param player: player value
return: (r,c) move cordinates on success, None on invalid move
'''
def place_move(move, player):
    c = move
    if not valid_cord((0,c)):  # does colm exist?
        return None
    colm = board[:,c]
    for r in range(len(colm)):
        if colm[r] != EMPTY:
            if r == 0:  # full colm, illegal move
                return None
            else:
                r = r - 1
                break  # we found the bottom piece
    board[r,c] = player
    return r,c

'''
Remove the top of a colm (assuming move already placed)
@param move: colm index of previously placed move
'''
def remove_move(move):
    c = move
    colm = board[:,c]
    for r in range(HEIGHT):
        if colm[r] != EMPTY:
            colm[r] = EMPTY
            return

def next_player(cur_player):
    return SASHA if cur_player is BRIAN else BRIAN

'''
Check a win of a move (assuming move already placed)
@param cords: (r,c) tuple of just placed move
@param to_win: number in a row needed to win
@return True on win, False otherwise
'''
def check_win(cords, to_win=CONNECT_X):
    rN, cN = cords  # new chip cords
    player = board[rN,cN]
    count = 1  # how many in a row so far
    if player is EMPTY:
        return False
    
    # check vertical with sliding windows
    count = 1
    # grow upwards
    for r in range(rN - 1, -1, -1):
        if board[r,cN] != player:
            break
        count += 1
    # grow downwards
    for r in range(rN + 1, HEIGHT, 1):
        if board[r,cN] != player:
            break
        count += 1
    # check win
    if count >= to_win:
        return True

    # check horizontal with sliding windows
    count = 1
    # grow leftwards
    for c in range(cN - 1, -1, -1):
        if board[rN,c] != player:
            break
        count += 1
    # grow rightwards
    for c in range(cN + 1, WIDTH, 1):
        if board[rN,c] != player:
            break
        count += 1
    # check win
    if count >= to_win:
        return True
    
    # check top-left to bottom-right with sliding windows
    count = 1
    # grow up-left
    r, c = rN - 1, cN - 1
    while True:
        if not valid_cord((r,c)) or board[r,c] != player:
            break
        r, c = r - 1, c - 1
        count += 1
    # grow down-right
    r, c = rN + 1, cN + 1
    while True:
        if not valid_cord((r,c)) or board[r,c] != player:
            break
        r, c = r + 1, c + 1
        count += 1
    # check win
    if count >= to_win:
        return True

    # check top-right to bottom-left with sliding windows
    count = 1
    # grow up-right
    r, c = rN - 1, cN + 1
    while True:
        if not valid_cord((r,c)) or board[r,c] != player:
            break
        r, c = r - 1, c + 1
        count += 1
    # grow down-left
    r, c = rN + 1, cN - 1
    while True:
        if not valid_cord((r,c)) or board[r,c] != player:
            break
        r, c = r + 1, c - 1
        count += 1
    # check win
    if count >= to_win:
        return True

    return False


'''
def eval_score(cord, depth, player)
    win:        return 1000
    max_depth:  return 0
    connectX-1: return 50 + (n/a)
    n/a:        return max([-recurse(m, depth+1, next_player) for m in moves])

@param cords: cords of previous turn
@param player: player of previous turn
@param layer: current layers of depth remaining
@return: value of that previous turn's move
'''
def eval_score(cords, player, layer):
    if check_win(cords):
        return CONNECT_X_VALUE * layer  # extra value if you win sooner
    elif layer == 0:
        return 0  # too deep
    else:
        connectx_close_score = CONNECT_X_CLOSE_VALUE if check_win(cords, CONNECT_X-1) else 0
        scores = [None for i in range(WIDTH)]
        next_p = next_player(player)
        for c in range(WIDTH):
            # make a move, store it on stack, recurse, undo move - all on the same board
            cords = place_move(c, next_p)
            if cords is None:
                continue
            scores[c] = eval_score(cords, next_p, layer-1)
            remove_move(c)
        scores = [s for s in scores if s != None]  # remove illegal moves
        if len(scores) == 0:
            return MAX_NEG_SCORE

        enemy_score = max(scores)  # calculate max, assuming they do best move every time
        return -enemy_score + connectx_close_score

'''
return: (the best move, list of move scores)
'''
def best_move(player):
    scores = [MAX_NEG_SCORE for i in range(WIDTH)]
    for c in range(WIDTH):
        cords = place_move(c, player)
        if cords is None:
            continue
        scores[c] = eval_score(cords, player, MAX_DEPTH)
        remove_move(c)
    max_score = max(scores)
    # return np.argmax(scores), scores
    # sketchy fix to get the most "middle" move
    best_scores = [i for i,s in enumerate(scores) if s == max_score]
    return min(best_scores, key=lambda x:abs(x - (WIDTH // 2))), scores
