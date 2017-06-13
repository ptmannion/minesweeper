import pdb
import random
import os
import sys
import time
from termcolor import colored

# TODO
# rows are labeled by letters e.g., A4
# print in color
# add ability to win game

# Default globals - can be reset with commandline params
MINE_DENSITY = 0.20
BOARD_WIDTH = 10
BOARD_HEIGHT = 10
START_TIME = time.time()

def create_mask(value):
    ''' create mask as list of lists (list of rows) of repeated value input '''

    if type(value) != int:
        raise ValueError('Mask value must be int.')

    mask = []
    for r in range(0,BOARD_HEIGHT):
        row = [value] * BOARD_WIDTH
        mask.append(row)

    return mask

def valid_space(r,c):
    valid_row = (r >= 0) & (r < BOARD_HEIGHT)
    valid_col = (c >= 0) & (c < BOARD_WIDTH)
    return valid_row & valid_col

def get_neighbors(r,c):
    neighbors = [(r-1,c),
    (r-1,c+1),
    (r,c+1),
    (r+1,c+1),
    (r+1,c),
    (r+1,c-1),
    (r,c-1),
    (r-1,c-1)
    ]

    valid_neighbors = []
    for r,c in neighbors:
        if valid_space(r,c):
            valid_neighbors.append((r,c))

    return valid_neighbors

def create_board():
    ''' create board with mines and adjacency counts '''

    # create board as list of lists (list of rows)
    board = []
    for r in range(0,BOARD_HEIGHT):
        row = ["0"] * BOARD_WIDTH
        board.append(row)

    # place mines
    mine_count = 0
    mine_locations = []
    for r in range(0,BOARD_HEIGHT):
        for c in range(0,BOARD_WIDTH):
            v = random.randint(1,1/MINE_DENSITY)
            if v == 1:
                has_mine = True
                mine_count += 1
                mine_locations.append((r,c))
            else:
                has_mine = False

            if has_mine:
                board[r][c] = "*"

    # count adjacent mines
    for r in range(0,BOARD_HEIGHT):
        for c in range(0,BOARD_WIDTH):
            if board[r][c] == "*":
                continue

            # enumerate neighbor coords clockwise from top
            valid_neighbors = get_neighbors(r,c)

            # count neighboring mines and use to update block
            count = 0
            for nr,nc in valid_neighbors:
                    if board[nr][nc] == "*":
                        count += 1

            board[r][c] = str(count)

    return (board,mine_count,mine_locations)

def get_input():
    ''' get user input of column and row number '''

    print "\nEnter row,col to click, f#,# to flag or u#,# to unflag."
    user_input = raw_input()

    move_type = 'click' # set default

    if user_input[0] == 'f':
        move_type = 'flag'
        user_input = user_input[1:]
    if user_input[0] == 'u':
        move_type = 'unflag'
        user_input = user_input[1:]

    try:
        r,c = user_input.split(",")
        r = int(r)
        c = int(c)

        if mask[r][c] == 0:
            print "This block has already been clicked. Try again:"
            move = get_input()

        if not valid_space(r,c):
            print "Your move is not on the board. Try again:"
            move = get_input()
        else:
            move = (r,c)

    except ValueError:
         print "Please use the format specified, e.g., '0,0'"
         move = get_input()

    return (move,move_type)

def recursive_clear(r,c,mask):
    if mask[r][c] == 0:
        # if already clear, move on
        return mask

    if int(board[r][c]) >= 1:
        # reveal number square
        mask[r][c] = 0
        return mask

    elif int(board[r][c]) == 0:
        # reveal blank square and neighbors up to number
        mask[r][c] = 0
        valid_neighbors = get_neighbors(r,c)

        for nr,nc in valid_neighbors:
            mask = recursive_clear(nr,nc,mask)

    return mask

def update_mask(board,mask,move,move_type,mine_count):
    r,c = move

    # if coordinates are a mine, game over
    if move_type == 'click':
        if board[r][c] == "*":
            os.system('clear')

            for mr,mc in mine_locations:
                mask[mr][mc] = 0
            print_board(board,mask,mine_count)

            print colored('Game over!','red')
            quit()

        else:
            mask = recursive_clear(r,c,mask)
    elif move_type == 'flag':
        mask[r][c] = 2
        mine_count -= 1
    elif move_type == 'unflag':
        mask[r][c] = 1
        mine_count += 1

    return mask,mine_count

def print_board(board,mask,mine_count):
    ''' print board, given mask, with column and row numbers '''

    # print mine count and timer
    seconds_passed = int(time.time() - START_TIME)
    print "Mines remaining: %i \t\t Time elapsed (sec): %i" % (mine_count, seconds_passed)

    # print column labels
    print " " * 6,
    for c in range(0,BOARD_WIDTH):
        spacing = 3 - len(str(c))
        print "  %i%s" % (c,spacing*" "),
    print "" # newline

    print " " * 6,
    for c in range(0,BOARD_WIDTH):
        print "_____",
    print "" # newline


    for r in range(0,BOARD_HEIGHT):
        # print row labels
        spacing = 3 - len(str(r))
        print "  %i%s|" % (r,spacing*" "),

        # print row contents
        for c in range(0,BOARD_WIDTH):
            # only print row if mask is 0, not 1
            if mask[r][c] == 0:
                value = board[r][c]
                block = '  %s  ' % value
                if value == '*':
                    print colored(block,'red'),
                else:
                    print colored(block,'green'),

            elif mask[r][c] == 1:
                block = "     "
                print block,
            elif mask[r][c] == 2:
                block = "  F  "
                print colored(block,'red'),
        print "" # newline

if __name__ == "__main__":

    if len(sys.argv) > 2:
        BOARD_WIDTH = int(sys.argv[1])
        BOARD_HEIGHT = int(sys.argv[2])
    if len(sys.argv) > 3:
        MINE_DENSITY = float(sys.argv[3])

    board,mine_count,mine_locations = create_board()
    mask = create_mask(1)

    while True:
        # clear console window
        os.system('clear')

        print_board(board,mask,mine_count)
        move,move_type = get_input()
        mask,mine_count = update_mask(board,mask,move,move_type,mine_count)
