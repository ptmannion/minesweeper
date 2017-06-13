import random
import pdb

MINE_DENSITY = 0.20
BOARD_WIDTH = 10
BOARD_HEIGHT = 10

def create_mask(value):
    ''' reate mask as list of lists (list of rows) of repeated value input '''

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
    '''create board with mines and adjacency counts, plus full mask'''

    # create board as list of lists (list of rows)
    board = []
    for r in range(0,BOARD_HEIGHT):
        row = ["0"] * BOARD_WIDTH
        board.append(row)

    # place mines
    for r in range(0,BOARD_HEIGHT):
        for c in range(0,BOARD_WIDTH):
            v = random.randint(1,1/MINE_DENSITY)
            if v == 1:
                has_mine = True
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

    return board

def get_input():
    ''' get user input of column and row number '''

    print "Select a block to click (format: row,column): "
    user_input = raw_input()

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

    return move

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

def update_mask(board,mask,move):
    r,c = move

    # if coordinates are a mine, game over
    if board[r][c] == "*":
        clear_mask = create_mask(0,size)
        print_board(board,clear_mask)

        print "Game over!"
        quit()

    else:
        mask = recursive_clear(r,c,mask)

    return mask

def print_board(board,mask):
    # print board with column and row numbers
    # distinguish between revealed and non-revealed squares
    height = len(board)
    width = len(board[0])

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
                block = board[r][c]
            elif mask[r][c] == 1:
                block = " "
            else:
                raise ValueError('Mask value must be 0 or 1.')
            print "  %s  " % block,
        print "" # newline


if __name__ == "__main__":

    board = create_board()
    mask = create_mask(1)

    while True:
         print_board(board,mask)
         move = get_input()
         mask = update_mask(board,mask,move)
