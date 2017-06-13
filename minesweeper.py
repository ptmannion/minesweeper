import random
import pdb

MINE_DENSITY = 0.20 # based on online game 16x30 board with 99 mines
BOARD_WIDTH = 10
BOARD_HEIGHT = 10

def create_board(size):
    '''create board with mines and adjacency counts, plus full mask'''

    width, height = size
    area = width * height

    # create mask as list of lists (list of rows)
    mask = []
    for r in range(0,height):
        row = [1] * width
        mask.append(row)

    # create board as list of lists (list of rows)
    board = []
    for r in range(0,height):
        row = ["0"] * width
        board.append(row)

    # place mines
    for r in range(0,height):
        for c in range(0,width):
            v = random.randint(1,1/MINE_DENSITY)
            if v == 1:
                has_mine = True
            else:
                has_mine = False

            if has_mine:
                board[r][c] = "*"

    # count adjacent mines
    for r in range(0,height):
        for c in range(0,width):
            if board[r][c] == "*":
                continue

            # enumerate neighbor coords clockwise from top
            neighbors = [(r-1,c),
            (r-1,c+1),
            (r,c+1),
            (r+1,c+1),
            (r+1,c),
            (r+1,c-1),
            (r,c-1),
            (r-1,c-1)
            ]

            # count neighboring mines and use to update block
            count = 0
            for nr,nc in neighbors:
                if nr < 0 | nc < 0:
                    # case of board edge causing negative index
                    continue

                try:
                    if board[nr][nc] == "*":
                        count += 1
                except IndexError:
                    # case of board edge causing too large index
                    pass

            board[r][c] = str(count)

    return (board,mask)

def get_input(size):
    ''' get user input of column and row number '''

    width, height = size

    print "Select a block to click (format: row,column): "
    user_input = raw_input()

    try:
        r,c = user_input.split(",")
        r = int(r)
        c = int(c)

        if r >= height:
            print "Maximum row value is %i. Try again:" % (height-1)
            move = get_input(size)
        elif c >= width:
            print "Maximum column value is %i. Try again:" % (width-1)
            move = get_input(size)
        else:
            move = (r,c)

    except ValueError:
         print "Please use the format specified, e.g., '0,0'"
         move = get_input(size)

    return move

def update_board(move):
    # if coordinates are a mine, game over
    # elif number, reveal that square only
    # elif blank, reveal adjacent area up to numbers
        # if blank, go out one step in each direction (recursive)
        # if number, clear that space and stop
    pass

def print_board(board,mask):
    # print board with column and row numbers
    # distinguish between revealed and non-revealed squares
    height = len(board)
    width = len(board[0])

    # print column labels
    print " " * 6,
    for c in range(0,width):
        spacing = 3 - len(str(c))
        print "  %i%s" % (c,spacing*" "),
    print "" # newline

    print " " * 6,
    for c in range(0,width):
        print "_____",
    print "" # newline


    for r in range(0,height):
        # print row labels
        spacing = 3 - len(str(r))
        print "  %i%s|" % (r,spacing*" "),

        # print row contents
        for c in range(0,width):
            if mask[r][c] != 1:
                block = board[r][c]
            else:
                block = "?"
            print "  %s  " % block,
        print "" # newline


if __name__ == "__main__":
    size = (BOARD_WIDTH,BOARD_HEIGHT)
    board,mask = create_board(size)
    print_board(board,mask)
    get_input(size)

    # while gameplay == True:
    #     print_board(board)
    #     move = get_input()
    #     board = update_board(move)
