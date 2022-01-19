import numpy as np
import os

WIDTH, HEIGHT = 7, 6  # dimentions
EMPTY = '*'
CONNECT_X = 4
MAX_DEPTH = 6

# ---------------------------------------- #
BRIAN, SASHA = 'R', 'B'
FIRST_PLAYER = SASHA
# ---------------------------------------- #

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
'''
def check_win(cords):
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
    if count >= CONNECT_X:
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
    if count >= CONNECT_X:
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
    if count >= CONNECT_X:
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
    if count >= CONNECT_X:
        return True

    return False


'''
def eval_score(cord, depth, player)
    win:        return 1000
    max_depth:  return 0
    n/a:        return max([-recurse(m, depth+1, next_player) for m in moves])

@param cords: cords of previous turn
@param player: player of previous turn
@param depth: current depth
@return: value of that previous turn's move
'''
def eval_score(cords, player, depth):
    if check_win(cords):
        return 1000
    elif depth >= MAX_DEPTH:
        return 0
    else:
        scores = [None for i in range(WIDTH)]
        next_p = next_player(player)
        for c in range(WIDTH):
            # make a move, store it on stack, recurse, undo move - all on the same board
            cords = place_move(c, next_p)
            if cords is None:
                continue
            scores[c] = eval_score(cords, next_p, depth+1)
            remove_move(c)
        # print(f'scores={scores}, depth={depth}')
        scores = [s for s in scores if s != None]  # remove illegal moves
        # enemy_score = max(scores)  # calculate max, assuming they do best move every time
        enemy_score = sum(scores) / len(scores)  # calc avg
        return -enemy_score

'''
return: (the best move, list of move scores)
'''
def best_move(player):
    scores = [-9999999 for i in range(WIDTH)]
    for c in range(WIDTH):
        cords = place_move(c, player)
        if cords is None:
            continue
        scores[c] = eval_score(cords, player, depth=0)
        remove_move(c)
    return np.argmax(scores), scores
