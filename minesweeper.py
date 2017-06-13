MINE_DENSITY = 0.20 # based on online game 16x30 board with 99 mines
BOARD_WIDTH = 10
BOARD_HEIGHT = 10

def create_board(size):
    width, height = size
    area = width * height

    # create board as list of lists (list of rows)
    board = []
    for r in range(0,height):
        row = [0] * width
        board.append(row)

    # place mines
    # count adjacent mines
    return board

def get_input():
    # get column and row number
    pass

def update_board(move):
    # if coordinates are a mine, game over
    # elif number, reveal that square only
    # elif blank, reveal adjacent area up to numbers
        # if blank, go out one step in each direction (recursive)
        # if number, clear that space and stop
    pass

def print_board(board):
    # print board with column and row numbers
    # distinguish between revealed and non-revealed squares
    height = len(board)
    width = len(board[0])

    # print column labels
    print " " * 6,
    for c in range(0,width):
        print "  %s  " % c,
    print "" # newline

    print " " * 6,
    for c in range(0,width):
        print "_____",
    print "" # newline

    # print row labels
    for r in range(0,height):
        print "  %i  |" % r,
        row = board[r]
        for c in range(0,width):
            block = row[c]
            print "  %i  " % block,
        print "" # newline


if __name__ == "__main__":
    size = (BOARD_WIDTH,BOARD_HEIGHT)
    board = create_board(size)
    print_board(board)

    # while gameplay == True:
    #     print_board(board)
    #     move = get_input()
    #     board = update_board(move)
