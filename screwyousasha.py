from connectX_util import *

def print_board():
    print(board)
    print()
    print(np.array([[str(i) for i in range(0,WIDTH)]]), '(columns)')
    print()

# hack to fix the first person, the error prevents the player switch
cur_player = FIRST_PLAYER
error_txt = f'Welcome to Connect{CONNECT_X}™!\n'
while True:
    os.system('cls' if os.name == 'nt' else 'clear')

    if error_txt != None:
        print(error_txt)
        error_txt = None
    else:  # progress the game
        cur_player = next_player(cur_player)
    player_str = f'SASHA (color={cur_player})' if cur_player is SASHA else f'Brian (color={cur_player})'

    print_board()

    if cur_player == BRIAN: # automated
        best_m, scores = best_move(cur_player)
        print(f'Recommended move: {best_m}')
        print(f'scores: {[(m,int(s)) for m,s in enumerate(scores)]}\n')
        input(f'{player_str} will move accordingly, press enter..')
        txt = str(best_m)
    else: # Sasha actually plays
        txt = input(f'{player_str}, enter your move (0-{WIDTH-1}): ')

    if txt == 'exit':
        exit(69)
    try:
        move = int(txt)
        cords = place_move(move, cur_player)
        if not cords:  # no move made
            raise ValueError('Invalid column index.')
    except:
        error_txt = f'Invalid move.\nPlease provide the column index of your legal move (between 0 and {WIDTH-1}, inclusive), or "exit" to exit\n'
        continue

    if check_win(cords):
        os.system('cls' if os.name == 'nt' else 'clear')
        print_board()
        print(f'\n{player_str} wins!!!!!\n')
        exit(0)  

# TODO
'''
X interface to play in terminal
X recursive solution
- memoization
- pygame click to play
- watch the screen and read/play automatically 
    - click the top left and bottom right spots, it calculates positions to motitor itself
'''