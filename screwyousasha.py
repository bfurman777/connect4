'''
This will handle the gameplay interaction.
Please run from linux.
'''

from connectX_util import *
import os

if __name__ == '__main__':

    if os.name != 'nt':
        print('Please run from Windows. Unfortunatly')
        exit(420)

    # hack to fix the first person on the first loop, the error_txt prevents the player switch
    cur_player = FIRST_PLAYER
    error_txt = f'Welcome to Connect{CONNECT_X}™!\n'

    board = empty_board()

    # option to type in a board (load)
    txt = input('(S)tart or (L)oad? ')
    if txt in ['l', 'L', 'load', 'Load']:
        txt = input(f'Load (p1={cur_player}) -> type in sequence of moves: ')
        for chr in txt:
            c = int(chr)
            if place_move(c, cur_player, board):
                cur_player = next_player(cur_player)

    with open(LOG_FILENAME,'w') as file:
        file.write('')  # overwrite file

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        if error_txt != None:
            printLog(error_txt)
            error_txt = None
        else:  # progress the game
            cur_player = next_player(cur_player)
        player_str = f'SASHA (color={cur_player})' if cur_player is SASHA else f'Brian (color={cur_player})'

        print_board(board)

        if cur_player == BRIAN: # or True: # calculate best move
            best_m, scores = best_move(cur_player, board)
            printLog(f'Recommended move: {best_m}')
            printLog(f'scores: {[(m,int(s)) for m,s in enumerate(scores)]}\n')
        elif cur_player == SASHA:
            best_m, scores = best_move_lite(cur_player, board)
            printLog(f'Sasha, don\'t screw up!')
            printLog(f'scores: {[(m,int(s)) for m,s in enumerate(scores)]}\n')
        txt = input(f'{player_str}, enter your move (0-{WIDTH-1}): ')

        if txt == 'exit':
            exit(69)
        try:
            move = int(txt)
            cords = place_move(move, cur_player, board)
            if not cords:  # no move made
                raise ValueError('Invalid column index.')
        except:
            print("ERROR")
            error_txt = f'Invalid move.\nPlease provide the column index of your legal move (between 0 and {WIDTH-1}, inclusive), or "exit" to exit\n'
            continue

        if check_win(cords, board):
            os.system('cls' if os.name == 'nt' else 'clear')
            print_board(board)
            printLog(f'\n{player_str} wins!!!!!\n')
            exit(0)  

    # TODO
    '''
    X interface to play in terminal
    X recursive solution
    X memoization
    X better algo (some score for connect 3 without extra for a dead end 3? how about split 3s?)
    - pygame click to play
    - watch the screen and read/play automatically 
        - click the top left and bottom right spots, it calculates positions to motitor itself
    '''