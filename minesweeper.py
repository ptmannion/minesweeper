import pdb
import random
import os
import sys
import time
from termcolor import colored

# Default globals - can be reset with commandline params
MINE_DENSITY = 0.20
BOARD_WIDTH = 10
BOARD_HEIGHT = 10

START_TIME = time.time()

def valid_space(r,c):
    ''' check if a set of coordinates is valid on the board '''

    valid_row = (r >= 0) & (r < BOARD_HEIGHT)
    valid_col = (c >= 0) & (c < BOARD_WIDTH)
    return valid_row & valid_col

def get_neighbors(r,c):
    ''' get coords of neighboring cells that are valid on the board '''

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

    # create blank board as list of rows
    board = []
    mask = []
    for r in range(0,BOARD_HEIGHT):
        board_row = ["0"] * BOARD_WIDTH
        board.append(board_row)

        mask_row = [1] * BOARD_WIDTH
        mask.append(mask_row)

    # place mines
    mine_count = 0
    mine_locations = []
    for r in range(0,BOARD_HEIGHT):
        for c in range(0,BOARD_WIDTH):
            v = random.randint(1,1/MINE_DENSITY)
            if v == 1:
                board[r][c] = "*"
                mine_count += 1
                mine_locations.append((r,c))

    # count adjacent mines
    for r in range(0,BOARD_HEIGHT):
        for c in range(0,BOARD_WIDTH):
            # skip mines
            if board[r][c] == "*":
                continue

            # count neighboring mines and use to update cell
            count = 0
            for nr,nc in get_neighbors(r,c):
                    if board[nr][nc] == "*":
                        count += 1
            board[r][c] = str(count)

    return (board,mask,mine_count,mine_locations)

def get_input():
    ''' get user input of column and row number '''

    print "\nEnter row,col to click, f#,# to flag mine or u#,# to unflag."
    user_input = raw_input()

    move_type = 'click' # set as default

    # override default move type and strip input to coords
    if user_input[0] == 'f':
        move_type = 'flag'
        user_input = user_input[1:]
    if user_input[0] == 'u':
        move_type = 'unflag'
        user_input = user_input[1:]

    # check for valid coords of move
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
    ''' remove mask from cell and adjacent cells as needed on click '''

    # base case - cell already cleared
    if mask[r][c] == 0:
        return mask

    # base case - number cell at edge of area to clear
    if int(board[r][c]) >= 1:
        mask[r][c] = 0
        return mask

    # recursive case - blank cell, need to clear neighbors
    elif int(board[r][c]) == 0:
        mask[r][c] = 0
        valid_neighbors = get_neighbors(r,c)
        for nr,nc in valid_neighbors:
            mask = recursive_clear(nr,nc,mask)

    return mask

def update_mask(board,mask,move,move_type,mine_count):
    r,c = move

    # normal click moves
    if move_type == 'click':
        # game over
        if board[r][c] == "*":
            os.system('clear')
            for mr,mc in mine_locations:
                mask[mr][mc] = 0
            print_board(board,mask,mine_count)
            print colored('Game over!','red')
            quit()
        # normal move - clear cell(s)
        else:
            mask = recursive_clear(r,c,mask)

    # flag and unflag moves
    elif move_type == 'flag':
        mask[r][c] = 2
        mine_count -= 1
    elif move_type == 'unflag':
        mask[r][c] = 1
        mine_count += 1

    # check if the game has been won
    all_mines_flagged = (mine_count == 0) # count of flags equals count of mines
    sum_of_mask_values = sum(sum(mask,[])) # sums flattened mask list
    all_other_cells_cleared = (sum_of_mask_values == len(mine_locations)*2) # all cells cleared except flags, which are 2's
    if all_mines_flagged & all_other_cells_cleared:
        os.system('clear')
        print_board(board,mask,mine_count)
        print colored('You won!','green')
        quit()

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
            # only print cell values if mask is 0
            if mask[r][c] == 0:
                value = board[r][c]
                block = '  %s  ' % value
                if value == '*':
                    print colored(block,'red'),
                else:
                    print colored(block,'green'),

            # handle masked (blank) and flagged cells
            elif mask[r][c] == 1:
                block = "     "
                print block,
            elif mask[r][c] == 2:
                block = "  F  "
                print colored(block,'red'),
        print "" # newline

if __name__ == "__main__":

    # handle custom board parameters
    if len(sys.argv) > 2:
        BOARD_WIDTH = int(sys.argv[1])
        BOARD_HEIGHT = int(sys.argv[2])
    if len(sys.argv) > 3:
        MINE_DENSITY = float(sys.argv[3])

    # initialize board
    board,mask,mine_count,mine_locations = create_board()

    # run game loop
    while True:
        # clear console window
        os.system('clear')

        print_board(board,mask,mine_count)
        move,move_type = get_input()
        mask,mine_count = update_mask(board,mask,move,move_type,mine_count)
