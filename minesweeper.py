import random

MINE_DENSITY = 0.20 # based on online game 16x30 board with 99 mines
BOARD_WIDTH = 10
BOARD_HEIGHT = 10

def create_board(size):
    width, height = size
    area = width * height

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
        spacing = 3 - len(str(c))
        print "  %i%s" % (c,spacing*" "),
    print "" # newline

    print " " * 6,
    for c in range(0,width):
        print "_____",
    print "" # newline

    # print row labels
    for r in range(0,height):
        spacing = 3 - len(str(r))
        print "  %i%s|" % (r,spacing*" "),
        row = board[r]
        for c in range(0,width):
            block = row[c]
            print "  %s  " % block,
        print "" # newline


if __name__ == "__main__":
    size = (BOARD_WIDTH,BOARD_HEIGHT)
    board = create_board(size)
    print_board(board)

    # while gameplay == True:
    #     print_board(board)
    #     move = get_input()
    #     board = update_board(move)
