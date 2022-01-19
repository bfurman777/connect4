from connectX_util import *

OUTPUT_FILE = 'out_prettygraphs.txt'

# a node is the string of a graph
graph = dict()  # {node:[children nodes]}

'''
Build the graph
'''
def go_deeper(player, layers=5):
    if layers <= 0:
        return  # we've gone too deep!

    board_str = str(board)
    
    if not board_str in graph:
        graph[board_str] = set()
    else:
        return  # we've been down this path before

    children = graph[board_str]
    player = next_player(player)
    for c in range(WIDTH):
        # make a move, store it on stack, recurse, undo move - all on the same board
        cords = place_move(c, player)
        if cords is None:  # illegal move
            continue
        
        child_str = str(board)
        children.add(child_str)

        # if check_win(cords):
        #     if not child_str in graph:
        #         graph[child_str] = set()
        #     graph[child_str].add(player)

        go_deeper(player, layers-1)

        remove_move(c)


# main
go_deeper(BRIAN)

with open(OUTPUT_FILE, 'w') as f:
    for b, children in graph.items():
        f.write(b)
        f.write('\nchilds:')
        for child in children:
            f.write(f'\n{child}')
        f.write('\n\n')
